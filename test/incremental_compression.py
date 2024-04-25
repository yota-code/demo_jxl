#!/usr/bin/env python3

import base64
import hashlib
import tempfile
import sys

import matplotlib.pyplot as plt

""" test images at incremental distances """

from cc_pathlib import Path

class IncrementalDistance() :
	def __init__(self, cwd=None) :
		self.cwd = (Path() if cwd is None else Path(cwd)).resolve()
		
		self.r_pth = self.cwd / "incremental_distance.pickle.br"
		self.r_map = self.r_pth.load() if self.r_pth.is_file() else dict()
		# hkey -> args -> dist -> [size, score]
		
	def get_hkey(self, src_pth) :
		hsh = hashlib.blake2b(src_pth.read_bytes(), digest_size=24).digest()
		key = base64.urlsafe_b64encode(hsh)
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
	
		hkey = self.get_hkey(src_pth)
		if hkey not in self.r_map :
			self.r_map[hkey] = dict()
		a_map = self.r_map[hkey]
			
		akey, c_lst = self.args_to_line(** args)
		if akey not in a_map :
			a_map[akey] = dict()
		d_map = a_map[akey] # {int(k) : v for k, v in a_map[akey].items()}
			
		with tempfile.TemporaryDirectory('jxl_inc') as tmp :
			tmp_dir = Path(tmp)
			dst_pth = tmp_dir / "i.jxl"
			for i in range(10, dist.stop)[dist] :
				d = f"{i / 1000}"
				if d in d_map :
					continue
				if a_map is None :
					a_map = dict()
				tmp_dir.run('cjxl', '-d', d, * c_lst, src_pth, dst_pth)
				ret = tmp_dir.run('ssimulacra2', src_pth, dst_pth)
				d_map[i] = [dst_pth.stat().st_size, float(ret.stdout.decode('utf8'))]
				print(d, d_map[i])
				
		self.r_pth.save(self.r_map)
		self.r_pth.with_suffix('.py').write_text(repr(self.r_map))
		
	def plot(self, src_pth) :
		hkey = self.get_hkey(src_pth)
			
		a_map = self.r_map[hkey]
		for akey in a_map :
			d_map = a_map[akey]
			s_lst, z_lst = list(), list()
			d_lst = sorted(d_map)
			for d in d_lst :
				s_lst.append(d_map[d][0])
				z_lst.append(d_map[d][1])
			plt.plot(d_lst, s_lst, label=akey)
			
		plt.legend()
		plt.grid()
		plt.show()
		
if __name__ == '__main__' :
	src_pth = Path(sys.argv[1]).resolve()
	u = IncrementalDistance()
	for e in range(1, 10) :
		u.run(src_pth, slice(0, 1000, 5), e=e)
	u.plot(src_pth)
		


	
