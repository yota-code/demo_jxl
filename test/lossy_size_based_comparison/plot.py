#!/usr/bin/env python3

import base64
import hashlib
import math
import tempfile
import sys

import numpy as np

import matplotlib
import matplotlib.pyplot as plt

""" test images at incremental distances """

from cc_pathlib import Path

class CodecPlot() :

	codec_map = {
		# ("jxl", '') : [matplotlib.colormaps["Reds"], 1, 10],
		("jxl", 'gaborish0') : [matplotlib.colormaps["YlOrRd"], 1, 10],
		("avif", '') : [matplotlib.colormaps["Blues"], 10, 0],
	}

	def __init__(self, cwd=None) :
		self.cwd = Path(__file__).resolve().parent

	def get_hkey(self, src_pth) :
		hsh = hashlib.blake2b(src_pth.read_bytes(), digest_size=24).digest()
		key = base64.urlsafe_b64encode(hsh).decode('ascii')
		return key

	def plot(self, src_pth, score="ssimulacra", is_3d=False) :

		src_pth = Path(src_pth).resolve()
		hkey = self.get_hkey(src_pth)
		
		if is_3d :
			ax = plt.figure().add_subplot(projection='3d')
		else :
			plt.figure(figsize=(16, 9))
				
		for codec, akey in self.codec_map :

			a_pth = self.cwd / codec / f"{hkey}.pickle.br"
			a_map = a_pth.load()

			print(a_map.keys())

			color_lst, color_from, color_to = self.codec_map[(codec, akey)]

			e_map = a_map[akey]
			e_lst = sorted(e_map)
			print(e_lst)
			for e in e_lst :
				if color_from < color_to :
					c = 0.8 * (e - color_from) / (color_to - color_from) + 0.2
				else :
					c = 0.8 * (color_from - e) / (color_from - color_to) + 0.2
				print(codec, e, c)
				color = color_lst(c)
				q_map = e_map[e]
				d_lst = sorted(q_map)
				print(d_lst)
				d_arr = np.array(d_lst) / 1000.0
				s_lst, z_lst = list(), list()
				for d in d_lst :
					s_lst.append(q_map[d][0])
					z_lst.append(q_map[d][2])
				if is_3d :
					ax.plot(d_arr, s_lst, z_lst, label=f'{codec} {e}', color=color)
				else :
					plt.plot(z_lst, s_lst, label=f'{codec} {e}', color=color)

		if is_3d :
			ax.set_xlabel('distance')
			ax.set_ylabel('size')
			ax.set_zlabel('score')
			# plt.legend()
			plt.grid()
		else :
			plt.xlabel('score')
			plt.ylabel('size')
			plt.yscale('log')
			plt.legend(bbox_to_anchor=(1.01, 0.5), loc="center left", borderaxespad=0)
			plt.grid()

		plt.savefig(f"plot/{hkey}_{akey}.png")
		plt.show()


if __name__ == '__main__' :
	src_pth = Path(sys.argv[1]).resolve()
	u = CodecPlot()
	u.plot(src_pth)