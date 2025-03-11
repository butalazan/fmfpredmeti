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


def pocisti(imedat):
    file1 = open(imedat, "w")
    file1.close()

def dodaj(tabela, imedat):
    file1 = open(imedat, "a")  # append mode: Append-adds after last row
    for i in range(len(tabela)):
        file1.write(str(tabela[i]))
        file1.write("   ")
    file1.writelines("\n")

    file1.close()

def preberi(imedat, numpyarrize=False):
    b = []
    with open(imedat) as file:
        for line in file:
            a = line.rstrip().split()
            if len(a) == 1:
                b.append(a[0])
            else:
                b.append([float(i) for i in a])
    if numpyarrize == True: return np.array(b)
    else: return b

def preberi_u(imedat, N):
    with open(imedat) as file:
        a = str()
        for line in file:
            a += line

    a = a.replace("[", "")
    b = a.replace("]", "").split()

    shape = len(b)//N**2
    c = np.array([np.zeros((N,N))] * shape)
    #print("shape c", c.shape)
    for i in range(len(b)//(N**2)):
        for j in range(N):
            for k in range(N):
                c[i][j][k] = float(b[i*N*N + j*N + k])
            
    return c

def zaokrozi(num):                     # rounds to 3 non-trivial digits
    if num%1 == 0: return num
    working = str(num-int(num))
    for i, e in enumerate(working[2:]):
        if e != '0':
            return int(num) + float(working[:i+5])

def nth(nums, nti):
    # a function that returns every nth element from a list.
    # Use list slicing to return elements starting from the (nth-1) index, with a step of 'nth'.
    return nums[nti - 1::nti]

#dodaj(np.linspace(0, 10*M*dt, 10*M-4), f"koords_N{N}")
#dodaj(X, f"koords_N{N}")
#np.savetxt(f'bic_koords_{poskus}1_N{N}.dat', np.column_stack((np.linspace(0, 10*M*dt, 10*M), X,Y)))

#fig, ax = plt.subplots(figsize=(6,4.5))
#ax.plot(N15adv[0], np.absolute((N15adv[3]-N15adv[3][0]*np.ones(len(N15adv[3])))/N15adv[3][0]), label="$dt = 0.1$")
#ax.set_title("Relativno odstopanje abs. energije")
#ax.set_xlabel("$t$")
#ax.set_ylabel("$\Delta E/E$")
#ax.set_yscale("log")
#ax.set_ylim(1E-7, 1E+4)
#ax.legend()
#igd.tight_layout()
#figd.savefig(f"./slike/energija_stabil1.png")

# ___________________________________________________________________________________________________________________

M=1

def U(x,y):
    return x**2*y**2*exp(-x**2 - y**2)

def RU(x,y,phi,a=0,b=0):
    R = [[cos(phi),sin(phi)],[-sin(phi),cos(phi)]]
    A = np.zeros((len(y),len(x)))
    for i in range(len(x)):
        for j in range(len(y)):
            x1, y1 = np.dot(R, [x[j]-a, y[i]-b])
            #x1, y1 = np.dot(R, [x[j], y[i]])
            #x1, y1 = x1-a, y1-b
            A[i][j] = x1**2*y1**2 * np.exp(-(x1**2+y1**2))
            #A[i][j] = x1*y1 * np.exp(-(x1**2+y1**2))
    return A

def interakcija(zz,t):
    x, y, u, v, phi, omega = zz

    # phi=pi/4
    R = [[cos(phi),sin(phi)],[-sin(phi),cos(phi)]]
    x1, y1 = np.dot(R, [x, y])
    dxdt = u
    dydt = v
    dudt = 2*x1*y1**2*exp(-x1**2-y1**2) * (-1 + x1**2)
    dvdt = 2*x1**2*y1*exp(-x1**2-y1**2) * (-1 + y1**2)
    dphidt = 0
    domegadt = 0

    dzdt = [dxdt, dydt, dudt, dvdt, dphidt, domegadt]
    return dzdt


def interakcija_z(zz,t):
    x, y, u, v, aa, bb, AA, BB, phi, omega = zz

    # phi=pi/4
    R = [[cos(phi),sin(phi)],[-sin(phi),cos(phi)]]
    x1, y1 = np.dot(R, [x-aa, y-bb])
    
    dxdt = u
    dydt = v
    dudt = 2*x1*y1**2*exp(-x1**2-y1**2) * (-1 + x1**2)
    dvdt = 2*x1**2*y1*exp(-x1**2-y1**2) * (-1 + y1**2)

    dadt = AA
    dbdt = BB
    dAdt = 2*x1*y1**2*exp(-x1**2-y1**2) * (1 - x1**2) / M
    dBdt = 2*x1**2*y1*exp(-x1**2-y1**2) * (1 - y1**2) / M

    dphidt = 0
    #domegadt = (2*x1**3*y1*exp(-1+y1**2) * (1 - y1**2)  -  2*x1*y1**3*exp(-1+x1**2) * (1 - y1**2)) / (3/4*np.pi*M)
    domegadt = 0

    dzdt = [dxdt, dydt, dudt, dvdt, dadt, dbdt, dAdt, dBdt, dphidt, domegadt]
    return dzdt


def interakcija_w(zz,t):
    x, y, u, v, aa, bb, AA, BB, phi, omega = zz

    # phi=pi/4
    R = [[cos(phi),sin(phi)],[-sin(phi),cos(phi)]]
    x1, y1 = np.dot(R, [x, y])
    
    dxdt = u
    dydt = v
    dudt = 2*x1*y1**2*exp(-x1**2-y1**2) * (-1 + x1**2)
    dvdt = 2*x1**2*y1*exp(-x1**2-y1**2) * (-1 + y1**2)

    dadt = AA
    dbdt = BB
    dAdt = 0
    dBdt = 0

    dphidt = omega
    domegadt = -(2*x1**3*y1*exp(-x1**2-y1**2) * (-1 + y1**2)  -  2*x1*y1**3*exp(-x1**2-y1**2) * (-1 + x1**2)) / (3/4*np.pi*M)

    dzdt = [dxdt, dydt, dudt, dvdt, dadt, dbdt, dAdt, dBdt, dphidt, domegadt]
    return dzdt

def interakcija_zw(zz,t):
    x, y, u, v, aa, bb, AA, BB, phi, omega = zz

    # phi=pi/4
    R = [[cos(phi),sin(phi)],[-sin(phi),cos(phi)]]
    x1, y1 = np.dot(R, [x-aa, y-bb])
    
    dxdt = u
    dydt = v
    dudt = 2*x1*y1**2*exp(-x1**2-y1**2) * (-1 + x1**2)
    dvdt = 2*x1**2*y1*exp(-x1**2-y1**2) * (-1 + y1**2)

    dadt = AA
    dbdt = BB
    dAdt = 2*x1*y1**2*exp(-x1**2-y1**2) * (1 - x1**2) / M
    dBdt = 2*x1**2*y1*exp(-x1**2-y1**2) * (1 - y1**2) / M

    dphidt = omega
    domegadt = -(2*x1**3*y1*exp(-x1**2-y1**2) * (-1 + y1**2)  -  2*x1*y1**3*exp(-x1**2-y1**2) * (-1 + x1**2)) / (3/4*np.pi*M)

    dzdt = [dxdt, dydt, dudt, dvdt, dadt, dbdt, dAdt, dBdt, dphidt, domegadt]
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
    phi = np.empty_like(t)
    omega = np.empty_like(t)

    x[0] = z0[0]
    y[0] = z0[1]
    vx[0] = z0[2]
    vy[0] = z0[3]
    phi[0] = z0[4]
    omega[0] = z0[5]

    # solve ODE
    for i in range(1,n):
        # span for next time step
        tspan = [t[i-1],t[i]]
        # solve for next step
        # z = odeint(model,z0,tspan,args=(u[i],))             # z parametrom u
        z = odeint(interakcija,z0,tspan)
        # store solution for plotting
        x[i] = z[1][0]
        y[i] = z[1][1]
        vx[i] = z[1][2]
        vy[i] = z[1][3]
        phi[i] = z[1][4]
        omega[i] = z[1][5]
        # next initial condition
        z0 = z[1]

    return x,y,vx,vy,phi,omega


def odeintegrator_z(z0):
    u = np.zeros(n)

    x = np.empty_like(t)
    y = np.empty_like(t)
    vx = np.empty_like(t)
    vy = np.empty_like(t)
    a = np.empty_like(t)
    b = np.empty_like(t)
    va = np.empty_like(t)
    vb = np.empty_like(t)
    phi = np.empty_like(t)
    omega = np.empty_like(t)

    x[0] = z0[0]
    y[0] = z0[1]
    vx[0] = z0[2]
    vy[0] = z0[3]
    a[0] = z0[4]
    b[0] = z0[5]
    va[0] = z0[6]
    vb[0] = z0[7]
    phi[0] = z0[8]
    omega[0] = z0[9]

    # solve ODE
    for i in range(1,n):
        # span for next time step
        tspan = [t[i-1],t[i]]
        # solve for next step
        # z = odeint(model,z0,tspan,args=(u[i],))             # z parametrom u
        z = odeint(interakcija_z,z0,tspan)
        # store solution for plotting
        x[i] = z[1][0]
        y[i] = z[1][1]
        vx[i] = z[1][2]
        vy[i] = z[1][3]
        a[i] = z[1][4]
        b[i] = z[1][5]
        va[i] = z[1][6]
        vb[i] = z[1][7]
        phi[i] = z[1][8]
        omega[i] = z[1][9]
        # next initial condition
        z0 = z[1]

    return x,y,vx,vy,a,b,va,vb,phi,omega


def odeintegrator_w(z0):
    u = np.zeros(n)

    x = np.empty_like(t)
    y = np.empty_like(t)
    vx = np.empty_like(t)
    vy = np.empty_like(t)
    a = np.empty_like(t)
    b = np.empty_like(t)
    va = np.empty_like(t)
    vb = np.empty_like(t)
    phi = np.empty_like(t)
    omega = np.empty_like(t)

    x[0] = z0[0]
    y[0] = z0[1]
    vx[0] = z0[2]
    vy[0] = z0[3]
    a[0] = z0[4]
    b[0] = z0[5]
    va[0] = z0[6]
    vb[0] = z0[7]
    phi[0] = z0[8]
    omega[0] = z0[9]

    # solve ODE
    for i in range(1,n):
        # span for next time step
        tspan = [t[i-1],t[i]]
        # solve for next step
        # z = odeint(model,z0,tspan,args=(u[i],))             # z parametrom u
        z = odeint(interakcija_w,z0,tspan)
        # store solution for plotting
        x[i] = z[1][0]
        y[i] = z[1][1]
        vx[i] = z[1][2]
        vy[i] = z[1][3]
        a[i] = z[1][4]
        b[i] = z[1][5]
        va[i] = z[1][6]
        vb[i] = z[1][7]
        phi[i] = z[1][8]
        omega[i] = z[1][9]
        # next initial condition
        z0 = z[1]

    return x,y,vx,vy,a,b,va,vb,phi,omega


def odeintegrator_zw(z0):
    u = np.zeros(n)

    x = np.empty_like(t)
    y = np.empty_like(t)
    vx = np.empty_like(t)
    vy = np.empty_like(t)
    a = np.empty_like(t)
    b = np.empty_like(t)
    va = np.empty_like(t)
    vb = np.empty_like(t)
    phi = np.empty_like(t)
    omega = np.empty_like(t)

    x[0] = z0[0]
    y[0] = z0[1]
    vx[0] = z0[2]
    vy[0] = z0[3]
    a[0] = z0[4]
    b[0] = z0[5]
    va[0] = z0[6]
    vb[0] = z0[7]
    phi[0] = z0[8]
    omega[0] = z0[9]

    # solve ODE
    for i in range(1,n):
        # span for next time step
        tspan = [t[i-1],t[i]]
        # solve for next step
        # z = odeint(model,z0,tspan,args=(u[i],))             # z parametrom u
        z = odeint(interakcija_zw,z0,tspan)
        # store solution for plotting
        x[i] = z[1][0]
        y[i] = z[1][1]
        vx[i] = z[1][2]
        vy[i] = z[1][3]
        a[i] = z[1][4]
        b[i] = z[1][5]
        va[i] = z[1][6]
        vb[i] = z[1][7]
        phi[i] = z[1][8]
        omega[i] = z[1][9]
        # next initial condition
        z0 = z[1]

    return x,y,vx,vy,a,b,va,vb,phi,omega


def kot(resitev):
    x,y,u,v,phi,omega = resitev
    tan = (y[-1]-y[-2])/(x[-1]-x[-2])
    phi = np.arctan2(y[-1]-y[-2],x[-1]-x[-2])
    return phi







x,y = np.linspace(-10,10,1000), np.linspace(-10,10,1000)
A = np.zeros((1000,1000))





#fig1, ax1 = plt.subplots(tight_layout=True)
#from matplotlib.lines import Line2D
#
#custom_lines = [Line2D([0], [0], color="C0", lw=1.8),
#                Line2D([0], [0], color="C1", lw=1.8)]
#
#ax1.legend(custom_lines, [r'$\varphi = 0$', r'$\varphi = \pi/8$'])
#
#x,y = np.linspace(-10,10,500), np.linspace(-10,10,500)
#X,Y = np.meshgrid(x,y)
#Z = RU(x,y,0)
#CS = ax1.contour(X, Y, Z, 10, linewidths=0.6, colors="C0", label="$\varphi = 0$")
#Z = RU(x,y,pi/8)
#CS = ax1.contour(X, Y, Z, 10, linewidths=0.6, colors="C1", label="$\varphi = \pi/8$")
## Z = RU(x,y,pi/4)
## CS = ax1.contour(X, Y, Z, 10, linewidths=0.6, colors="grey")
#ax1.axis("equal")
#ax1.set(xlim=(-5, 5), ylim=(-5, 5))
#ax1.set_xlabel("$x$")
#ax1.set_ylabel("$y$")
#fig1.tight_layout()
#





plt.rcParams['font.size'] = 10



n = 200
t = np.linspace(0,70,n)


sol_odeint = odeintegrator([-10, 1, 0.3, 0., 0.8, 0])
sol_odeint_z = odeintegrator_z([-10, 1, 0.3, 0., 0, 0, 0, 0, 0.8, 0])




fig1, ax1 = plt.subplots(tight_layout=True)
x,y = np.linspace(-10,10,500), np.linspace(-10,10,500)
X,Y = np.meshgrid(x,y)
Z = RU(x,y,0.8)
CS = ax1.contour(X, Y, Z, 10, linewidths=0.6, colors="C1", label="$\varphi = 0$")
ax1.plot(sol_odeint[0], sol_odeint[1], "--", color="grey")
ax1.plot(sol_odeint_z[0], sol_odeint_z[1])
ax1.scatter(sol_odeint_z[4], sol_odeint_z[5], color="C1")
ax1.axis("equal")
ax1.set(xlim=(-5, 5), ylim=(-5, 5))
ax1.set_xlabel("$x$")
ax1.set_ylabel("$y$")



sol_odeint = odeintegrator([-10, 1, 0.3, 0., 0.0, 0])
sol_odeint_w = odeintegrator_w([-10, 1, 0.3, 0., 0, 0, 0, 0, 0., 0])




fig2, ax2 = plt.subplots(tight_layout=True)
x,y = np.linspace(-10,10,500), np.linspace(-10,10,500)
X,Y = np.meshgrid(x,y)
Z = RU(x,y,0.)
CS = ax2.contour(X, Y, Z, 10, linewidths=0.6, colors="C1", label="$\varphi = 0$")
ax2.plot(sol_odeint[0], sol_odeint[1], "--", color="grey")
ax2.plot(sol_odeint_w[0], sol_odeint_w[1])
ax2.scatter(sol_odeint_w[4], sol_odeint_w[5], color="C1")
ax2.axis("equal")
ax2.set(xlim=(-5, 5), ylim=(-5, 5))
ax2.set_xlabel("$x$")
ax2.set_ylabel("$y$")



#from matplotlib import animation
#from matplotlib.animation import FuncAnimation  
#
#fig = plt.figure()  
#   
## marking the x-axis and y-axis 
#axis = plt.axes(xlim =(-5,5),  
#                ylim =(-5,5))  
#  
## initializing a line variable 
#line, = axis.plot([], [], lw = 3)  
#   
## data which the line will  
## contain (x, y) 
#def init():  
#    line.set_data([], []) 
#    return line, 
#   
#def animate(i): 
#    x = sol_odeint_w[0][:i]
#    y = sol_odeint_w[1][:i]
#    line.set_data(x, y) 
#      
#    return line, 
#   
#anim = FuncAnimation(fig, animate, init_func = init, frames = len(t), interval = 20, blit = True) 
#
##anim.save('test1.mp4', writer = 'ffmpeg', fps = 30) 
#
#writergif = animation.PillowWriter(fps=30)
#anim.save('filename.gif',writer=writergif)


M=5
sol_odeint_w = odeintegrator_w([-10, 0.8, 0.8, 0., 0, 0, 0, 0, 0., 0])


fig3, ax3 = plt.subplots(tight_layout=True)
x,y = np.linspace(-10,10,500), np.linspace(-10,10,500)
X,Y = np.meshgrid(x,y)
for j in range(20,len(t),2):
    fig3, ax3 = plt.subplots(tight_layout=True)
    #Z = RU(x-sol_odeint_w[4][j],y-sol_odeint_w[5][j],sol_odeint_w[8][j])
    Z = RU(x,y,sol_odeint_w[8][j], sol_odeint_w[4][j], sol_odeint_w[5][j])
    CS = ax3.contour(X, Y, Z, 10, linewidths=0.6, colors="C1", label="$\varphi = 0$")
    ax3.plot(sol_odeint_w[0][:j], sol_odeint_w[1][:j], label=f"$v_0={sol_odeint_w[2][0]}$")
    ax3.scatter(sol_odeint_w[4][:j], sol_odeint_w[5][:j], color="C1", s=4, label=f"$m/M = {round(1/M,1)}$")
    ax3.axis("equal")
    ax3.set(xlim=(-5, 5), ylim=(-5, 5))
    ax3.set_xlabel("$x$")
    ax3.set_ylabel("$y$")
    ax3.legend()
    #ax3.set_title("Translacijski odriv")
    ax3.set_title("Rotacijski odriv")
    #ax3.set_title("Poln odriv")
    fig3.savefig(f"./video/zasuk2_{1000+j}.png")