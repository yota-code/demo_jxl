
import base64
import collections
import hashlib
import random

import imageio.v3 as iio

import numpy as np
import matplotlib.pyplot as plt

from cc_pathlib import Path

def decimate_map(s_map, rate=1.0, min_rep=4) :

	h_map = collections.defaultdict(int)

	e_lst = list(s_map)
	for e in e_lst :
		# on vire les tous les qui ne sont pas répétés au moins <min_rep> fois
		if min_rep <= len(s_map[e]) :
			h_map[len(s_map[e])] += 1

	h_min, h_max = min(h_map), max(h_map)
	h_lst = [0,] * (h_max - h_min + 1)
	for h in h_map :
		h_lst[h - h_min] = h_map[h]

	x_lst = list(range(h_min, h_max + 1))

	# plt.figure()
	if rate != 1.0 :
		h_lim = max(h_lst) * rate

		# plt.plot(x_lst, h_lst, '+--')
		# plt.axhline(h_lim, color="tab:red")

		for i in range(len(h_lst)) :
			if h_lst[-1-i] > h_lim :
				h_lst = h_lst[-i:]
				x_lst = x_lst[-i:]
				break
	# plt.plot(x_lst, h_lst)
	# plt.grid()
	# plt.show()

	print('----')
	print(x_lst)
	print(h_lst)

	x_min = min(x_lst)
	for e in e_lst :
		if len(s_map[e]) < x_min :
			del s_map[e]
	
class SameScan() :

	block = 8
	coverage = 1.0
	seed = 0
	repeat = 4 # discard blocks repeated less than <repeat> times

	# def __init__(self, cache_dir=None) :
	# 	self.cache_dir = Path(cache_dir).resolve() if cache_dir is not None else None

	def load(self, pth) :

		self.pth = Path(pth).resolve()

		self.img = iio.imread(self.pth)
		if self.img.dtype != np.uint8 :
			self.img = (self.img * 255).round().clip(0, 255).astype(np.uint8)
		
		h = hashlib.blake2b(str(self.pth).encode('utf8'), digest_size=12, salt=b'samesame')
		self._b = base64.urlsafe_b64encode(h.digest()).decode("ascii")
		
	def iter(self) :
		h, w, d = self.img.shape

		if self.coverage == 1.0 :
			for r in range(h - self.block) :
				for c in range(w - self.block) :
					yield r, c
		else :
			p_lst = list()
			for r in range(h - self.block) :
				for c in range(w - self.block) :
					p_lst.append((r, c))

			random.seed(self.seed)
			random.shuffle(p_lst)

			for r, c in p_lst[:int(len(p_lst) * self.coverage)] :
				yield r, c
		
	def scan(self, pth) :

		self.load(pth)

		print("first pass")
		s_map = collections.defaultdict(list)
		for r, c in self.iter() :
			e = hash(self.img[r:r+self.block, c:c+self.block].tobytes()) & 0xFFFF_FFFF
			s_map[e].append((r, c))

		decimate_map(s_map, 0.2)

		print("second pass")
		z_map = collections.defaultdict(list)
		for e in s_map :
			for r, c in s_map[e] :
				e = self.img[r:r+self.block, c:c+self.block].tobytes()
				z_map[base64.a85encode(e).decode('ascii')].append((r, c))

		decimate_map(z_map, 1.0)

		print("save")
		self.pth.with_suffix('.json').save(z_map, verbose=True)

		return z_map