#!/usr/bin/env python3

import math
import random
import sys

import numpy as np
import matplotlib.pyplot as plt

import collections

if True :
    u = (plt.imread(sys.argv[1])[:,:,1] * 256).clip(0, 255).astype(np.uint8)
    h, w = u.shape

else :
    w, h = 1920, 1080
    u = (256 * np.random.random((h, w))).astype(np.uint8)

plt.imshow(u)
plt.show()

print(w, h, u)

color_lst = plt.rcParams['axes.prop_cycle'].by_key()['color']
print(color_lst)

plt.figure()

r = 4

if False :
    for i, c in enumerate(color_lst[:-1]) :
        # r = random.randrange(2, 8)
        px, py = random.randrange(r, h-r), random.randrange(r, w-r)
        m = 1 + (int((random.random() * 10.0)**2) // 10)
        print(m)
        for j in range(m) :
            qx, qy = random.randrange(r, h-r), random.randrange(r, w-r)
            u[qx-r:qx+r,qy-r:qy+r] = u[px-r:px+r,py-r:py+r]
            plt.plot([py-r, py+r, py+r, py-r, py-r], [px-r, px-r, px+r, px+r, px-r], color=c)
            plt.plot([qy-r, qy+r, qy+r, qy-r, qy-r], [qx-r, qx-r, qx+r, qx+r, qx-r], color=c)
            plt.plot([py, qy], [px, qx], color=c)

v_lst = [(0, 0), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]

v_map = collections.defaultdict(set)
for x in range(r, h-r) :
    print(x, h, end='\r')
    for y in range(r, w-r) :
        v = bytes([u[x+i, y+j] for i, j in v_lst])
        v_map[v].add((x, y))

lb_lst = [(0, None),] * len(color_lst)

for v in v_map :
    if len(v_map[v]) > 1 :
        if len(v_map[v]) >= lb_lst[0][0] :
            lb_lst[0] = ((len(v_map[v]), v))
            lb_lst.sort()
            
print(lb_lst)

for i, (l, b) in enumerate(lb_lst) :
    plt.plot([y for x, y in v_map[b]], [x for x, y in v_map[b]], 'x', color=color_lst[i])

plt.imshow(u)
plt.show()   
plt.savefig("similarities.png")
