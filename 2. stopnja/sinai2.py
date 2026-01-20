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
maxSteps = 20000 # of steps of ball motion (in constant speed)

n = 1 # of circular obstacles


# create circular obstacle(s)
cxList = []
cyList = []
crList = []
for i in range(n):
    while(True): # circle(s) must not overlap
        cr = (3-0)/8 # circle radius
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
# initial location of the ball must be outside of the circle(s)
while(True):
    x = 15/16
    y = 0.5
    flag = False
    for i in range(n):
        if math.hypot(x - cxList[i], y - cyList[i]) <= crList[i]:
            flag = True
            break
    if flag == False:
        break
    
# initial direction of the ball
a = np.pi/2
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
plt.savefig(f"sinai2a.png")





# create circular obstacle(s)
cxList = []
cyList = []
crList = []
for i in range(n):
    while(True): # circle(s) must not overlap
        cr = (3-0)/8 # circle radius
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
# initial location of the ball must be outside of the circle(s)
while(True):
    x = 1/2
    y = 1E-4
    flag = False
    for i in range(n):
        if math.hypot(x - cxList[i], y - cyList[i]) <= crList[i]:
            flag = True
            break
    if flag == False:
        break
    
# initial direction of the ball
a = np.pi/2
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
plt.savefig(f"sinai2b.png")




# create circular obstacle(s)
cxList = []
cyList = []
crList = []
for i in range(n):
    while(True): # circle(s) must not overlap
        cr = (np.sqrt(2))/4.1 # circle radius
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
# initial location of the ball must be outside of the circle(s)
while(True):
    x = 1/2
    y = 0.0
    flag = False
    for i in range(n):
        if math.hypot(x - cxList[i], y - cyList[i]) <= crList[i]:
            flag = True
            break
    if flag == False:
        break
    
# initial direction of the ball
a = np.pi/4
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
plt.savefig(f"sinai2c.png")


def f(x):
    return -2*(1-1/x)

R = np.linspace(1E-8,1/2, 100)
plt.figure()
plt.plot(R, f(R))
plt.hlines(2,0,1/2,linestyles="dashed", colors="red")
plt.ylim(-0.5,20)
plt.xlabel("R")
plt.ylabel("tr$F$")
plt.tight_layout()
plt.savefig("sinai2b_1.png")





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


X,Y = [], []
# initial location of the ball must be outside of the circle(s)
#while(True):
#    x = cr
#    y = 1/2
#    flag = False
#    for i in range(n):
#        if math.hypot(x - cxList[i], y - cyList[i]) <= crList[i]:
#            flag = True
#            break
#    if flag == False:
#        break
x = 1/2+cr
y = 1/2

# initial direction of the ball
a = np.pi/4+0.00016
s = math.sin(a)
c = math.cos(a)

dt = 0.001
maxSteps=2120
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
ax.plot(X,[1-Y[i] for i in range(len(Y))], color="C1")
N= 100
circle = [1/2+ cr*np.cos(2*np.pi/N*i) for i in range(N+1)], [1/2+cr*np.sin(2*np.pi/N*i) for i in range(N+1)]
ax.plot(circle[0], circle[1], color="black")
ax.plot([0,1,1,0,0], [0,0,1,1,0], color="black")
ax.set_xlabel("$x$")
ax.set_ylabel("$y$")
ax.set_aspect(1)
fig.tight_layout()
plt.savefig(f"sinai2d.png")