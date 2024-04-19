#!/usr/bin/env python3

import collections

"""
take a list of blocks flagged as similar, try to expand them as much as possible while keeping them similar
"""

class PatchList() :

	w_map = {
		'up': [-1, 0, 1, 0],
		'down': [0, 0, 1, 0],
		'left' : [0, -1, 0, 1],
		'right': [0, 0, 0, 1]
	}

	def __init__(self, rc_lst, height, width) :
		self.rc_lst = rc_lst
		self.height, self.width = height, width

	def __iter__(self) :
		for r, c in self.rc_lst :
			yield r, c

	def grow(self, way) :
		# return a new class
		for br, bc in self.rc_lst :
			if br == 0 and way == 'up' :
				raise ValueError
			if bc == 0 and way == 'left' :
				raise ValueError
			
		dr, dc, dh, dw = self.w_map[way]

		rc_lst = list()
		width = self.width + dw
		height = self.height + dh
		for br, bc in self.rc_lst :
			rc_lst.append((br+dr, bc+dc))

		return PatchList(rc_lst, height, width)

class SameGrow() :

	def __init__(self, img, rc_lst, height, width) :

		self.img = img
		self.h, self.w, self.d = img.shape

		self.p_lst = PatchList(rc_lst, height, width)

	def check(self, p_lst=None) :

		if p_lst is None :
			p_lst = self.p_lst

		print(">>>", p_lst.rc_lst, p_lst.height, p_lst.width, end='\t')
		
		prev = None
		bh, bw = p_lst.height, p_lst.width
		for br, bc in p_lst :
			curr = self.img[br:br+bh, bc:bc+bw, :]
			if prev is not None :
				if not (prev == curr).all() :
					print("FAILURE")
					return False
			prev = curr
		print("SUCCESS")
		return True

	def grow(self) :
		e = True
		while e :
			e = False
			print("----")
			for w in PatchList.w_map :
				try :
					q_lst = self.p_lst.grow(w)
				except ValueError :
					e = False
					break
				if self.check(q_lst) :
					print(f"grow {w} SUCCESS")
					e = True
					self.p_lst = q_lst
				else :
					print(f"grow {w} FAILURE")

	def plot(self) :
		import matplotlib.pyplot as plt

		plt.figure()
		plt.imshow(self.img)
		h, w = self.p_lst.height, self.p_lst.width
		for r, c in self.p_lst :
			print(r, c, h, w)
			plt.plot([c-0.5, c+w-0.5, c+w-0.5, c-0.5, c-0.5], [r-0.5, r-0.5, r+h-0.5, r+h-0.5, r-0.5], color='tab:blue')

		plt.grid()
		plt.show()