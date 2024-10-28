#!/usr/bin/env python3

import numpy as np
from quadproj.quadrics import Quadric
import matplotlib.pyplot as plt

from scipy.stats import ortho_group


eps_test = pow(10, -6)
SHOW = True


def test_initiate_quadrics():
    param = {}
    param['A'] = np.array([[2, 0.4], [0.4, -1]])
    param['b'] = np.array([1, 1])
    param['c'] = 0

    Quadric(**param)


def test_equivalence_std():
    param = {}
    param['A'] = np.array([[2, 0.4], [0.4, -1]])
    param['b'] = np.array([1, 1])
    param['c'] = 1

    Q = Quadric(**param)
    x0_not_std = np.array([0, 1])
    x0 = Q.to_standardized(x0_not_std)
    assert abs(Q.evaluate_point(x0_not_std) - np.dot(np.dot(x0, Q.L), x0) - np.dot(Q.b_reduced, x0)
               - Q.c) < eps_test

    param = {}
    param['A'] = np.array([[-1, 0], [0, 2]])
    param['b'] = np.array([1, 0])
    param['c'] = -2
    param['diagonalize'] = True
    Q = Quadric(**param)
    x0_not_std = np.array([1, 1])

    assert Q.is_feasible(x0_not_std), 'Two points are equivalent iff they are feasible'
    x0 = Q.to_standardized(x0_not_std)

    assert np.all(x0_not_std == Q.to_non_standardized(x0)), \
        'Transform to and from standardized yield an error'
    assert abs(Q.evaluate_point(x0_not_std) -
               np.dot(np.dot(x0, Q.L), x0) + 1) < eps_test


def test_plot_1D():
    A = np.array([[1]])
    b = np.array([0])
    c = -1
    Q = Quadric(A=A, b=b, c=c)
    Q.plot(show=SHOW)


    A = np.array([[1]])
    b = np.array([-2])
    c = 1
    Q = Quadric(A=A, b=b, c=c)
    Q.plot(show=SHOW)


def test_plot_2D():
    param = {}
    param['A'] = np.array([[2, 0.4], [0.4, 1]])
    param['b'] = np.array([1, 1])
    param['c'] = 0.3
    try:
        Q = Quadric(**param)
    except Quadric.EmptyQuadric:
        print('Correctly catch empty quadric!')

    param = {}
    param['A'] = np.array([[2, 0.4], [0.4, -1]])
    param['b'] = np.array([1, 1])
    param['c'] = -1
    plt.close()
    Q = Quadric(**param)
    Q.plot(show_principal_axes=True)
    param = {}
    param['A'] = np.array([[2, 0.4], [0.4, 1]])
    param['b'] = np.array([1, 1])
    param['c'] = -1
    Q = Quadric(**param)
    if SHOW:
        plt.show()
        plt.close()
        fig, ax = plt.subplots()
        Q.plot(fig=fig, ax=ax, show=True, show_principal_axes=True)
    param['A'] = np.array([[2, 0.4], [0.4, -1]])
    param['b'] = np.array([1, 1])
    param['c'] = -1
    Q = Quadric(**param)
    if SHOW:
        plt.close()
        fig, ax = plt.subplots()
        Q.plot(fig=fig, ax=ax, show=True, show_principal_axes=True)
        plt.show()
        plt.close('all')


def test_plot_3D():

    print('\n\n Two sheets hyperboloid \n\n')

    param = {}
    param['A'] = np.array([[-2, 0.4, 0.5], [0.4, 1, 0.6], [0.5, 0.6, -3]])
    param['b'] = np.array([1, 1, 0])
    param['c'] = -1.5
    Q = Quadric(**param)

    Q.plot(show=SHOW, show_principal_axes=True)

    print('\n\n Ellipsoid cylinder \n\n')
    param = {}
    param['A'] = np.array([[1, 0, 0], [0, 2, 0], [0, 0, 0]])
    param['b'] = np.array([0, 2, 0])
    param['c'] = -1.5
    Q = Quadric(**param)
    assert Q.is_cylindrical
    Q.plot(show=SHOW, show_principal_axes=False)

    print('\n\n Paraboloid \n\n')
    param = {}
    param['A'] = np.array([[1, 0, 0], [0, 2, 0], [0, 0, 0]]) / 1
    param['b'] = np.array([0, 0, 1])
    param['c'] = -1.5
    Q = Quadric(**param)
    Q.plot(show=SHOW, show_principal_axes=True)
    print('\n\n Ellipsoid \n\n')

    param = {}
    param['A'] = np.array([[2, 0.4, 0.5], [0.4, 1, 0.6], [0.5, 0.6, 3]])
    param['b'] = np.array([1, 1, 0])
    param['c'] = -1.5
    Q = Quadric(**param)

    Q.plot(show=SHOW)
    plt.close('all')
    print('\n\n One sheet hyperboloid \n\n')
    param = {}
    param['A'] = np.array([[2, 0.4, 0.5], [0.4, 1, 0.6], [0.5, 0.6, -3]])
    param['b'] = np.array([1, 1, 0])
    param['c'] = -1.5
    Q = Quadric(**param)

    Q.plot(show=SHOW, show_principal_axes=True)

    plt.close('all')


def test_switching_equality():
    A = np.array([[-1, 0], [0, 0]])
    b = np.array([0, 1])
    c = 0

    Q = Quadric(A=A, b=b, c=c)
    assert np.linalg.norm(Q.A + A) < eps_test

    A = np.array([[1, 0], [0, 1]])
    Q = Quadric(A=A, b=b, c=c)
    assert np.linalg.norm(Q.A - A) < eps_test

    Q = Quadric(A=-A, b=-b, c=-c)
    assert np.linalg.norm(Q.A - A) < eps_test

    A = np.array([[-1, 0], [0, 1]])
    Q = Quadric(A=A, b=b, c=c)
    assert np.linalg.norm(Q.A - A) < eps_test


def test_parallel_lines():
    A = np.array([[1, 0], [0, 0]])
    b = np.array([0, 0])
    c = 1
    Q = Quadric(A=A, b=b, c=c)
    assert Q.is_empty

    c = -1
    Q = Quadric(A=A, b=b, c=c)
    assert not Q.is_empty

    Q.plot(show=SHOW)

    A = np.array([[0, 0], [0, 1]])
    b = np.array([0, 0])
    c = -1
    Q = Quadric(A=A, b=b, c=c)
    Q.plot(show=SHOW)


def test_single_point():
    A = np.array([[4]])
    b = np.array([12])

    c = 9
    Q = Quadric(A=A, b=b, c=c)
    assert not Q.is_empty
    assert Q.sol_R == Q.sol_L
    assert Q.sol_R == -3 / 2

    Q.plot(show=SHOW)


def test_single_line():
    A = np.array([[1, 0], [0, 0]])
    b = np.array([-2, 0])

    c = 1
    Q = Quadric(A=A, b=b, c=c)
    assert not Q.is_empty

    Q.plot(show=SHOW)


def test_single_plane():
    A = np.array([[1, 0, 0], [0, 0, 0], [0, 0, 0]])
    b = np.array([-2, 0, 0])

    c = 1
    Q = Quadric(A=A, b=b, c=c)

    assert Q.is_single_plane
    Q.plot(show=SHOW)


def test_single_plane_rotated():
    A = np.array([[1, 0, 0], [0, 0, 0], [0, 0, 0]])
    b = np.array([-2, 0, 0])

    V = ortho_group.rvs(3)

    A2 = V @ A @ V.T
    b2 = V @ b

    c = 1
    Q = Quadric(A=A2, b=b2, c=c)

    assert Q.is_single_plane
    Q.plot(show=SHOW)


def test_parallel_planes():
    A = np.array([[0, 0, 0], [0, -2, 0], [0, 0, 0]])
    b = np.array([0, 0, 0])

    c = 1
    Q = Quadric(A=A, b=b, c=c)

    assert Q.is_parallel_planes
    Q.plot(show=SHOW)


def test_is_paraboloid_cylinder():
    A = np.array([[1, 0, 0], [0, 0, 0], [0, 0, 0]])
    b = np.array([0, -1, 1])
    c = -1
    Q = Quadric(A=A, b=b, c=c)
    assert Q.is_paraboloid_cylinder
    assert Q.is_feasible(np.array([0, 1 , 2]))
    if SHOW:
        fig, ax = Q.plot(show=False)
        ax.scatter(0, 1, 2, color="r")
        plt.show()


def test_paraboloid():
    param = {}
    param['A'] = np.array([[1, 0, 0], [0, -2, 0], [0, 0, 0]]) / 1
    param['b'] = np.array([0, 0, 1])
    param['c'] = -1.5
    Q = Quadric(**param)
    assert Q.is_paraboloid
    Q.plot(show=SHOW, show_principal_axes=True)


def test_paraboloid_cylinder():
    param = {}
    param['A'] = np.array([[1, 0, 0], [0, 0, 0], [0, 0, 0]])
    param['b'] = np.array([0, 2, 0])
    param['c'] = -2
    Q = Quadric(**param)
    assert Q.is_paraboloid_cylinder
    Q.plot(show=SHOW)


def test_elliptic_cone():
    param = {}
    param['A'] = np.array([[4, 0, 0], [0, -2, 0], [0, 0, 10]])
    param['b'] = np.array([0, 0, 0])
    param['c'] = 0
    Q = Quadric(**param)
    Q.plot(show=SHOW)
    assert Q.is_elliptic_cone
