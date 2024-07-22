#!/usr/bin/env python3

import collections
import sys

from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt

import imageio.v3 as iio

ref_pth = Path(sys.argv[1])
tst_pth = Path(sys.argv[2])

ref = iio.imread(ref_pth).astype(np.int16)[:128,:128,:]
tst = iio.imread(tst_pth).astype(np.int16)[:128,:128,:]

h_map = dict()

plt.figure(figsize=(24,24))
plt.suptitle(f"{ref_pth.name} -> {tst_pth.name}")
plt.subplot(2,2,1)
plt.imshow(ref, cmap='seismic')

for i, m in enumerate('RGB') :
	plt.subplot(2,2,2+i)
	plt.title(m)

	dif = tst[:,:,i] - ref[:,:,i]
	hst = collections.defaultdict(int)
	for k in np.nditer(dif) :
		hst[int(k)] += 1
	hst.pop(0, None)
	h_map[m] = hst

	print(m, np.mean(dif), np.std(dif))

	c = 16
	plt.imshow(dif, cmap='seismic', vmin=-c, vmax=c)
	plt.colorbar()

plt.figure()
plt.suptitle(f"{ref_pth.name} -> {tst_pth.name}")
for i, m in enumerate('RGB') :
	plt.subplot(2,2,2+i)
	plt.title(m)
	plt.grid()
	plt.yscale('log')
	hst = h_map[m]
	x_sup = sorted(x for x in hst if x > 0)
	x_inf = sorted(-x for x in hst if x < 0)
	plt.plot(x_sup, [hst[x] for x in x_sup], color="tab:red")
	plt.plot(x_inf, [hst[-x] for x in x_inf], color="tab:blue")
	
# plt.show()




