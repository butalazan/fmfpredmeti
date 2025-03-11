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
from numba import jit, cuda
from scipy.integrate import solve_ivp
from numpy import cos, sin, pi, exp
import pylab as pl


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


def U(x,y):
    return x**2*y**2*exp(-x**2 - y**2)

def interakcija(zz,t):
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
        z = odeint(interakcija,z0,tspan)
        # store solution for plotting
        x[i] = z[1][0]
        y[i] = z[1][1]
        vx[i] = z[1][2]
        vy[i] = z[1][3]
        # next initial condition
        z0 = z[1]
    return x,y,vx,vy

def kot(resitev):
    x,y,u,v = resitev
    tan = (y[-1]-y[-2])/(x[-1]-x[-2])
    phi = np.arctan2(y[-1]-y[-2],x[-1]-x[-2])
    return phi

@jit(target_backend='cuda')
def hausdorff(bji, phiji):
    N, M = len(bji), len(phiji)
    dx, dy = (max(bji)-min(bji))/M, (max(phiji)-min(phiji))/N
    dx, dy = 4/M, 2*np.pi/N

    image = np.zeros((N,M))
    for i in range(N-1):
        for j in range(M-1):
            for k in range(len(bji)):
                if bji[k]>=-2+j*dx and bji[k]<-2+(j+1)*dx and phiji[k]>=-np.pi+i*dy and phiji[k]<-np.pi+(i+1)*dy:
                    image[i:,j] = 1


    # finding all the non-zero pixels
    pixels=[]
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            if image[i,j]>0:
                pixels.append((i,j))
    
    Lx=image.shape[1]
    Ly=image.shape[0]
    print(Lx, Ly)
    pixels=pl.array(pixels)
    print(pixels.shape)
    
    # computing the fractal dimension
    #considering only scales in a logarithmic list
    scales=np.logspace(0.01, 1, num=10, endpoint=False, base=2)
    Ns=[]
    # looping over several scales
    for scale in scales:
        print("======= Scale :",scale)
        # computing the histogram
        H, edges=np.histogramdd(pixels, bins=(np.arange(0,Lx,scale),np.arange(0,Ly,scale)))
        Ns.append(np.sum(H>0))
    
    # linear fit, polynomial of degree 1
    return np.polyfit(np.log(scales), 1.001*np.log(Ns), 1)




pl.rcParams['font.size'] = 10

#v0 = "10"
#
#switch = 0
#for st in np.linspace(20,10000,150):
#    switch += 1
#    print(int(st))
#    if switch%2==0 and st>0:
#        switch=0
#
#        fraktali1 = preberi(f"./datoteke/fraktali"+ v0 + f"_{int(st)}.dat", numpyarrize=True)
#        bji = fraktali1[:,0]
#        phiji = fraktali1[:,1]
#
#        
#        N, M = len(bji), len(phiji)
#        dx, dy = (max(bji)-min(bji))/M, (max(phiji)-min(phiji))/N
#        dx, dy = 4/M, 2*np.pi/N
#
#        image = np.zeros((N,M))
#        for i in range(N-1):
#            for j in range(M-1):
#                for k in range(len(bji)):
#                    if bji[k]>=-2+j*dx and bji[k]<-2+(j+1)*dx and phiji[k]>=-np.pi+i*dy and phiji[k]<-np.pi+(i+1)*dy:
#                        image[i:,j] = 1
#
#
#        # finding all the non-zero pixels
#        pixels=[]
#        for i in range(image.shape[0]):
#            for j in range(image.shape[1]):
#                if image[i,j]>0:
#                    pixels.append((i,j))
#        
#        Lx=image.shape[1]
#        Ly=image.shape[0]
#        print(Lx, Ly)
#        pixels=pl.array(pixels)
#        print(pixels.shape)
#        
#        # computing the fractal dimension
#        #considering only scales in a logarithmic list
#        scales=np.logspace(0.01, 1, num=10, endpoint=False, base=2)
#        Ns=[]
#        # looping over several scales
#        for scale in scales:
#            print("======= Scale :",scale)
#            # computing the histogram
#            H, edges=np.histogramdd(pixels, bins=(np.arange(0,Lx,scale),np.arange(0,Ly,scale)))
#            Ns.append(np.sum(H>0))
#        
#        # linear fit, polynomial of degree 1
#        coeffs=np.polyfit(np.log(scales), 1.001*np.log(Ns), 1)
#        #coeffs = hausdorff(bji, phiji)
#
#        
#        print ("The Hausdorff dimension is", -coeffs[0]) #the fractal dimension is the OPPOSITE of the fitting coefficient
#        dodaj([N, -coeffs[0]], f"./datoteke/hausdorf_scaling_final"+v0+".dat")



pl.figure(figsize=(6,4.5))
from scipy.optimize import curve_fit
def expo(x, a, b, c):
    return np.exp(a*x)*b+c

bji = np.linspace(0,2500, 100)

final = preberi("./datoteke/hausdorf_scaling_final04.dat", numpyarrize=True)
pl.scatter(final[:,0], final[:,1]/1.70, label=f"$E={round(0.3**2/2,2)}$")
pars, covs =  curve_fit(expo, final[:,0], final[:,1]/1.70, p0=[-0.1,-100,1])
pl.plot(bji, expo(bji, pars[0], pars[1], pars[2]), "--", label="$d_H ={0:.1f} \pm {1:.3f}$".format(pars[2], np.sqrt(covs[2][2])))
final = preberi("./datoteke/hausdorf_scaling_final.dat", numpyarrize=True)
pl.scatter(final[:,0], final[:,1]/1.70, label=f"$E={round(0.7**2/2,2)}$")
pars, covs =  curve_fit(expo, final[:,0], final[:,1]/1.70, p0=[-0.1,-50,1.2])
pl.plot(bji, expo(bji, pars[0], pars[1], pars[2]), "--", label="$d_H ={0:.1f} \pm {1:.3f}$".format(pars[2], np.sqrt(covs[2][2])))
final = preberi("./datoteke/hausdorf_scaling_final03.dat", numpyarrize=True)
pl.scatter(final[:,0], final[:,1]/1.9, label=f"$E={round(5**2/2,2)}$")
pars, covs =  curve_fit(expo, final[:,0], final[:,1]/1.9, p0=[-0.01,-80,1])
pl.plot(bji, expo(bji, pars[0], pars[1], pars[2]), "--", label="$d_H ={0:.2f} \pm {1:.3f}$".format(pars[2], np.sqrt(covs[2][2])))
final = preberi("./datoteke/hausdorf_scaling_final10.dat", numpyarrize=True)
pl.scatter(final[:,0], final[:,1]/1.9, label=f"$E={round(10**2/2,2)}$")
pars, covs =  curve_fit(expo, final[:,0], final[:,1]/1.9, p0=[-0.01,-80,1])
pl.plot(bji, expo(bji, pars[0], pars[1], pars[2]), "--", label="$d_H ={0:.2f} \pm {1:.3f}$".format(pars[2], np.sqrt(covs[2][2])))
pl.title(f"Hausdorffova dimenzija")
pl.xlabel('# točk parametra $b$')
pl.ylabel('$d_H$')
pl.legend()
pl.tight_layout()
pl.savefig(f'./slike/hausdorff_final111.png')


#final = preberi("./datoteke/hausdorf_scaling_final.dat", numpyarrize=True)
#pl.plot(final[:,0], final[:,1]/1.75, label=f"$E={round(0.3**2/2,2)}$")
#final = preberi("./datoteke/hausdorf_scaling_final04.dat", numpyarrize=True)
#pl.plot(final[:,0], final[:,1]/1.75, label=f"$E={round(0.7**2/2,2)}$")
#final = preberi("./datoteke/hausdorf_scaling_final03.dat", numpyarrize=True)
#pl.plot(final[:,0], final[:,1]/1.9, label=f"$E={round(5**2/2,2)}$")
#final = preberi("./datoteke/hausdorf_scaling_final10.dat", numpyarrize=True)
#pl.plot(final[:,0], final[:,1]/1.9, label=f"$E={round(10**2/2,2)}$")
#pl.title(f"Hausdorffova dimenzija")
#pl.xlabel('# točk parametra $b$')
#pl.ylabel('$d_H$')
#pl.legend()
#pl.tight_layout()
#pl.savefig(f'./slike/hausdorff_final222.png')








plt.show()
