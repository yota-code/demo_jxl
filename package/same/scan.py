
import base64
import collections
import hashlib
import random

import imageio.v3 as iio

import numpy as np

from cc_pathlib import Path

class SameScan() :

	block = 8
	coverage = 1.0
	seed = 0
	repeat = 24 # discard blocks repeated less than <repeat> times

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

		e_lst = list(s_map)
		for e in e_lst :
			if len(s_map[e]) < self.repeat :
				del s_map[e]

		print("second pass")
		z_map = collections.defaultdict(list)
		for e in s_map :
			for r, c in s_map[e] :
				e = self.img[r:r+self.block, c:c+self.block].tobytes()
				z_map[base64.a85encode(e).decode('ascii')].append((r, c))

		e_lst = list(z_map)
		for e in e_lst :
			if len(z_map[e]) < self.repeat :
				del z_map[e]

		print("save")
		self.pth.with_suffix('.json').save(z_map, verbose=True)

		return z_map