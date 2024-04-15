#!/usr/bin/env python3

import collections
import math
import random
import sys

import imageio.v3 as iio

import numpy as np
import matplotlib.pyplot as plt

from cc_pathlib import Path

i_pth = Path("i_map.pickle")

img = iio.imread(sys.argv[1])
if img.dtype != np.uint8 :
	img = (img * 255).round().clip(0, 255).astype(np.uint8)
h, w, d = img.shape

print(h, w, d, img.dtype)

block_size = 12

if not i_pth.is_file() :

	# plt.imshow(img)
	# plt.show()

	p_lst = list()
	for r in range(h-block_size) :
		for c in range(w-block_size) :
			p_lst.append((r, c))
	random.seed(0)
	random.shuffle(p_lst)

	i_map = collections.defaultdict(list)

	print("SCANNING...")

	for r, c in p_lst :
		e = hash(img[r:r+block_size, c:c+block_size].tobytes()) & 0xFFFF_FFFF
		i_map[e].append((r, c))

	print("DONE!")

	e_lst = list(i_map)
	for e in e_lst :
		if len(i_map[e]) <= 3 :
			del i_map[e]

	i_pth.save(i_map)
else :
	i_map = i_pth.load()

print(i_map)

color_lst = plt.rcParams['axes.prop_cycle'].by_key()['color']

lb_lst = [(0, None),] * len(color_lst)
for e in i_map :
	if len(i_map[e]) > 1 :
		lb_lst.append((len(i_map[e]), e))
		lb_lst = sorted(lb_lst)[-len(color_lst):]

print(lb_lst)

plt.figure()

plt.imshow(img)

for i, (l, b) in enumerate(lb_lst) :
	plt.plot([y for x, y in i_map[b]], [x for x, y in i_map[b]], 'x', color=color_lst[i])

plt.savefig("similarities.png")

plt.show()
