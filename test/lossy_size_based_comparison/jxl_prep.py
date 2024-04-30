#!/usr/bin/env python3

import base64
import hashlib
import tempfile
import sys

import numpy as np

import matplotlib
import matplotlib.pyplot as plt

""" test images at incremental distances """

from cc_pathlib import Path

class JxlPrep() :
	def __init__(self, cwd=None) :
		# self.cwd = (Path(__file__) if cwd is None else Path(cwd)).resolve()
		self.cwd = Path(__file__).resolve().parent
		# self.r_pth = self.cwd / "incremental_distance.pickle.br"
		# self.r_map = self.r_pth.load() if self.r_pth.is_file() else dict()
		# hkey -> other_args -> effort -> distance -> [size, score]
		
	def get_hkey(self, src_pth) :
		hsh = hashlib.blake2b(src_pth.read_bytes(), digest_size=24).digest()
		key = base64.urlsafe_b64encode(hsh).decode('ascii')
		return key
		
	def args_to_line(self, ** args) :
		""" ne contient pas l'argument -d """
		a_lst = list()
		c_lst = list()
		for k in sorted(args) :
			a_lst.append(f"{k}{args[k]}")
			c_lst += ['-'*min(2, len(k)) + k, str(args[k])] 
		return '_'.join(a_lst), c_lst
		
	def run(self, src_pth, dist, ** args) :

		src_pth = Path(src_pth).resolve()
		hkey = self.get_hkey(src_pth)
		
		a_pth = self.cwd / "jxl" / f"{hkey}.pickle.br"

		a_map = a_pth.load() if a_pth.is_file() else dict()
			
		akey, c_lst = self.args_to_line(** args)
		if akey not in a_map :
			a_map[akey] = dict()
		e_map = a_map[akey] # {int(k) : v for k, v in a_map[akey].items()}

		with tempfile.TemporaryDirectory('jxl_inc') as tmp :
			tmp_dir = Path(tmp)
			dst_pth = tmp_dir / "i.jxl"
			for e in range(1, 11) :
				if e not in e_map :
					e_map[e] = dict()
				d_map = e_map[e]

				# print("\nD_MAP\n", e, d_map)

				for i in range(10, dist.stop)[dist] :
					d = f"{i / 1000}"
					if i in d_map :
						continue
					tmp_dir.run('cjxl', '-d', d, '-e', e, * c_lst, src_pth, dst_pth)
					ss_score = float(tmp_dir.run('ssimulacra2', src_pth, dst_pth).stdout.decode('utf8'))
					ba_score = float(tmp_dir.run('butteraugli_main', src_pth, dst_pth).stdout.decode('utf8').splitlines()[0])
					d_map[i] = [dst_pth.stat().st_size, ss_score, ba_score]
					print(d, d_map[i])
				
		a_pth.save(a_map)
		a_pth.with_suffix('.json').save(a_map)
		
	def plot(self, src_pth, is_3d=False) :

		src_pth = Path(src_pth).resolve()
		hkey = self.get_hkey(src_pth)
		
		a_pth = self.cwd / "jxl" / f"{hkey}.pickle.br"
		a_map = a_pth.load()

		#color_lst = matplotlib.colormaps['viridis']
		color_lst = matplotlib.colormaps['tab10']
			
		for akey in a_map :

			print(akey)

			if is_3d :
				ax = plt.figure().add_subplot(projection='3d')
			else :
				plt.figure(figsize=(16, 9))
			
			plt.suptitle(f"{src_pth.name} {akey}")

			e_map = a_map[akey]
			e_lst = sorted(e_map)
			for e in e_lst :
				d_map = e_map[e]
				d_lst = sorted(d_map)
				d_arr = np.array(d_lst) / 1000.0
				s_lst, z_lst = list(), list()
				for d in d_lst :
					s_lst.append(d_map[d][0])
					z_lst.append(d_map[d][1])
				if is_3d :
					ax.plot(d_arr, s_lst, z_lst, label=f'e{e}', color=color_lst(e / 10.0))
				else :
					plt.subplot(2, 2, 1)
					plt.plot(d_arr, s_lst, label=f'e{e}', color=color_lst(e-1))

					plt.subplot(2, 2, 2)
					plt.plot(z_lst, s_lst, label=f'e{e}', color=color_lst(e-1))

					plt.subplot(2, 2, 3)
					plt.plot(d_arr, z_lst, label=f'e{e}', color=color_lst(e-1))

			if is_3d :
				ax.set_xlabel('distance')
				ax.set_ylabel('size')
				ax.set_zlabel('score')
				# plt.legend()
				plt.grid()
			else :
				plt.subplot(2, 2, 1)
				plt.xlabel('distance')
				plt.ylabel('size')
				plt.yscale('log')
				# plt.legend()
				plt.grid()
				plt.subplot(2, 2, 2)
				plt.xlabel('score')
				plt.ylabel('size')
				plt.yscale('log')
				# plt.legend()
				plt.grid()
				plt.subplot(2, 2, 3)
				plt.xlabel('distance')
				plt.ylabel('score')
				plt.legend(bbox_to_anchor=(1.04, 0.5), loc="center left", borderaxespad=0)
				plt.grid()

			plt.savefig(f"plot/{hkey}_{akey}.png")
			plt.show()
		
if __name__ == '__main__' :
	src_pth = Path(sys.argv[1]).resolve()
	u = JxlPrep()
	u.run(src_pth, slice(10, 1000, 5), gaborish=0)
	u.plot(src_pth)
		


	
