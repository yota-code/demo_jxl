#!/usr/bin/env python3

import collections

"""
take a list of blocks flagged as similar, try to expand them as much as possible while keeping them similar
"""

blip = collections.NamedTuple('Blip', ['br', 'bc', 'bh', 'bw'])

class SameGrow() :

	w_map = {
		'up': [-1, 0, 1, 0],
		'down': [0, 0, 1, 0],
		'left' : [0, -1, 0, 1],
		'right': [0, 0, 0, 1]
	}

	def __init__(self, arr) :

		self.arr = arr
		self.h, self.w, self.d = arr.shape

		self.b_set = set()

	def push(self, blip) :

		self.b_set.add(blip)

	def _grow_one(self, way) :
		for br, bc, bh, bw in self.b_set :
			if br == 0 :
				return False
			
		r_set = set()

		dr, dc, dh, dw = self.w_map[way]
		for br, bc, bh, bw in self.b_set :
			r_set.add(blip(br+dr, bc+dc, bh+dh, bw+dw))

		return r_set

	def check(self, r_set=None) :
		if r_set is None :
			r_set = self.b_set

		prev = None
		for br, bc, bh, bw in r_set :
			curr = self.arr[br:br+bh, bc:bc+bw]
			if prev is not None :
				if not (prev == curr).all() :
					return False
			prev = curr

	def grow(self) :
		
		e = True
		while e :
			e = False
			for w in self.w_map :
				r_set = self._grow_one(w)
				if self.check(r_set) :
					e = True
					self.b_set = r_set 
			