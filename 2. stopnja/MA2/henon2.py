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
    return 1/2*(x**2 + y**2 + 2*x**2*y - 2/3*y**3)

def henon1(t, zz):
    x, y, u, v = zz
    dxdt = u
    dydt = v
    dudt = - x - 2*x*y
    dvdt = - y - x**2 + y**2

    dzdt = [dxdt, dydt, dudt, dvdt]
    return dzdt

def henon2(zz,t):
    x, y, u, v = zz
    dxdt = u
    dydt = v
    dudt = - x - 2*x*y
    dvdt = - y - x**2 + y**2

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

#
# n = 1000
# t = np.linspace(0,100,n)
#
# sol_odeint = odeintegrator([0., 0.3, -0.2, 0.])
# sol_rk45 = solve_ivp(henon1, [t[0], t[-1]], [0., 0.3, -0.2, 0.], t_eval=t, method="RK45").y
#
# plt.plot(sol_rk45[0], sol_rk45[1])
# plt.plot(sol_odeint[0], sol_odeint[1])
# plt.plot(np.linspace(0,0.8660254,10), np.linspace(1,-0.5,10), color="black")
# plt.plot(np.linspace(0.8660254,-0.8660254,10), np.linspace(-0.5,-0.5,10), color="black")
# plt.plot(np.linspace(-0.8660254,0,10), np.linspace(-0.5,1,10), color="black")
# x,y = np.linspace(-1.3,1.3,200), np.linspace(-0.7,1.2,200)
# X,Y = np.meshgrid(x,y)
# Z = U(X,Y)
# CS = plt.contour(X, Y, Z, 40, linewidths=0.6, colors="grey")
# plt.axis("equal")
# plt.show()


# ______________________________________________________________________________

n = 30000
t = np.linspace(0,3000,n)

for E0 in [0.01, 0.05, 0.1, 0.15]:
    E0=0.167

    counter = 0
    plt.figure()
    for j in range(500):

        y0, v0 = np.random.uniform(-0.11,0.11), np.random.uniform(-0.1,0.1)
        x0, u0 = 0, np.sqrt(2*abs(E0 - 1/2*v0**2 - U(0,y0)))

        if abs(E([x0,y0],[u0,v0])-E0)<0.01:
            counter += 1
            print(counter)
            if counter>50: break

            # sol = solve_ivp(henon, [t[0], t[-1]], [x0, y0, u0, v0], t_eval=t, method="RK45").y
            sol = odeintegrator([x0, y0, u0, v0])
            x, y, u, v = sol[0], sol[1], sol[2], sol[3]


            poiny, poinv = [], []
            for k in range(5, len(x)-2):
                if x[k] * x[k+1] < 0:
                    poiny.append(y[k])
                    poinv.append(v[k])

            plt.scatter(poiny, poinv, s=0.5, label="i={0}".format(j))
            print("i={0}, z=[\n {1} \n {2} \n {3} \n {4}\n]".format(j, x0, y0, u0, v0))

    plt.title("E={0}".format(E0))
    plt.xlabel("$y$")
    plt.ylabel("$v_y$")
    # plt.legend()
    plt.axis("equal")
    # plt.savefig("henon_poincare_{0}.png".format(E0*100+2))
    plt.show()


