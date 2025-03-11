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

def round(num):                     # rounds to 3 non-trivial digits
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


@jit(target_backend='cuda')
def U(x,y):
    return x**2*y**2*exp(-x**2 - y**2)

@jit(target_backend='cuda')
def interakcija(zz,t):
    x, y, u, v = zz
    dxdt = u
    dydt = v
    dudt = 2*x*y**2*exp(-x**2-y**2) * (-1 + x**2)
    dvdt = 2*x**2*y*exp(-x**2-y**2) * (-1 + y**2)

    dzdt = [dxdt, dydt, dudt, dvdt]
    return dzdt

@jit(target_backend='cuda')
def presecisce(r1, r2):
    x1,y1 = r1
    x2,y2 = r2
    return (y2-y1)/(x2/x1 + 1) + y1

@jit(target_backend='cuda')
def E(r,rpika):
    x,y = r
    u,v = rpika

    # print("E: ", 1/2*(u**2+v**2) + U(x,y), 1/6)
    return 1/2*(u**2+v**2) + U(x,y)

#@jit(target_backend='cuda')
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
        z = odeint(interakcija,z0,tspan)
        # store solution for plotting
        x[i] = z[1][0]
        y[i] = z[1][1]
        vx[i] = z[1][2]
        vy[i] = z[1][3]
        # next initial condition
        z0 = z[1]
    return x,y,vx,vy

@jit(target_backend='cuda')
def kot(resitev):
    x,y,u,v = resitev
    tan = (y[-1]-y[-2])/(x[-1]-x[-2])
    phi = np.arctan2(y[-1]-y[-2],x[-1]-x[-2])
    return phi

n = 1000
t = np.linspace(0,50,n)


#fig1, ax1 = plt.subplots(tight_layout=True)
#
#bji = np.linspace(-2,2,200)
#phiji = np.zeros(len(bji))
#for a in range(len(bji)):
#
#    sol_odeint = odeintegrator([-10, bji[a], 0.3, 0.])
#    phiji[a] = kot(sol_odeint)
#    # if a%50==0:
#    #     plt.plot(sol_odeint[0], sol_odeint[1])
#    #     plt.axis("equal")
#    #     plt.show()
#    #dodaj([bji[a], phiji[a]], f"./datoteke/fraktali1_{len(bji)}.dat")
#
#ax1.scatter(bji, phiji, color="black", s=1)
#
## ax1.axis("equal")
## ax1.set(xlim=(-5, 5), ylim=(-5, 5))
#ax1.set_title("$E_0={0:.3f}$".format(1/2*sol_odeint[2][0]**2))
#ax1.set_xlabel("$b$")
#ax1.set_ylabel("$\phi$")
#plt.tight_layout()
##plt.show()
#
#
#
#
#fig1, ax1 = plt.subplots(tight_layout=True)
#
#bji = np.linspace(0.32,0.582,100)
#bji = np.linspace(0.3,2.60,10)
#phiji = np.zeros(len(bji))
#for a in range(len(bji)):
#
#    sol_odeint = odeintegrator([-10, bji[a], 0.3, 0.])
#    phiji[a] = kot(sol_odeint)
#    # if a%50==0:
#    #plt.plot(sol_odeint[0], sol_odeint[1])
#    #plt.title("$\phi = {0:.2f}$".format(kot(sol_odeint)))
#    #plt.axis("equal")
#    #plt.show()
#    #dodaj([bji[a], phiji[a]], f"./datoteke/fraktali1_{len(bji)}.dat")
#
#ax1.scatter(bji, phiji, color="black", s=0.5)
#
##dodaj(bji, "./datoteke/fraktali1.dat")
##dodaj(phiji, "./datoteke/fraktali1.dat")
#
## ax1.axis("equal")
## ax1.set(xlim=(-5, 5), ylim=(-5, 5))
#ax1.set_title("$E_0={0:.3f}$".format(1/2*sol_odeint[2][0]**2))
#ax1.set_xlabel("$b$")
#ax1.set_ylabel("$\phi$")
#plt.tight_layout()
#










v0 = "04"


Kji = np.linspace(20,10000,150)
#for K in range(20,10000,25):
for K in Kji:
    if K>1:
        print(int(K))

        bji = np.linspace(-2,2,int(K))
        phiji = np.zeros(len(bji))
        pocisti(f"./datoteke/sols" + v0 + f"_{len(bji)}.dat")
        pocisti(f"./datoteke/fraktali" + v0 + f"_{len(bji)}.dat")

        for a in range(len(bji)):

            sol_odeint = odeintegrator([-10, bji[a], 0.4, 0.])
            phiji[a] = kot(sol_odeint)

            dodaj(sol_odeint[0], f"./datoteke/sols" + v0 + f"_{len(bji)}.dat")
            dodaj(sol_odeint[1], f"./datoteke/sols" + v0 + f"_{len(bji)}.dat")
            dodaj([bji[a], phiji[a], bji[1]-bji[0]], f"./datoteke/fraktali" + v0 + f"_{len(bji)}.dat")

            
        


plt.show()
