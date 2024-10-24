from quadproj import quadrics
from quadproj.project import project


import numpy as np


# creating random data
dim = 42
_A = np.random.rand(dim, dim)
A = _A + _A.T  # make sure that A is positive definite
b = np.random.rand(dim)
c = -1.42


param = {'A': A, 'b': b, 'c': c}
Q = quadrics.Quadric(**param)

x0 = np.random.rand(dim)
x_project = project(Q, x0)
assert Q.is_feasible(x_project), 'The projection is incorrect!'
from quadproj.project import plot_x0_x_project
from os.path import join

import pathlib


root_folder = pathlib.Path(__file__).resolve().parent.parent
output_folder = join(root_folder, 'output')

import matplotlib.pyplot as plt

show = False

A = np.array([[1, 0.1], [0.1, 2]])
b = np.zeros(2)
c = -1
Q = quadrics.Quadric(**{'A': A, 'b': b, 'c': c})

x0 = np.array([2, 1])
x_project = project(Q, x0)

fig, ax = Q.plot(show=show)
plot_x0_x_project(ax, Q, x0, x_project)
plt.savefig(join(output_folder, 'ellipse_no_circle.png'))
fig, ax = Q.plot()
plot_x0_x_project(ax, Q, x0, x_project, flag_circle=True)
fig.savefig(join(output_folder, 'ellipse_circle.png'))
if show:
    plt.show()
x0 = Q.to_non_standardized(np.array([0, 0.1]))
x_project = project(Q, x0)
fig, ax = Q.plot(show_principal_axes=True)
plot_x0_x_project(ax, Q, x0, x_project, flag_circle=True)
fig.savefig(join(output_folder, 'ellipse_degenerated.png'))
if show:
    plt.show()
A[0, 0] = -2
Q = quadrics.Quadric(**{'A': A, 'b': b, 'c': c})
x0 = Q.to_non_standardized(np.array([0, 0.1]))
x_project = project(Q, x0)
fig, ax = Q.plot(show_principal_axes=True)
plot_x0_x_project(ax, Q, x0, x_project, flag_circle=True)
fig.savefig(join(output_folder, 'hyperbola_degenerated.png'))
if show:
    plt.show()
dim = 3
A = np.eye(dim)
A[0, 0] = 2
A[1, 1] = 0.5

b = np.zeros(dim)
c = -1
param = {'A': A, 'b': b, 'c': c}
Q = quadrics.Quadric(**param)


fig, ax = Q.plot()

fig.savefig(join(output_folder, 'ellipsoid.png'))

Q.get_turning_gif(step=4, gif_path=join(output_folder, Q.type + '.gif'))


A[0, 0] = -4

param = {'A': A, 'b': b, 'c': c}
Q = quadrics.Quadric(**param)

x0 = np.array([0.1, 0.42, -1.5])

x_project = project(Q, x0)

fig, ax = Q.plot()
ax.grid(False)
ax.axis('off')
plot_x0_x_project(ax, Q, x0, x_project)
ax.get_legend().remove()

save_gif = True
if save_gif:
    quadrics.get_gif(fig, ax, elev=15, gif_path=join(output_folder, 'one_sheet_hyperboloid.gif'))
if show:
    plt.show()
fig, ax = Q.plot()
ax.grid(False)
ax.axis('off')
plot_x0_x_project(ax, Q, x0, x_project, flag_circle=True)
ax.get_legend().remove()

if save_gif: 
    quadrics.get_gif(fig, ax, elev=15, gif_path=join(output_folder, 'one_sheet_hyperboloid_ball.gif'))
A[0, 0] = 4
A[1, 1] = -2
A[2, 2] = -1

b = np.array([0.5, 1, -0.25])

c = -1

param = {'A': A, 'b': b, 'c': c}
Q = quadrics.Quadric(**param)

x0 = np.array([0.1, 0.42, -0.45])

x_project = project(Q, x0)

fig, ax = Q.plot()
ax.grid(False)
ax.axis('off')
plot_x0_x_project(ax, Q, x0, x_project)

if save_gif:
    quadrics.get_gif(fig, ax, gif_path=join(output_folder, 'two_sheet_hyperboloid.gif'))
if show:
    plt.show()
