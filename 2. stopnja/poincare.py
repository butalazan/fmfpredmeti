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
maxSteps = 1000000 # of steps of ball motion (in constant speed)

n = 1 # of circular obstacles


# create circular obstacle(s)
cxList = []
cyList = []
crList = []
for i in range(n):
    while(True): # circle(s) must not overlap
        cr = 0.0 # circle radius
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

fig, ax = plt.subplots(figsize=(8,6))
for k in range(35):
    X,Y = [], []
    poincx, poincp = [], []
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
        if xnew > 1:
            c = -c
            xnew = x
            poincx.append(ynew)
            poincp.append((Y[-1]-Y[-2])/dt)
        if ynew > 1:
            s = -s
            ynew = y
            poincx.append(1+xnew)
            poincp.append((X[-1]-X[-2])/dt)
        if xnew < 0 :
            c = -c
            xnew = x
            poincx.append(2+ynew)
            poincp.append((Y[-1]-Y[-2])/dt)
        if ynew < 0:
            s = -s
            ynew = y
            poincx.append(3+xnew)
            poincp.append((X[-1]-X[-2])/dt)

        # reflection from the circle(s)
        if math.hypot(xnew - cxList[0], ynew - cyList[0]) <= crList[0]:
            # angle of the circle point
            ca = math.atan2(ynew - cyList[0], xnew - cxList[0])
            # reversed collision angle of the ball
            rca = math.atan2(-s, -c)
            # reflection angle of the ball
            rab = rca + (ca - rca) * 2
            s = math.sin(rab)
            c = math.cos(rab)
            xnew = x
            ynew = y

            phi_star = np.arctan2(Y[-2]-1/2, X[-2]-1/2)
            phi = np.arctan2(ynew-1/2, xnew-1/2)
            R = np.sqrt((xnew-1/2)**2 + (ynew-1/2)**2)

            pphi = R*(phi_star-phi)*1000

            poincx.append(4+R*phi + np.pi*cr)
            poincp.append(pphi)

        x = xnew
        y = ynew
        X.append(x)
        Y.append(y)
        
    if i == 0:
        ax.vlines(4, -1, 1, linestyles="dashed", linewidth=0.7, color="black")
    #ax.scatter(poincx, poincp, color="C1", s=1)
    ax.scatter(poincx, poincp, s=0.8)
    ax.set_title(f"$R=${cr}")
    ax.set_xlabel("$s$")
    ax.set_ylabel("$p_s$")
    ax.set_ylim(-1.1, 1.1)
    fig.tight_layout()
fig.savefig(f"poincare04d.png")






maxSteps = 5000

# create circular obstacle(s)
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

from numpy import pi as pi
fig, ax = plt.subplots(figsize=(8,6))
xz = [0.10, 0.15, 0.2, 1-0.10, 1-0.15, 1-0.2, 0., 0., 0., 0., 0., 0., 0.45, 0.55, 0.59]
yz = [0., 0., 0., 0., 0., 0., 0.1, 0.15, 0.2, 1-0.1, 1-0.15, 1-0.2, 0, 0, 0]
az = [pi/2, pi/2, pi/2, pi/2, pi/2, pi/2, 0, 0, 0, 0, 0, 0, pi/4, pi/4, pi/4]
barve = ["C1", "C2", "C3", "C4", "C5"]
fig1, ax1 = plt.subplots(figsize=(6,6))
for j in range(5):
    for k in range(3):
        X,Y = [], []
        poincx, poincp = [], []
        # initial location of the ball must be outside of the circle(s)
        print(j*3+k)
        while(True):
            #x = np.random.uniform(0,1)
            #y = np.random.uniform(0,1)
            x = xz[j*3+k]
            y = yz[j*3+k]
            flag = False
            for i in range(n):
                if math.hypot(x - cxList[i], y - cyList[i]) <= crList[i]:
                    flag = True
                    break
            if flag == False:
                break
            
        # initial direction of the ball
        #a = np.pi*2*np.random.uniform(0,1)
        a = az[j*3+k]
        s = math.sin(a)
        c = math.cos(a)

        dt = 0.001
        for i in range(maxSteps):
            #image.putpixel((int(x), int(y)), (255, 255, 255))
            xnew = x + c*dt
            ynew = y + s*dt

            # reflection from the walls
            if xnew > 1:
                c = -c
                xnew = x
                poincx.append(ynew)
                poincp.append((Y[-1]-Y[-2])/dt)
            if ynew > 1:
                s = -s
                ynew = y
                poincx.append(1+xnew)
                poincp.append((X[-1]-X[-2])/dt)
            if xnew < 0 :
                c = -c
                xnew = x
                poincx.append(2+ynew)
                poincp.append((Y[-1]-Y[-2])/dt)
            if ynew < 0:
                s = -s
                ynew = y
                poincx.append(3+xnew)
                poincp.append((X[-1]-X[-2])/dt)

            # reflection from the circle(s)
            if math.hypot(xnew - cxList[0], ynew - cyList[0]) <= crList[0]:
                # angle of the circle point
                ca = math.atan2(ynew - cyList[0], xnew - cxList[0])
                # reversed collision angle of the ball
                rca = math.atan2(-s, -c)
                # reflection angle of the ball
                rab = rca + (ca - rca) * 2
                s = math.sin(rab)
                c = math.cos(rab)
                xnew = x
                ynew = y

                phi_star = np.arctan2(Y[-2]-1/2, X[-2]-1/2)
                phi = np.arctan2(ynew-1/2, xnew-1/2)
                R = np.sqrt((xnew-1/2)**2 + (ynew-1/2)**2)

                pphi = R*(phi_star-phi)*1000

                poincx.append(4+R*phi + np.pi*cr)
                poincp.append(pphi)

            x = xnew
            y = ynew
            X.append(x)
            Y.append(y)
            


        ax1.plot(X,Y, color=barve[j])
        N= 100
        circle = [1/2+ cr*np.cos(2*np.pi/N*i) for i in range(N+1)], [1/2+cr*np.sin(2*np.pi/N*i) for i in range(N+1)]
        ax1.plot(circle[0], circle[1], color="black")
        ax1.plot([0,1,1,0,0], [0,0,1,1,0], color="black")
        ax1.set_title("$R=${cr}")
        ax1.set_xlabel("$x$")
        ax1.set_ylabel("$y$")
        ax1.set_aspect(1)
        fig1.tight_layout()
fig1.savefig(f"poincare02.png")
