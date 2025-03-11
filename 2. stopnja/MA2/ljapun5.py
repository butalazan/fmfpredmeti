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





# Only 1 ball is used!
maxSteps = 2500000 # of steps of ball motion (in constant speed)

n = 1 # of circular obstacles

R = [0, 0.1, 0.2, 0.3]
#R = [3/8]
fig2, ax2 = plt.subplots(figsize=(8,5.5))
for k in range(len(R)):
    # create circular obstacle
    cxList = []
    cyList = []
    crList = []
    for i in range(n):
        while(True): # circle(s) must not overlap
            cr = R[k] # circle radius
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
    T = []
    # initial location of the bližnje trajektorije
    epsilon = 1E-4
    #while(True):
    #    b = 2.0 * math.pi * random.random()
    #    x = X[0] + epsilon*np.cos(b)
    #    y = Y[0] + epsilon*np.sin(b)
    #    flag = False
    #    for i in range(n):
    #        if math.hypot(x - cxList[i], y - cyList[i]) <= crList[i]:
    #            flag = True
    #            break
    #    if flag == False:
    #        break

    b = a + math.pi/2
    x = X[0] + epsilon*np.cos(b)
    y = Y[0] + epsilon*np.sin(b)
    if math.hypot(x - cxList[0], y - cyList[0]) <= crList[0]:
        b = a - math.pi/2
        x = X[0] + epsilon*np.cos(b)
        y = Y[0] + epsilon*np.sin(b)
        
    # initial direction of the ball
    s = S[0]
    c = C[0]
    S1.append(s)
    C1.append(c)
    Dx.append(epsilon*np.cos(b))
    Dy.append(epsilon*np.sin(b))
    D.append(epsilon)
    T.append(0.)


    eta = 5*1E-2
    dt = 0.001
    for i in range(maxSteps):
        xnew = x + c*dt
        ynew = y + s*dt

        if i%500==0:
                dx, dy = abs(xnew-X[i]), abs(ynew-Y[i])
                d = np.sqrt((xnew-X[i])**2 + (ynew-Y[i])**2)
                xnew = X[i] + epsilon/d*(xnew - X[i])
                ynew = Y[i] + epsilon/d*(ynew - Y[i])
                c = C[i]
                s = S[i]
                Dx.append(dx)
                Dy.append(dy)
                D.append(d)
                T.append(i*dt)

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




        
    fig, ax = plt.subplots(figsize=(8,5.5))

    ax.plot(X,Y, color="C0")
    ax.scatter(X[0],Y[0], color="C0")
    ax.plot(X1,Y1, color="C1")
    N= 100
    circle = [1/2+ 3/8*np.cos(2*np.pi/N*i) for i in range(N+1)], [1/2+3/8*np.sin(2*np.pi/N*i) for i in range(N+1)]
    ax.plot(circle[0], circle[1], color="black")
    ax.plot([0,1,1,0,0], [0,0,1,1,0], color="black")
    ax.set_title(f"Sinai; r={cr:.2f}")
    ax.set_xlabel("$x$")
    ax.set_ylabel("$y$")
    ax.set_aspect(1)
    fig.tight_layout()
    #plt.savefig("ljapun02.png")






    fig1, ax1 = plt.subplots(figsize=(8,5.5))
    ax1.plot(D, color="C0")
    ax1.set_title(f"Razdalje pri reskalacijah; $\Delta$t={500*dt}, $\epsilon$={epsilon}")
    ax1.set_xlabel("$i$")
    ax1.set_ylabel(r"$|\delta|$")
    fig1.tight_layout()
    #plt.savefig("ljapun02a.png")


    dodaj(T, f"./ljapun_razdalje1_r0{int(cr*10)}.dat")
    dodaj(D, f"./ljapun_razdalje1_r0{int(cr*10)}.dat")

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

    #fig2, ax2 = plt.subplots(figsize=(8,5.5))
    ax2.plot(ljepunov(D, T), label=f"R={cr:.3f}")
    ax2.hlines(y=ljepunov(D, T)[-1], xmin=len(D)/2, xmax=len(D), colors="black", linewidth=0.85, linestyles="dashed")
    ax2.text(len(D)*1.007,ljepunov(D, T)[-1],s=f"$\lambda_\infty$={ljepunov(D, T)[-1]:.2f}")
    ax2.set_title("$\lambda(t_i)$")
    ax2.set_xlabel("$i$")
    ax2.set_ylabel(r"$\lambda$")
    ax2.legend()
    ax2.set_ylim(-0.5,4.2)
    ax2.set_xlim(-0.03*int(len(D)), int(len(D)*1.11))
    fig2.tight_layout()
    #plt.show()
#fig2.savefig("ljapun02b.png")