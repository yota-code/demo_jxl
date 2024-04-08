#!/usr/bin/env python3

"""
https://hal.science/hal-03859737/document
"""

import sys

import numpy as np
import scipy
import matplotlib.pyplot as plt
import imageio.v3 as iio

from pathlib import Path

src_pth = Path(sys.argv[1])
dst_pth = src_pth.with_suffix('.red.png')

img = iio.imread(src_pth)
h, w, d = img.shape

""" on compte les zeros d'une transformée dct """
res = scipy.fft.dct(img[:,:,0] + img[:,:,1] + img[:,:,2])
p = 1
for i in range(w) :
	if abs(res[h // 2, i]) <= 0.01 :
		p += 1

try :
	assert w % p == 0
	assert h % p == 0
except AssertionError :
	plt.imshow(np.clip(np.absolute(res), 0.0, 8.0))
	plt.show()
	raise

red = np.zeros_like(img)[:h//p,:w//p,:]
for r in range(h // p) :
	for c in range(w // p) :
		for l in range(d) :
			z = img[r*p:(r+1)*p,c*p:(c+1)*p,:]
			try :
				# on vérifie que tous les pixels sont bien identiques sur la zone avant de copier
				assert np.all(z == z[0,0,:])
			except :
				plt.imshow(z)
				plt.show()
				raise
			red[r,c,:] = z[0,0,:]

iio.imwrite(dst_pth, red)

""" on sauvegarde le résultat de l'image réduite """
