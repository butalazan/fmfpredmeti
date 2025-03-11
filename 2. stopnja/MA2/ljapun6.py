import numpy as np
# Dynamical Billiards Simulation
# FB - 201010295
# See Wikipedia for more info:
# http://en.wikipedia.org/wiki/Dynamical_billiards
import math
import random
from PIL import Image, ImageDraw
from matplotlib import pyplot as plt




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




DT00 = preberi(f"./ljapun_razdalje1_r00.dat")
DT01 = preberi(f"./ljapun_razdalje1_r01.dat")
DT02 = preberi(f"./ljapun_razdalje1_r02.dat")
DT03 = preberi(f"./ljapun_razdalje1_r03.dat")


epsilon = 1E-4

def ljepunov(DD, TT):
    LJEP = []
    ljep = 0
    for i in range(len(DD)):
        ljep += np.log(DD[i]/epsilon)
        LJEP.append(ljep/TT[i])

    return LJEP

def avg(DD):
    av=0
    for i in range(len(DD)*3//4, len(DD)):
        av += DD[i]
    return av/len(DD)*4

def sigma(DD):
    av=avg(DD)
    sig = 0
    for i in range(len(DD)*3//4, len(DD)):
        sig += (DD[i]-av)**2
    return np.sqrt(sig/len(DD))


meja1, meja2 = np.random.randint(120, 220), np.random.randint(340, 550)
a=3
indt, indd = a*2, a*2+1
T = [DT00[indt][j] for j in range(0,meja1)]
T.extend([DT01[indt][j] for j in range(meja1,meja2)])
T.extend([DT00[indt][j] for j in range(meja2,len(DT00[0]))])

D = [DT00[indd][j] for j in range(0,meja1)]
D.extend([DT01[indd][j] for j in range(meja1,meja2)])
D.extend([DT00[indd][j] for j in range(meja2,len(DT00[0]))])



#dodaj(ljepunov(D, T), "ljapunov01.dat")




fig2, ax2 = plt.subplots(figsize=(8,5.5))
ax2.plot(ljepunov(D, T))
#ax2.hlines(y=ljepunov(D, T)[-1], xmin=len(D)/2, xmax=len(D), colors="black", linewidth=0.85, linestyles="dashed")
#ax2.text(len(D)*1.007,ljepunov(D, T)[-1],s=f"$\lambda_\infty$={ljepunov(D, T)[-1]:.2f}")
ax2.set_title("$\lambda(t_i)$")
ax2.set_xlabel("$i$")
ax2.set_ylabel(r"$\lambda$")
ax2.legend()
ax2.set_ylim(-0.5,4.2)
ax2.set_xlim(-0.03*int(len(D)), int(len(D)*1.11))
fig2.tight_layout()
#plt.show()