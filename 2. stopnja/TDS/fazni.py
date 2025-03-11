import numpy as np
# Dynamical Billiards Simulation
# FB - 201010295
# See Wikipedia for more info:
# http://en.wikipedia.org/wiki/Dynamical_billiards
import math
import random
from PIL import Image, ImageDraw
from matplotlib import pyplot as plt



# Only 1 ball is used!
maxSteps = 500000 # of steps of ball motion (in constant speed)

n = 1 # of circular obstacles


# create circular obstacle(s)
cxList = []
cyList = []
crList = []
for i in range(n):
    while(True): # circle(s) must not overlap
        cr = 2/8 # circle radius
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

fig1, ax1 = plt.subplots(figsize=(8,6))
for k in range(1):
    X,Y = [], []
    # initial location of the ball must be outside of the circle(s)
    while(True):
        x = np.random.uniform(0,1)
        y = np.random.uniform(0,1)
        flag = False
        for i in range(n):
            if math.hypot(x - cxList[i], y - cyList[i]) <= crList[i]:
                flag = True
                break
        if flag == False:
            break
        
    # initial direction of the ball
    a = np.pi*2*np.random.uniform(0,1)
    s = math.sin(a)
    c = math.cos(a)

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
        
    fig, ax = plt.subplots(figsize=(6,6))

    ax.plot(X,Y, color="C1")
    N= 100
    circle = [1/2+ cr*np.cos(2*np.pi/N*i) for i in range(N+1)], [1/2+cr*np.sin(2*np.pi/N*i) for i in range(N+1)]
    ax.plot(circle[0], circle[1], color="black")
    ax.plot([0,1,1,0,0], [0,0,1,1,0], color="black")
    ax.set_xlabel("$x$")
    ax.set_ylabel("$y$")
    ax.set_aspect(1)
    fig.tight_layout()
    plt.savefig(f"fazni01a.png")


    def fazni(X, Y):
        n = len(X)
        phi, pphi = [], []
        Rji = []
        for i in range(n):
            phi.append(np.arctan2(Y[i]-1/2, X[i]-1/2))
            Rji.append(np.sqrt((X[i]-1/2)**2 + (Y[i]-1/2)**2))
        for i in range(n-1):
            pphi.append(Rji[i]*(phi[i+1]-phi[i])*1000)
            if pphi[-1] > 1:
                print(Rji[i], phi[i+1]-phi[i], Rji[i]*(phi[i+1]-phi[i]), pphi[-1])
        return phi[:-1], pphi

    x, p = fazni(X,Y)
    #fig1, ax1 = plt.subplots(figsize=(8,6))
    ax1.scatter(x, p, s=1, color="C1")
    ax1.set_ylim(-1.1, 1.1)
    ax1.set_xlabel("$\phi$")
    ax1.set_ylabel("$p_\phi$")
    fig1.tight_layout()
fig1.savefig(f"fazni01b.png")






# NAVADEN FAZNI
maxSteps = 50000 # of steps of ball motion (in constant speed)
# create circular obstacle(s)
cxList = []
cyList = []
crList = []
for i in range(n):
    while(True): # circle(s) must not overlap
        cr = 2/8 # circle radius
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

fig1, ax1 = plt.subplots(figsize=(8,6))
for k in range(10):
    X,Y = [], []
    # initial location of the ball must be outside of the circle(s)
    while(True):
        x = np.random.uniform(0,1)
        y = np.random.uniform(0,1)
        flag = False
        for i in range(n):
            if math.hypot(x - cxList[i], y - cyList[i]) <= crList[i]:
                flag = True
                break
        if flag == False:
            break
        
    # initial direction of the ball
    a = np.pi*2*np.random.uniform(0,1)
    s = math.sin(a)
    c = math.cos(a)

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
        
    fig, ax = plt.subplots(figsize=(6,6))

    ax.plot(X,Y, color="C1")
    N= 100
    circle = [1/2+ cr*np.cos(2*np.pi/N*i) for i in range(N+1)], [1/2+cr*np.sin(2*np.pi/N*i) for i in range(N+1)]
    ax.plot(circle[0], circle[1], color="black")
    ax.plot([0,1,1,0,0], [0,0,1,1,0], color="black")
    ax.set_xlabel("$x$")
    ax.set_ylabel("$y$")
    ax.set_aspect(1)
    fig.tight_layout()
    plt.savefig(f"fazni01a.png")


    def faznix(X, Y):
        n = len(X)
        px = []
        for i in range(n-1):
            px.append((X[i+1]-X[i])*1000)
        return X[:-1], px

    x, p = faznix(X,Y)
    #fig1, ax1 = plt.subplots(figsize=(8,6))
    ax1.scatter(x, p, s=1)
    ax1.set_ylim(-1.1, 1.1)
    ax1.set_xlabel("$x$")
    ax1.set_ylabel("$p_x$")
    fig1.tight_layout()
fig1.savefig(f"fazni02b.png")