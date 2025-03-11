
import matplotlib.pyplot as plt
import numpy as np
import scipy
from scipy import optimize
import pandas as pd
import math
import random
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
epsilon = 1E-4

print(random.randint(0,1))

fig1, ax1 = plt.subplots(tight_layout=True)

bji = np.linspace(-2,2,200)
phiji, phiji_ref = np.zeros(len(bji)), np.zeros(len(bji))
for a in range(len(bji)):

    delta = epsilon*(2*random.randint(0,1)-1)
    sol_ref = odeintegrator([-10, bji[a], 0.3, 0.])
    sol_odeint = odeintegrator([-10, bji[a]+delta, 0.3, 0.])
    phiji_ref[a] = kot(sol_ref)
    phiji[a] = kot(sol_odeint)
    # if a%50==0:
    #     plt.plot(sol_odeint[0], sol_odeint[1])
    #     plt.axis("equal")
    #     plt.show()
    dodaj([bji[a], phiji[a]], f"./datoteke/ljapunov1_{len(bji)}.dat")

ax1.scatter(bji, phiji, color="black", s=1)

# ax1.axis("equal")
# ax1.set(xlim=(-5, 5), ylim=(-5, 5))
ax1.set_title("$E_0={0:.3f}$".format(1/2*sol_odeint[2][0]**2))
ax1.set_xlabel("$b$")
ax1.set_ylabel("$\phi$")
plt.tight_layout()
#plt.show()










# Only 1 ball is used!
maxSteps = 7000 # of steps of ball motion (in constant speed)

n = 1 # of circular obstacles

# create circular obstacle
cxList = []
cyList = []
crList = []
for i in range(n):
    while(True): # circle(s) must not overlap
        cr = 3/8 # circle radius
        cx = 1/2 # circle center x
        cy = 1/2 # circle center y
        flag = True
        if i > 0:
            for j in range(i):
                if math.hypot(cx - cxList[j], cy - cyList[j]) < cr + crList[j]:
                    flag = False
                    break
        if flag == True:
            break
    #draw.ellipse((cx - cr, cy - cr, cx + cr, cy + cr))
    cxList.append(cx)
    cyList.append(cy)
    crList.append(cr)




X,Y = [], []
S, C = [],[]
# initial location of the ball must be outside of the circle(s)
while(True):
    x = float(random.uniform(0, 1))
    y = float(random.uniform(0, 1))
    flag = False
    for i in range(n):
        if math.hypot(x - cxList[i], y - cyList[i]) <= crList[i]:
            flag = True
            break
    if flag == False:
        break
X.append(x)
Y.append(y)
    
# initial direction of the ball
a = 2.0 * math.pi * random.random()
s = math.sin(a)
c = math.cos(a)
S.append(s)
C.append(c)


dt = 0.001
for i in range(maxSteps):
    #image.putpixel((int(x), int(y)), (255, 255, 255))
    xnew = x + c*dt
    ynew = y + s*dt

    # reflection from the walls
    if xnew < 0 or xnew > 1:
        c = -c
        xnew = x
    if ynew < 0 or ynew > 1:
        s = -s
        ynew = y

    # reflection from the circle(s)
    for i in range(n):
        if math.hypot(xnew - cxList[i], ynew - cyList[i]) <= crList[i]:
            # angle of the circle point
            ca = math.atan2(ynew - cyList[i], xnew - cxList[i])
            # reversed collision angle of the ball
            rca = math.atan2(-s, -c)
            # reflection angle of the ball
            rab = rca + (ca - rca) * 2
            s = math.sin(rab)
            c = math.cos(rab)
            xnew = x
            ynew = y

    x = xnew
    y = ynew
    X.append(x)
    Y.append(y)
    S.append(s)
    C.append(c)






X1,Y1 = [], []
S1, C1 = [],[]
Dx, Dy, D = [], [], []
# initial location of the bližnje trajektorije
epsilon = 1E-4
while(True):
    b = 2.0 * math.pi * random.random()
    x = X[0] + epsilon*np.cos(b)
    y = Y[0] + epsilon*np.sin(b)
    flag = False
    for i in range(n):
        if math.hypot(x - cxList[i], y - cyList[i]) <= crList[i]:
            flag = True
            break
    if flag == False:
        break
    
# initial direction of the ball
s = S[0]
c = C[0]
S1.append(s)
C1.append(c)
Dx.append(epsilon*np.cos(b))
Dy.append(epsilon*np.sin(b))
D.append(epsilon)

eta = 5*1E-2
dt = 0.001
for i in range(maxSteps):
    xnew = x + c*dt
    ynew = y + s*dt

    if (xnew-X[i])**2 + (ynew-Y[i])**2 > eta**2:
            dx, dy = abs(xnew-X[i]), abs(ynew-Y[i])
            d = np.sqrt((xnew-X[i])**2 + (ynew-Y[i])**2)
            xnew = X[i] + epsilon/d*(xnew - X[i])
            ynew = Y[i] + epsilon/d*(ynew - Y[i])
            c = C[i]
            s = S[i]
            Dx.append(dx)
            Dy.append(dy)
            D.append(d)


    # reflection from the walls
    if xnew < 0 or xnew > 1:
        c = -c
        xnew = x
    if ynew < 0 or ynew > 1:
        s = -s
        ynew = y

    # reflection from the circle(s)
    for i in range(n):
        if math.hypot(xnew - cxList[i], ynew - cyList[i]) <= crList[i]:
            # angle of the circle point
            ca = math.atan2(ynew - cyList[i], xnew - cxList[i])
            # reversed collision angle of the ball
            rca = math.atan2(-s, -c)
            # reflection angle of the ball
            rab = rca + (ca - rca) * 2
            s = math.sin(rab)
            c = math.cos(rab)
            xnew = x
            ynew = y

    x = xnew
    y = ynew
    X1.append(x)
    Y1.append(y)
    S1.append(s)
    C1.append(c)




    
fig, ax = plt.subplots()

ax.plot(X,Y, color="C0")
ax.scatter(X[0],Y[0], color="C0")
ax.plot(X1,Y1, color="C1")
N= 100
circle = [1/2+ 3/8*np.cos(2*np.pi/N*i) for i in range(N+1)], [1/2+3/8*np.sin(2*np.pi/N*i) for i in range(N+1)]
ax.plot(circle[0], circle[1], color="black")
ax.plot([0,1,1,0,0], [0,0,1,1,0], color="black")
ax.set_xlabel("$x$")
ax.set_ylabel("$y$")
ax.set_aspect(1)
fig.tight_layout()
plt.show()