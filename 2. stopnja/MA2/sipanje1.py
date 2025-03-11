import matplotlib.pyplot as plt
import numpy as np
import scipy
from scipy import optimize
import pandas as pd
# import scipy.optimize._linprog as lin
# from scipy.optimize import optimize
# import copy
# import decimal as dec
# from matplotlib import cm, colors
# from mpl_toolkits.mplot3d import Axes3D
from scipy.integrate import odeint
# from matplotlib.colors import LogNorm
# from numba import jit
# from time import time
# import statistics as stat
import sys
import mpmath
from numba import jit
from scipy.integrate import solve_ivp
from numpy import cos, sin, pi, exp


def U(x,y):
    return x**2*y**2*exp(-x**2 - y**2)

def henon1(t, zz):
    x, y, u, v = zz
    dxdt = u
    dydt = v
    dudt = 2*x*y**2*exp(-x**2-y**2) * (-1 + x**2)
    dvdt = 2*x**2*y*exp(-x**2-y**2) * (-1 + y**2)

    dzdt = [dxdt, dydt, dudt, dvdt]
    return dzdt

def henon2(zz,t):
    x, y, u, v = zz
    dxdt = u
    dydt = v
    dudt = 2*x*y**2*exp(-x**2-y**2) * (-1 + x**2)
    dvdt = 2*x**2*y*exp(-x**2-y**2) * (-1 + y**2)

    dzdt = [dxdt, dydt, dudt, dvdt]
    return dzdt

def presecisce(r1, r2):
    x1,y1 = r1
    x2,y2 = r2
    return (y2-y1)/(x2/x1 + 1) + y1

def E(r,rpika):
    x,y = r
    u,v = rpika

    # print("E: ", 1/2*(u**2+v**2) + U(x,y), 1/6)
    return 1/2*(u**2+v**2) + U(x,y)

def odeintegrator(z0):
    u = np.zeros(n)

    x = np.empty_like(t)
    y = np.empty_like(t)
    vx = np.empty_like(t)
    vy = np.empty_like(t)

    x[0] = z0[0]
    y[0] = z0[1]
    vx[0] = z0[2]
    vy[0] = z0[3]

    # solve ODE
    for i in range(1,n):
        # span for next time step
        tspan = [t[i-1],t[i]]
        # solve for next step
        # z = odeint(model,z0,tspan,args=(u[i],))             # z parametrom u
        z = odeint(henon2,z0,tspan)
        # store solution for plotting
        x[i] = z[1][0]
        y[i] = z[1][1]
        vx[i] = z[1][2]
        vy[i] = z[1][3]
        # next initial condition
        z0 = z[1]
    return x,y,vx,vy


x,y = np.linspace(-10,10,1000), np.linspace(-10,10,1000)
A = np.zeros((1000,1000))
for i in range(1000):
    for j in range(1000):
        A[i][j] = x[j]**2*y[i]**2 * np.exp(-(x[j]**2+y[i]**2))

# plt.imshow(A)
# plt.show()

n = 1000
t = np.linspace(0,20,n)

sol_odeint = odeintegrator([-10, 0.5, 1, 0.])
sol_rk45 = solve_ivp(henon1, [t[0], t[-1]], [-10, 0.3, 1, 0.], t_eval=t, method="RK45").y


fig1, ax1 = plt.subplots(tight_layout=True)

ax1.plot(sol_rk45[0], sol_rk45[1])
ax1.plot(sol_odeint[0], sol_odeint[1])
x,y = np.linspace(-10,10,500), np.linspace(-10,10,500)
X,Y = np.meshgrid(x,y)
Z = U(X,Y)
CS = ax1.contour(X, Y, Z, 10, linewidths=0.6, colors="grey")
ax1.axis("equal")
ax1.set(xlim=(-5, 5), ylim=(-5, 5))
ax1.set_xlabel("$x$")
ax1.set_ylabel("$y$")
plt.tight_layout()
plt.show()


