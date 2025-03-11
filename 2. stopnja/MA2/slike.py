
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



for n in range(20, 10000, 150):
    m = int(n)
    fig1, ax1 = plt.subplots(tight_layout=True)

    try:
        A = preberi("./datoteke/fraktali04_{m}.dat")
        bji = A[0]
        phiji = A[1]
        ax1.scatter(bji, phiji, color="C0", s=1)
        print(bji)
        # ax1.axis("equal")
        # ax1.set(xlim=(-5, 5), ylim=(-5, 5))
        ax1.set_xlabel("$b$")
        ax1.set_ylabel("$\phi$")
        #plt.tight_layout()
        #fig1.savefig(f"./slike/fraktali1_{8593}.png")
        fig1.savefig("./slike/fraktaliaaa04_{m}.png")
        plt.close('all')
    except:
        plt.close('all')

#plt.show()