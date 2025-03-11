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


def U(x,y):
    return 1/2*(x**2 + y**2)

def henon1(t, zz):
    x, y, u, v = zz
    dxdt = u
    dydt = v
    dudt = - x
    dvdt = - y

    dzdt = [dxdt, dydt, dudt, dvdt]
    return dzdt

def henon2(zz,t):
    x, y, u, v = zz
    dxdt = u
    dydt = v
    dudt = - x
    dvdt = - y

    dzdt = [dxdt, dydt, dudt, dvdt]
    return dzdt

def henon3(zz,t):
    x, y, u, v = zz
    dxdt = u
    dydt = v
    dudt = - x
    dvdt = - 1.01215111453896512*y

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

def odeintegrator3(z0):
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
        z = odeint(henon3,z0,tspan)
        # store solution for plotting
        x[i] = z[1][0]
        y[i] = z[1][1]
        vx[i] = z[1][2]
        vy[i] = z[1][3]
        # next initial condition
        z0 = z[1]
    return x,y,vx,vy


n = 3000
t = np.linspace(0,200,n)

sol_odeint = odeintegrator([0., 0.4, -0.3, 0.])
odeint3 = odeintegrator3([0., 0.4, -0.3, 0.])
# rk45 = solve_ivp(henon1, [t[0], t[-1]], [0., 0.4, -0.3, 0.], t_eval=t, method="RK45").y

plt.plot(sol_odeint[0], sol_odeint[1], label="$V(x,y)=x^2+y^2$", linewidth=1.5, zorder=2)
plt.plot(odeint3[0], odeint3[1], label="$V(x,y)=x^2+(1+\epsilon)y^2$",linewidth=0.8, zorder=0)
x,y = np.linspace(-0.8,0.8,200), np.linspace(-0.6,0.6,200)
X,Y = np.meshgrid(x,y)
Z = U(X,Y)
CS = plt.contour(X, Y, Z, 40, linewidths=0.4, colors="grey")
plt.axis("equal")
plt.title("Konfiguracijski")
plt.xlabel("$x$")
plt.ylabel("$y$")
plt.legend()
plt.figure()


n = 30000
t = np.linspace(0,3000,n)

sol_odeint = odeintegrator([0., 0.4, -0.3, 0.])
sol_rk45 = odeintegrator3([0., 0.4, -0.3, 0.])
# sol_rk45 = solve_ivp(henon1, [t[0], t[-1]], [0., 0.4, -0.3, 0.], t_eval=t, method="Radau").y

poiny1, poinv1 = [], []
for k in range(0, n - 2):
    if sol_odeint[0][k] * sol_odeint[0][k + 1] < 0:
        poiny1.append(sol_odeint[1][k])
        poinv1.append(sol_odeint[2][k])

plt.scatter(poiny1, poinv1, s=4, label="$V(x,y)=x^2+y^2$",zorder=1)


poiny2, poinv2 = [], []
for k in range(0, n - 2):
    if sol_rk45[0][k] * sol_rk45[0][k + 1] < 0:
        poiny2.append(sol_rk45[1][k])
        poinv2.append(sol_rk45[2][k])

plt.scatter(poiny2, poinv2, s=1.5, label="$V(x,y)=x^2+(1+\epsilon)y^2$", zorder=0)
plt.title("Poincare")
plt.xlabel("$v_x$")
plt.ylabel("$y$")
plt.legend()
plt.show()


