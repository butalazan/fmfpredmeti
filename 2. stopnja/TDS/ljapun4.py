import numpy as np
# Dynamical Billiards Simulation
# FB - 201010295
# See Wikipedia for more info:
# http://en.wikipedia.org/wiki/Dynamical_billiards
import math
import random
from PIL import Image, ImageDraw
from matplotlib import pyplot as plt


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


# Only 1 ball is used!
maxSteps = 1000000 # of steps of ball motion (in constant speed)

n = 1 # of circular obstacles

N=25
R = [(1/2-0)*1.2/N*(N-j-1) for j in range(N)]
#R = [3/8]
fig2, ax2 = plt.subplots(figsize=(8,5.5))
fig3, ax3 = plt.subplots(figsize=(8,5.5))
for k in range(len(R)):
    LJAPUNOV_R = []
    for kk in range(20):
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
        #X.append(x)
        #Y.append(y)
            
        # initial direction of the ball
        a = 2.0 * math.pi * random.random()
        s = math.sin(a)
        c = math.cos(a)
        #S.append(s)
        #C.append(c)


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
        #S1.append(s)
        #C1.append(c)
        #Dx.append(epsilon*np.cos(b))
        #Dy.append(epsilon*np.sin(b))
        #D.append(epsilon)
        #T.append(0.)


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
        

        LJAPUNOV_R.append(ljepunov(D, T)[-1])


        ax2.scatter(cr, ljepunov(D, T)[-1], color="C0", s=8)
    ax2.set_title("$\lambda(R)$")
    ax2.set_xlabel("$R$")
    ax2.set_ylabel(r"$\lambda_\infty$")
    ax2.set_ylim(-0.2,3.6)
    #ax3.legend()
    fig2.tight_layout()

    ax3.errorbar(cr, avg(LJAPUNOV_R), sigma(LJAPUNOV_R), fmt="o", ms=3, capsize=4, color="C0")
    ax3.set_title("$\lambda(R)$")
    ax3.set_xlabel("$R$")
    ax3.set_ylabel(r"$\lambda_\infty$")
    #ax3.legend()
    fig3.tight_layout()

fig2.savefig("ljapun04b.png")
fig3.savefig("ljapun04c.png")