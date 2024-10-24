#!/usr/bin/env python3
"""

This module defines the class `Quadric` and some
companion functions (for plotting).

"""

import numpy as np
import scipy.sparse
import imageio
from tempfile import NamedTemporaryFile
from io import BytesIO
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401


from quadproj.utils import get_project_root, get_tmp_path, get_output_path, get_tmp_gif_path


root = get_project_root()
tmp_path = get_tmp_path()
output_path = get_output_path()
tmp_gif_path = get_tmp_gif_path()

global eps_p
eps_p = pow(10, -10)
eps_dev = eps_p


class Quadric:
    """
    Quadric class.

    This class defines a quadric (or quadratic hypersurface) object.

    The quadric Q is the set of points that verify:
    x' A x + b' x +c = 0.

    To ease computation and be able to project easily onto Q,
    we consider (via a coordinate change) the quadric in *normal* or *normalized* form:

    x' D x = 1,

    where D is a diagonal matrix containing the eigenvalues (sorted descending).

    Any quadric cannot be reduced to a standard form, we also consider the *reduced* form

    x' D x + b_reduced' x + c = 0

    where b_reduced is in general different than the original ones.

    Such diagonalization requires computing the eigendecomposition
    that may be expensive for large dimensions.

    Since quadrics are within a sign difference:
    x' A x + b'x + c = 0 <=> x' (-A) x + (-b') x + (-c) = 0
    we change the sign to ensure the largest eigenvalue (in absolute value) is positive (see 'check_equality_sign').

    Please refer to the `Notes` section or the companion paper for
    further explanation.


    Attributes
    ----------
    A : ndarray
        2-D ndarray :math:`\\in \\mathbb{R}^{n \\times n}` defining the not standardized quadratic form.
    b : ndarray
        1-D ndarray :math:`\\in \\mathbb{R}^n` defining the not standardized quadratic form.
    c : float
        Independent parameter of the not standardized quadratic form.
    d : ndarray
    1-D ndarray :math:`\\in \\mathbb{R}^n` if it exists: containing the not standardized quadric center.
    dim : float
        Quadric dimension: :math:`n`.
    gamma : float
        Parameter of non-singular matrix: :math:`\\gamma = \\sqrt{\\big |c  + \\mathbf{b}^t \\mathbf{d} + \\mathbf{d}^t \\mathbf{d} \\big |} \\in \\mathbb{R}`.
    is_empty : bool
        Whether the quadric is empty.
    is_diagonal : bool
        Whether the input matrix is diagonal, if yes we do not compute the eigendecomposition.
    eig : ndarray
        1-D ndarray :math:`\\in \\mathbb{R^n}` containing (sorted, descending) eigenvalues of `A`.
    eig_bar : ndarray
        1-D ndarray `eig` with no repetition.
    type : {''unknown'', ''ellipsoid'', ''hyperboloid'', ''paraboloid'', ''simple plane'', ''double planes'', ''elliptic cone''} (and every combination with ''cylinder'' appended at the end (e.g., ellipsoid cylinder)
        Quadric type.
    V : ndarray
        2-D ndarray :math:`\\in \\mathbb{R^{n \\times n}}` containing eigenvectors of `A` associated to `eig`.
    L : ndarray
        2-D ndarray :math:`\\in \\mathbb{R^{n \\times n}}` diagonal matrix containing `eig`.
    axes : ndarray
        1-D ndarray :math:`\\in \\mathbb{R^n}` containing the axis length of the quadric.


    Notes
    -----
    However, because there are quadrics where the underlying matrix `A` is singular, we consider the **standardized** version:
    this matrix is diagonalized, i.e., rotated by using the decomposition
    :math:`A = V L V^t` where :math:`L` is diagonal matrix containing the eigenvalues
    and :math:`V` the orthonormal matrix containing the associated eigenvectors.

    .. math::  \\mathbf{y}^t L \\mathbf{y} +  \\mathbf{y}^t \\mathbf{b}^r + c = 0

    where :math:`\\mathbf{b}^r = V^t \\mathbf{r}`.

    **Remark**: We sort the eigenvalues from the largest to the smallest.

    Notes on normalized
    -------------------
    If the matrix is nonsingular, we can go one step ahead in the simplification.

    Let :math:`A \\in \\mathbb{R}^{n \\times n}, \\mathbf{b} \\in \\mathbb{R}^n, c \\in \\mathbb{R}`, we
    consider quadric on the form

    .. math::  \\mathbf{y}^t A \\mathbf{y} + \\mathbf{y}^t \\mathbf{b} + c = 0

    that can be changed (via scaling and shifting) under the form

    .. math:: \\mathbf{z}^t A \\mathbf{z} = 1

    with :math:`\\mathbf{y} = \\mathbf{z}  \\gamma + \\mathbf{d}`,  :math:`\\mathbf{d} = - \\frac{A^{-1}  \\mathbf{b}}{2}` and
    :math:`\\gamma = \\sqrt{\\big |c  + \\mathbf{b}^t \\mathbf{d} + \\mathbf{d}^t A \\mathbf{d} \\big |} \\in \\mathbb{R}`.

    This quadric can then be diagonalized, i.e., rotated by using the decomposition
    :math:`A = V L V^t` where :math:`L` is diagonal matrix containing the eigenvalues
    and :math:`V` the orthonormal matrix containing the associated eigenvectors.

    It follows that :math:`\\mathbf{u}^t L \\mathbf{u} = 1` with :math:`\\mathbf{u} = V^t \\mathbf{z}`
    and therefore :math:`\\mathbf{x} = \\mathbf{d} + \\gamma  V \\mathbf{u}`.

    This gives us a **normalized** quadric

    .. math:: \\mathcal{Q} = \\Big \\{ \\mathbf{x} \\in \\mathbb{R}^n \\Big | \\mathbf{x}^t L \\mathbf{x} - 1 = 0  \\Big \\}

    and we have

    .. math::  \\mathbf{x}^t L \\mathbf{x} - 1  =
        \\sum_{i=1}^n \\lambda_i \\mathbf{x}^2 -1 .

    """

    class EmptyQuadric(Exception):
        """
        Python-exception-derived object raised by `quadproj.quadrics.Quadric` class.

        Raised when the quadric is empty.

        .. deprecated:: 0.046
            This may change in further releases and empty quadrics could be accepted.

        """

        def __str__(self):
            return 'Quadric appears to be empty'

    class InvalidArgument(Exception):
        """
        Python-exception-derived object raised by `quadproj.quadrics.Quadric` class.

        Raised when the constructor is called with invalid arguments.

        """

        def __init__(self, msg):
            self.msg = 'Invalid input arguments\n' + msg

        def __str__(self):
            return self.msg

    class NotNormalized(Exception):
        """
        Python-exception-derived object raised by `quadproj.quadrics.Quadric` class.

        Raised while using a method requiring a normalized quadric and the instance
        is not normalized.

        """
        def __str__(self):
            return 'Quadric is not normalized, please normalized the quadric.'

    def __init__(self, A, b, c, is_diagonal=False, **kwargs):
        try:
            self.A = A
            if not np.allclose(self.A, self.A.T):
                raise self.InvalidArgument('Matrix is not symmetric!')

            self.b = b
            self.c = c
        except KeyError:
            raise self.InvalidArgument('Please enter matrices (ndarray)\
                             A [n x n], b [n x 1] and a float c')

        self.d, _, self.r, _ = np.linalg.lstsq(self.A, -self.b / 2.0, rcond=None)
        self.dim = np.size(self.A, 0)
        self.type = "unknown"
        if not is_diagonal:
            self.eig, self.V = np.linalg.eigh(self.A)
        else:
            self.eig = self.A
            self.V = np.eye(self.dim)

        idx = np.argsort(-self.eig)
        self.eig = self.eig[idx]
        indexes = np.unique(self.eig[idx], return_index=True)[1]
        self.eig_bar = [self.eig[_idx] for _idx in sorted(indexes)]
        self.L = np.diag(self.eig)  # correctly sorted
        self.T = np.eye(self.dim)
        self.V = self.V[:, idx]
        self.b_reduced = self.V.T @ self.b
        if not self.check_equality_sign():
            print('\n\nSwitching equality sign!\n\n')
            self.__init__(A=-self.A, b=-self.b, c=-self.c)
        self.is_normalized = False

        self.gamma = self.c + self.b.T @ self.d + self.d.T @ self.A @ self.d
        if self.r == 0:
            raise NotImplementedError("Quadric is linear")
        elif self.r == 1 and np.all(abs(self.b_reduced[1:])) < eps_dev:
            self.delta = self.b_reduced[0]**2 - 4 * self.L[0, 0] * self.c
            if self.delta > -eps_dev:
                self.sol_R = (-self.b_reduced[0] + np.sqrt(self.delta)) / (2 * self.L[0, 0])
                if abs(self.delta) < eps_dev:
                    self.type = "simple plane"
                    self.sol_L = self.sol_R
                else:
                    self.type = "double planes"
                    self.sol_L = (-self.b_reduced[0] - np.sqrt(self.delta)) / (2 * self.L[0, 0])

        elif self.r < self.dim:
            self.noncylindric_indices = []
            self.cylindric_indices = []

            A_b = np.append(A, b.reshape(self.dim, 1), axis=1)
            r2 = np.linalg.matrix_rank(A_b)
            if self.r < self.dim - 1 and r2 > self.r:
                # take the first one that is nonzero (there must have one!) and then use it to null all the other such that at the end there is only one entry of this (sub)b that is nonzero
                for i, eig in enumerate(self.eig):
                    if abs(eig) > eps_dev:
                        self.noncylindric_indices.append(i)
                    else:
                        self.cylindric_indices.append(i)
                T = np.eye(self.dim)

                non_zero_cylindric_indices = [i for i in self.cylindric_indices if abs(self.b_reduced[i]) > eps_dev]
                pivot_cylinder = non_zero_cylindric_indices.pop()

                self.cylindric_indices.remove(pivot_cylinder)
                self.noncylindric_indices.append(pivot_cylinder)
                self.noncylindric_indices.sort()

                for i in non_zero_cylindric_indices:
                    T[pivot_cylinder, i] = - self.b_reduced[i] / self.b_reduced[pivot_cylinder]
                self.T = T
            elif r2 > self.r:
                self.noncylindric_indices = list(range(self.dim))
                self.cylindric_indices = []
            else:
                for i, eig in enumerate(self.eig):
                    if abs(eig) > eps_dev or abs(self.b_reduced[i]) > eps_dev:
                        self.noncylindric_indices.append(i)
                    else:
                        self.cylindric_indices.append(i)

            self.all_indices = np.array(self.noncylindric_indices + self.cylindric_indices)
            if len(self.noncylindric_indices) < self.dim:
                sub_L = self.L[self.noncylindric_indices, :][:, self.noncylindric_indices]
                sub_b = self.b_reduced[self.noncylindric_indices]
                sub_A = sub_L
                self.sub_Q = Quadric(A=sub_A, b=sub_b, c=self.c)
                self.type = self.sub_Q.type + " cylinder"
                print("Quadric is cylindrical!")
                print("SubQuadric is!", self.sub_Q.type)
            else:
                self.type = "paraboloid"
        elif self.r == self.dim:
            if np.all(self.eig > 0):
                self.type = "ellipsoid"
            elif abs(self.gamma) > eps_dev:
                self.type = "hyperboloid"
            else:
                self.type = "elliptic cone"
        self.axes = np.zeros(self.dim)
        for i in range(self.dim):
            if abs(self.eig[i]) > eps_dev:
                self.axes[i] = np.sign(self.eig[i]) * 1 / np.sqrt(abs(self.eig[i]))
        self.is_empty = self.check_empty()
        if self.is_empty:
            print('Quadric appears to be empty!')
            return

    def __str__(self):
        return f"Quadric of type {self.type}"

    def check_equality_sign(self):
        """
        check that the max eigenvalue (in absolute value) is positive
        """
        if self.dim == 1:
            if self.eig[0] < 0:
                return True
            elif self.b[0] < 0:
                return True
            elif self.c < 0:
                return True
            return False

        if self.eig[0] > abs(self.eig[-1]):
            return True  # meaning we do NOT want to switch equality sign
        elif self.eig[0] < -self.eig[-1]:
            return False
        elif self.eig[0] > 0:
            return True
        else:
            if np.all(self.b_reduced == self.b_reduced[0]):
                if self.eig[0] == 0:
                    return self.c >= 0
                else:
                    return np.sign(self.eig[0])
            else:
                if self.eig[0] == 0:
                    return self.b_reduced[0] >= 0
                else:
                    return np.sign(-self.eig[0])

    def check_empty(self):
        """
        Check whether the quadric is empty.

        Return True if quadric is empty


        """
        if self.is_paraboloid:
            return
        elif self.is_planes:
            return self.delta < 0

        if self.is_cylindrical:
            return self.sub_Q.check_empty()

        if self.c + self.b @ self.d / 2 < 0:
            p = np.sum(self.eig > 0)
        else:
            p = np.sum(self.eig < 0)
        return p == 0

    def is_feasible(self, x):
        return abs(self.evaluate_point(x)) <= eps_dev

    def evaluate_point(self, x):
        """
        Compute x' A x + b' x + c.

        Parameters
        ----------
        x : ndarray
            1-D array, point not standardized.
        """
        if scipy.sparse.issparse(self.A):
            out = np.dot(self.A.dot(x), x) + np.dot(self.b, x) + self.c
        else:
            out = np.dot(np.dot(x, self.A), x) + np.dot(self.b, x) + self.c
        return out

    def is_in_quadric(self, x):
        """
        Check whether a point is inside the quadric.

        For a circle (boundary of a 1-D ball),
        check whether it is in the ball.

        Parameters
        ----------
        x : ndarray
            1-D array, point not standardized.
        """
        return self.evaluate_point(x) <= 0

    def get_tangent_plane(self, x, forced=False):
        """
        Compute the direction of the tangent space.

        Parameters
        ----------
        x : ndarray
            1-D array, point not standardized and feasible.
        force : bool
            If `True`, compute the tangent plane even if `x` is not feasible.
        """
        if not forced:
            if not self.is_feasible(x):
                raise ValueError('Cannot compute tan gent plane on infeasible points')
        Tp = 2 * np.dot(self.A, x) + self.b
        return Tp

    def get_starting_point_from_feasible_point(self, x, distance=1):
        """
        Starting from a feasible point x, gets a point x0 in the direction (outward) of Tp
        such that the projection of x0 on the quadric will be x.

        The goal of this function is to create projection problems which we know the solution of (for testing purpose)

        Parameters
        ----------
        x: ndarray
            1-D array, point feasible
        length: int
            distance between x and x0, defaulted to 1

        """
        grad = self.get_tangent_plane(x)
        normalized_grad = grad / np.linalg.norm(grad)

        sign = np.sign(np.random.randn(1)[0])
        return x + sign * normalized_grad * distance

    @property
    def is_paraboloid(self):
        return self.type == "paraboloid" or self.is_paraboloid_cylinder

    @property
    def is_elliptic_paraboloid(self):
        return self.is_paraboloid and np.all(self.eig >= - eps_dev)

    @property
    def is_hyperbolic_paraboloid(self):
        return self.is_paraboloid and np.any(self.eig < - eps_dev)

    @property
    def is_paraboloid_cylinder(self):
        return self.type == "paraboloid cylinder"

    @property
    def is_double_planes(self):
        return self.type == "double planes"

    @property
    def is_simple_plane(self):
        return self.type == "simple plane"

    @property
    def is_planes(self):
        return "plane" in self.type

    @property
    def is_ellipse(self):
        return self.is_ellipsoid and self.dim == 2

    @property
    def is_hyperbola(self):
        return self.is_hyperboloid and self.dim == 2

    @property
    def is_parabola(self):
        return self.is_paraboloid and self.dim == 2

    @property
    def is_ellipsoid(self):
        return self.type == "ellipsoid" or self.is_ellipsoid_cylinder

    @property
    def is_ellipsoid_cylinder(self):
        return self.type == "ellipsoid cylinder"

    @property
    def is_hyperboloid_cylinder(self):
        return self.type == "hyperboloid cylinder"

    @property
    def is_hyperboloid(self):
        return self.type == "hyperboloid"

    @property
    def is_elliptic_cone(self):
        return abs(self.gamma) < eps_dev and np.any(self.eig < 0) and self.r == self.dim

    @property
    def is_elliptic_cone_cylinder(self):
        return self.type == "elliptic cone cylinder"

    @property
    def is_one_sheet_hyperboloid(self):
        return self.dim == 3 and self.is_hyperboloid and self.gamma * np.prod(self.axes) > 0

    @property
    def is_two_sheet_hyperboloid(self):
        return self.dim == 3 and self.is_hyperboloid and np.prod(self.axes) * self.gamma < 0

    @property
    def is_cylindrical(self):
        return "cylinder" in self.type

    def to_non_standardized(self, x):
        return self.V @ x

    def to_non_normalized(self, x):
        """Denormalize a point.

        Given a standardized point x such that
        x' L x = 1,
        returns a point y such that
        y' A y + b' y + c = 0.

        Parameters
        ----------
        x : ndarray
            1-dimensional ndarray :math:`\\in \\mathbb{R}^n` non-standardized input.
        Returns
        -------
        x : ndarray
            1-dimensional ndarray :math:`\\in \\mathbb{R}^n` standardized output.
        """

        if not self.is_standardized:
            raise self.NotNormalized()
        y = self.V @ (x * np.sqrt(abs(self.gamma))) + self.d
        return y

    def to_standardized(self, y):
        return self.V.T @ y

    def to_normalized(self, y):
        """Normalize a point.

        Given a not normalized point y such that
        y' A y + b' y + c = 0,
        returns a point x such that
        x' L x = 1.

        Parameters
        ----------
        y : ndarray
            1-dimensional ndarray :math:`\\in \\mathbb{R}^n` normalized intput.
        Returns
        -------
        x : ndarray
            1-dimensional ndarray :math:`\\in \\mathbb{R}^n` non-normalized output
        """
        if not self.is_standardized:
            raise self.NotNormalized()
        x = self.V.T @ (y - self.d) / np.sqrt(abs(self.gamma))
        return x

    def plot(self, show=False, path_file=None, show_principal_axes=False, **kwargs):
        """Plot the (2D or 3D) standardized quadric.

        This function plot a standardized quadric in the unstandardized domain.

        If the `matplotlib.pyplot.figure` `fig` and `matplotlib.axes` `ax` is not \
        provided as argument, the function creates some.

        Parameters
        ----------
        show : bool, default=False
            Whether we show the plot.
        path_file : str, default=None
            If not `None`, save the figure at `path_file`.
        show_principal_axes : bool, default=False
            Whether we show the principal axes plot.
        **kwargs : {fig, ax}
            Additional arguments with keywords.

        Returns
        -------
        fig : matplotlib.pyplot.figure
            Figure instance where the quadric is plotted.
        ax : matplotlib.axes
            Axes instance where the quadric is plotted.
        """
        fig, ax = get_fig_ax(self)
        if 'fig' in kwargs:
            fig = kwargs['fig']
        if 'ax' in kwargs:
            ax = kwargs['ax']

        dim = self.dim
        assert dim <= 3, 'Sorry, I can not represent easily > 3D spaces...'  # TODO remove assert
        assert self.type != 'unknown', 'Diagonalize is none, impossible to know quadric type'  # TODO remove assert
        m = 1000
        quadric_color = 'royalblue'

        T = np.linspace(-np.pi, np.pi, m)
        x = np.zeros_like(T)
        y = np.zeros_like(T)
        gamma = (np.sqrt(abs(self.c + self.d.T @ self.A @ self.d + self.b.T @ self.d)))

        if dim == 2:
            x = np.zeros_like(T)
            y = np.zeros_like(T)
            flag_double_plot = self.is_hyperboloid or self.is_double_planes or self.is_elliptic_cone

            d = self.d
            for i, t in enumerate(T):
                if self.is_hyperbola:
                    t = t / 4  # otherwise we plot too much of the quadric...
                    v = self.d + (self.V @ np.array([self.axes[0] / np.cos(t),
                                                     -self.axes[1] * np.tan(t)])) * gamma
                    v2 = self.d + (self.V @ np.array([self.axes[0] / np.cos(t + np.pi),
                                                      -self.axes[1] * np.tan(t + np.pi)])) * gamma
                    x[i // 2], y[i // 2] = (v[0], v[1])
                    x[i // 2 + m // 2], y[i // 2 + m // 2] = (v2[0], v2[1])
                elif self.is_ellipse:
                    v = self.d + (self.V @ np.array([self.axes[0] * np.cos(t),
                                                     self.axes[1] * np.sin(t)])) * gamma
                    #   v = np.array([self.axes[0]*np.cos(t), self.axes[1] * np.sin(t)])
                    x[i], y[i] = (v[0], v[1])
                elif self.is_parabola:

                    a_x = np.sqrt(self.eig[0])
                    b_x = self.b_reduced[0] / 2 / a_x
                    c = np.sqrt(-self.c + b_x**2)

                    # parametrization for x^2 + 4*a*y = 0  as x = -2*a*t and y = -a * t^2
                    d = np.array([-b_x, c**2])

                    def _y(t):
                        return -(self.eig[0] * t**2 + self.b_reduced[0] * t + self.c) / self.b_reduced[1]

                    v = (self.V @ np.array([t, _y(t)]))

                    d_x = -self.b_reduced[0] / (2 * self.eig[0])
                    d = self.V @ np.array([d_x, _y(d_x)])

                    x[i], y[i] = (v[0], v[1])
                    _y = np.array([v[0], v[1]])
                    assert self.is_feasible(_y)

                elif self.is_elliptic_cone:
                    sol_R = np.sqrt(abs(self.eig[0] / self.eig[1])) * t
                    sol_L = -sol_R
                    v = np.array([t, sol_R])
                    v2 = np.array([t, sol_L])
                    x[i // 2], y[i // 2] = self.V @ np.array([v[0], v[1]])
                    x[i // 2 + m // 2], y[i // 2 + m // 2] = self.V @ np.array([v2[0], v2[1]])

                elif self.is_double_planes:
                    v = np.array([self.sol_R, t])
                    v2 = np.array([self.sol_L, t])
                    x[i // 2], y[i // 2] = self.V @ np.array([v[0], v[1]])
                    x[i // 2 + m // 2], y[i // 2 + m // 2] = self.V @ np.array([v2[0], v2[1]])
                elif self.is_simple_plane:
                    v = self.V @ np.array([self.sol_R, t])
                    x[i], y[i] = (v[0], v[1])
            if flag_double_plot:
                ax.plot(x[:m // 2], y[:m // 2], color=quadric_color, zorder=1,
                        label=r'$\mathcal{Q}$')
                ax.plot(x[m // 2:], y[m // 2:], color=quadric_color, zorder=1)
            else:
                ax.plot(x, y, color=quadric_color, label=r'$\mathcal{Q}$', zorder=1)
            ax.scatter(d[0], d[1], color=quadric_color, label=r'$\mathbf{d}$', zorder=2)
            if show_principal_axes:
                for i in range(dim):
                    xR = d + self.V[:, i]
                    xL = d - self.V[:, i]
                    L1 = plt.Line2D([xR[0], xL[0]], [xR[1], xL[1]], linestyle='--', color='black', zorder=1)
                    ax.add_artist(L1)
                ax.plot([0], [0], label='Principal axes', color='k', linestyle='--')
        elif dim == 3:
            m1 = 40
            m2 = 20
            d = self.d
            if self.is_one_sheet_hyperboloid:
                t, s = np.mgrid[0:2 * np.pi:m1 * 1j, -1:1:m2 * 1j]
                if self.axes[1] > 0:  # meaning we have 2 "+" and one "-" the sec is on axe 2
                    u_x = self.axes[0] * np.cos(t) * np.sqrt(1 + s**2)
                    u_y = self.axes[1] * np.sin(t) * np.sqrt(1 + s**2)
                    u_z = self.axes[2] * s
                else:
                    u_x = self.axes[0] * s
                    u_y = self.axes[1] * np.sin(t) * np.sqrt(1 + s**2)
                    u_z = self.axes[2] * np.cos(t) * np.sqrt(1 + s**2)

                U_vec = np.tile(self.d, (m1 * m2, 1)).T\
                    + self.V @ np.vstack((u_x.flatten(), u_y.flatten(), u_z.flatten())) * gamma
                x = np.reshape(U_vec[0, :], (m1, m2))
                y = np.reshape(U_vec[1, :], (m1, m2))
                z = np.reshape(U_vec[2, :], (m1, m2))

            elif self.is_two_sheet_hyperboloid:
                t, s1 = np.mgrid[0:2 * np.pi:m1 * 1j, 0:np.pi / 2 - 1:m2 // 2 * 1j]
                _, s2 = np.mgrid[0:2 * np.pi:m1 * 1j, np.pi / 2 + 1:np.pi:m2 // 2 * 1j]
                s = np.hstack((s1, s2))
                t = np.hstack((t, t))
                if self.axes[1] > 0:  # meaning we have 2 "+" and one "-" the sec is on axe 2
                    u_x = self.axes[0] * np.sin(t) * np.tan(s)
                    u_y = self.axes[1] * np.cos(t) * np.tan(s)
                    u_z = self.axes[2] / np.cos(s)
                else:  # 1 "+" and 2 "-": the sec is on axe 0
                    u_x = self.axes[0] / np.cos(s)
                    u_y = self.axes[1] * np.cos(t) * np.tan(s)
                    u_z = self.axes[2] * np.sin(t) * np.tan(s)

                U_vec = np.tile(self.d, (m1 * m2, 1)).T \
                    + self.V @ np.vstack((u_x.flatten(), u_y.flatten(), u_z.flatten())) * gamma
                x = np.reshape(U_vec[0, :], (m1, m2))
                y = np.reshape(U_vec[1, :], (m1, m2))
                z = np.reshape(U_vec[2, :], (m1, m2))
                x1 = x[:, :m2 // 2]
                y1 = y[:, :m2 // 2]
                z1 = z[:, :m2 // 2]
                x2 = x[:, m2 // 2:]
                y2 = y[:, m2 // 2:]
                z2 = z[:, m2 // 2:]
            elif self.is_ellipsoid_cylinder:
                t, z = np.mgrid[0:2 * np.pi:m1 * 1j, -1:1:m2 * 1j]

                sub_Q = self.sub_Q

                u_x = sub_Q.axes[0] * np.cos(t)
                u_y = sub_Q.axes[1] * np.sin(t)
                u_z = z
                U_vec = np.tile(self.d, (m1 * m2, 1)).T\
                    + self.V @ np.vstack((u_x.flatten(), u_y.flatten(), u_z.flatten())) * gamma
                x = np.reshape(U_vec[0, :], (m1, m2))
                y = np.reshape(U_vec[1, :], (m1, m2))
                z = np.reshape(U_vec[2, :], (m1, m2))
            elif self.is_elliptic_cone_cylinder:

                m2 = m2 // 2
                t, z = np.mgrid[-np.pi / 4: np.pi / 4:m1 * 1j, -1:1:m2 * 1j]

                u_x_1 = t
                u_y_1 = np.sqrt(abs(self.eig[0] / self.eig[2])) * t
                u_x_2 = t
                u_y_2 = -u_x_1
                u_z = z

                V2 = np.zeros_like(self.V)
                V2[self.all_indices, np.arange(self.dim)] = 1

                U_vec1 = np.tile(self.d, (m1 * m2, 1)).T\
                    + self.V @ V2 @ np.vstack((u_x_1.flatten(), u_y_1.flatten(), u_z.flatten()))
                U_vec2 = np.tile(self.d, (m1 * m2, 1)).T\
                    + self.V @ V2 @ np.vstack((u_x_2.flatten(), u_y_2.flatten(), u_z.flatten()))
                x1 = np.reshape(U_vec1[0, :], (m1, m2))
                y1 = np.reshape(U_vec1[1, :], (m1, m2))
                z1 = np.reshape(U_vec1[2, :], (m1, m2))
                x2 = np.reshape(U_vec2[0, :], (m1, m2))
                y2 = np.reshape(U_vec2[1, :], (m1, m2))
                z2 = np.reshape(U_vec2[2, :], (m1, m2))
                m2 = m2 * 2
            elif self.is_elliptic_cone:
                t, z = np.mgrid[0:2 * np.pi:m1 * 1j, -1:1:m2 * 1j]
                u_x = self.axes[0] * np.cos(t) * z
                u_y = self.axes[1] * np.sin(t) * z
                u_z = -self.axes[2] * z
                U_vec = np.tile(self.d, (m1 * m2, 1)).T\
                    + self.V @ np.vstack((u_x.flatten(), u_y.flatten(), u_z.flatten()))
                x = np.reshape(U_vec[0, :], (m1, m2))
                y = np.reshape(U_vec[1, :], (m1, m2))
                z = np.reshape(U_vec[2, :], (m1, m2))
            elif self.is_hyperboloid_cylinder:
                m2 = m2 // 2
                t, z = np.mgrid[-np.pi / 4: np.pi / 4:m1 * 1j, -1:1:m2 * 1j]

                u_x_1 = self.sub_Q.axes[0] / np.cos(t)
                u_y_1 = -self.sub_Q.axes[1] * np.tan(t)
                u_x_2 = self.sub_Q.axes[0] / np.cos(t + np.pi)
                u_y_2 = -self.sub_Q.axes[1] * np.tan(t + np.pi)
                u_z = z

                V2 = np.zeros_like(self.V)
                V2[self.all_indices, np.arange(self.dim)] = 1

                U_vec1 = np.tile(self.d, (m1 * m2, 1)).T\
                    + self.V @ V2 @ np.vstack((u_x_1.flatten(), u_y_1.flatten(), u_z.flatten())) * gamma
                U_vec2 = np.tile(self.d, (m1 * m2, 1)).T\
                    + self.V @ V2 @ np.vstack((u_x_2.flatten(), u_y_2.flatten(), u_z.flatten())) * gamma
                x1 = np.reshape(U_vec1[0, :], (m1, m2))
                y1 = np.reshape(U_vec1[1, :], (m1, m2))
                z1 = np.reshape(U_vec1[2, :], (m1, m2))
                x2 = np.reshape(U_vec2[0, :], (m1, m2))
                y2 = np.reshape(U_vec2[1, :], (m1, m2))
                z2 = np.reshape(U_vec2[2, :], (m1, m2))
                m2 = m2 * 2
            elif self.is_paraboloid_cylinder:
                s_min = -3
                s_max = 3
                s, t = np.mgrid[s_min:s_max:m1 * 1j, -3:3:m2 * 1j]

                a_x = np.sqrt(self.eig[0])
                b_x = self.b_reduced[0] / 2 / a_x
                c = self.c - b_x**2
                d_x = - self.b_reduced[0] / (2 * self.eig[0])
                d_y = 0
                d_z = (-c - a_x * d_x**2) / self.b_reduced[2]
                d = self.V @ [d_x, d_y, d_z]

                u_x = self.axes[0] * t + d_x
                u_y = -1 / self.b_reduced[1] * (t**2 / 2 + s / 2) + d_y
                u_z = -1 / self.b_reduced[2] * (t**2 / 2 - s / 2) + d_z

                U_vec = self.V @ np.vstack((u_x.flatten(), u_y.flatten(), u_z.flatten()))
                x = np.reshape(U_vec[0, :], (m1, -1))
                y = np.reshape(U_vec[1, :], (m1, -1))
                z = np.reshape(U_vec[2, :], (m1, -1))
            elif self.is_ellipsoid:
                t, s = np.mgrid[0:2 * np.pi:m1 * 1j, 0:np.pi:m2 * 1j]
                u_x = self.axes[0] * np.cos(t) * np.sin(s)
                u_y = self.axes[1] * np.sin(t) * np.sin(s)
                u_z = self.axes[2] * np.cos(s)
                U_vec = np.tile(self.d, (m1 * m2, 1)).T\
                    + self.V @ np.vstack((u_x.flatten(), u_y.flatten(), u_z.flatten())) * gamma

                x = np.reshape(U_vec[0, :], (m1, m2))
                y = np.reshape(U_vec[1, :], (m1, m2))
                z = np.reshape(U_vec[2, :], (m1, m2))
            elif self.is_elliptic_paraboloid:
                t, s = np.mgrid[0:2 * np.pi:m1 * 1j, -1:1.5:m2 * 1j]

                a_x = np.sqrt(self.eig[0])
                b_x = self.b_reduced[0] / 2 / a_x
                a_y = np.sqrt(self.eig[1])
                b_y = self.b_reduced[1] / 2 / a_y

                c = self.c - b_y**2 - b_x**2
                d_x = - self.b_reduced[0] / (2 * self.eig[0])
                d_y = - self.b_reduced[1] / (2 * self.eig[1])
                d_z = -c / self.b_reduced[2]
                d = self.V @ [d_x, d_y, d_z]

                u_x = self.axes[0] * np.cos(t) * s + d_x
                u_y = self.axes[1] * np.sin(t) * s + d_y
                u_z = - 1 / self.b_reduced[2] * s**2 + d_z
                U_vec = self.V @ np.vstack((u_x.flatten(), u_y.flatten(), u_z.flatten()))
                x = np.reshape(U_vec[0, :], (m1, m2))
                y = np.reshape(U_vec[1, :], (m1, m2))
                z = np.reshape(U_vec[2, :], (m1, m2))
            elif self.is_hyperbolic_paraboloid:
                t, s = np.mgrid[-4:4:m1 * 1j, -4:4:m2 * 1j]
                c = -self.c + self.b_reduced[0]**2 / 4 / self.eig[0] + self.b_reduced[2]**2 / 4 / self.eig[2]
                d_x = - self.b_reduced[0] / (2 * self.eig[0])
                d_y = c / self.b_reduced[1]
                d_z = - self.b_reduced[2] / (2 * self.eig[2])
                d = self.V @ [d_x, d_y, d_z]

                u_x = self.axes[0] * s + d_x
                u_y = -1 / self.b_reduced[1] * (s**2 - t**2) + d_y
                u_z = self.axes[2] * t + d_z
                U_vec = self.V @ np.vstack((u_x.flatten(), u_y.flatten(), u_z.flatten()))
                x = np.reshape(U_vec[0, :], (m1, m2))
                y = np.reshape(U_vec[1, :], (m1, m2))
                z = np.reshape(U_vec[2, :], (m1, m2))

            if self.is_two_sheet_hyperboloid or self.is_hyperboloid_cylinder or self.is_elliptic_cone_cylinder:
                ax.plot_surface(x1, y1, z1, color=quadric_color, alpha=0.3, label=r'$\mathcal{Q}$')
                ax.plot_wireframe(x1, y1, z1, color=quadric_color, alpha=0.7)
                ax.plot_surface(x2, y2, z2, color=quadric_color, alpha=0.3)
                ax.plot_wireframe(x2, y2, z2, color=quadric_color, alpha=0.7)

            else:
                ax.plot_surface(x, y, z, color=quadric_color, alpha=0.3, label=r'$\mathcal{Q}$')
                ax.plot_wireframe(x, y, z, color=quadric_color, alpha=0.7)

            ax.scatter(d[0], d[1], d[2],
                       color=quadric_color, label=r'$\mathbf{d}$')
            ax.set_aspect("equal")

            if show_principal_axes:

                for i in range(dim):
                    xR = d + self.V[:, i]
                    xL = d - self.V[:, i]
                    ax.plot([xR[0], xL[0]], [xR[1], xL[1]], [xR[2], xL[2]], linestyle='--', color='black', zorder=1)
                ax.plot([0], [0], [0], label='Principal axes', color='k', linestyle='--')
        plt.legend()
        if show:
            plt.show()
        if path_file is not None:
            fig.savefig(path_file)

        return fig, ax

    def get_turning_gif(self, gif_path, step=2, elev=25):
        """Create a gif.

        Plot the 3D quadric and create a rotating gif.

        Parameters
        ----------
        gif_path : str, default = ''out.gif..
            Path where the gif is written.
        elev : float, default=25
            Elevation angle.
        step : float, default=1
            Degree difference between two frames.
        """
        if self.dim != 3:
            raise self.InvalidArgument(f'Cannot create gif of quadric with dimension different\
                                       then 3. Current dim is {self.dim}.')
        fig, ax = self.plot()
        ax.grid(False)
        ax.axis('off')
        get_gif(fig, ax, gif_path=gif_path, step=step, elev=elev)


def get_gif(fig, ax, gif_path='out.gif', elev=25, step=2):
    """
        Create a rotating gif of a given figure.

        Parameters
        ----------
        fig : matplotlib.pyplot.figure
            Figure object to rotate.
        ax : matplotlib.axes
            Axes object to rotate.
        gif_path : str, default='out.gif'
            Path of the output gif.
        elev : float
            Elevation angle.
        step : float
            Degree difference between two frames.
    """
    azims = np.arange(1, 360, step)
    filenames = []
    for i, azim in enumerate(azims):
        ax.view_init(elev=elev, azim=azim)
        buf = BytesIO()
        ext = 'png'
        fig.savefig(buf, format=ext, dpi=96)
        fp = NamedTemporaryFile()
        with open(f"{fp.name}.{ext}", 'wb') as ff:
            ff.write(buf.getvalue())
            filenames.append(f"{fp.name}.{ext}")
        buf.close()
    write_gif(filenames, gif_name=gif_path)


def get_fig_ax(Q):
    """
    Create appropriate plot objects.

    This function creates a figure and axis instance \
    taking into account the dimension of the quadric.

    Parameters
    ----------
    Q : Quadric instance
        Quadric that we want to plot.

    Returns
    -------
    fig : matplotlib.pyplot.figure
        Figure instance to plot Q.
    ax : matplotlib.axes
        Axes instance to plot W.
    """
    fig = plt.figure()
    assert Q.dim in [2, 3], 'I can only plot 2 or 3D quadrics'  # TODO: remove assert into IllegalDimension exception
    if Q.dim == 2:
        ax = fig.add_subplot()
        ax.axis('equal')
        ax.set_aspect(1)
    else:
        ax = fig.add_subplot(projection='3d')
    return fig, ax


def write_gif(filenames, gif_name='out.gif'):
    """Write a gif.

    Given a list of image paths, create and safe a gif.

    Parameters
    ----------
    filenames: list of str
        List of the image paths.
    gif_name: str
        Path where to write the gif.


    """
    images = []
    for filename in filenames:
        images.append(imageio.imread(filename))
    imageio.mimsave(gif_name, images)  # fps=25 for projection
