#!/usr/bin/env python3

import ast
import base64
import hashlib
import tempfile
import sys

import numpy as np

import matplotlib
import matplotlib.pyplot as plt

""" test images at incremental distances """

from cc_pathlib import Path

class CodecPrep() :

	def __init__(self, cwd=None) :
		self.cwd = Path(__file__).resolve().parent

	def get_hkey(self, src_pth) :
		hsh = hashlib.blake2b(src_pth.read_bytes(), digest_size=24).digest()
		key = base64.urlsafe_b64encode(hsh).decode('ascii')
		return key
		
	def args_to_akey(self, ** args) :
		a_lst = list()
		for k in sorted(args) :
			a_lst.append(f"{k}{args[k]}")
		return '_'.join(a_lst)
	
	def args_to_command(self, ** args) :
		c_lst = list()
		for k in sorted(args) :
			c_lst += ['-'*min(2, len(k)) + k, str(args[k])] 
		return c_lst
		
	def run(self, src_pth, ** args) :
		src_pth = Path(src_pth).resolve()
		hkey = self.get_hkey(src_pth)
		
		a_pth = self.cwd / self.codec_name / f"{hkey}.pickle.br"
		self.a_map = a_pth.load() if a_pth.is_file() else dict()
			
		akey = self.args_to_akey(** args)
		if akey not in self.a_map :
			self.a_map[akey] = dict()
		s_map = self.a_map[akey]

		try :
			with tempfile.TemporaryDirectory('lsbc') as tmp :
				tmp_dir = Path(tmp)
				for s in range(self.speed_range.stop)[self.speed_range] :
					if s not in s_map :
						s_map[s] = dict()
					q_map = s_map[s]

					for q in range(self.quality_range.stop)[self.quality_range] :
						if q in q_map :
							continue
						q_map[q] = self.one(src_pth, tmp_dir, q, s, ** args)
						print(q, q_map[q])
		except KeyboardInterrupt :
			pass
				
		a_pth.save(self.a_map)
		(self.cwd / self.codec_name / f"{hkey}.json").save(self.a_map, verbose=True)
		
class AvifPrep(CodecPrep) :

	quality_range = slice(70, 100)
	speed_range = slice(0, 11)
	codec_name = "avif"

	def one(self, src_pth, tmp_dir, quality, speed, ** args) :
		dst_pth = tmp_dir / "file.avif"
		png_pth = dst_pth.with_suffix('.png')

		c_lst = self.args_to_command(** args)
	
		tmp_dir.run('avifenc', '-q', quality, '-s', speed, * c_lst, src_pth, dst_pth)
		tmp_dir.run('avifdec', dst_pth, png_pth)
		ss_score = float(tmp_dir.run('ssimulacra2', src_pth, png_pth).stdout.decode('utf8'))
		ba_score = float(tmp_dir.run('butteraugli_main', src_pth, png_pth).stdout.decode('utf8').splitlines()[0])

		return dst_pth.stat().st_size, ss_score, ba_score
	
class JxlPrep(CodecPrep) :

	quality_range = slice(10, 1600, 5)
	speed_range = slice(1, 11)
	codec_name = "jxl"

	def one(self, src_pth, tmp_dir, distance, effort, ** args) :
		dst_pth = tmp_dir / "file.jxl"

		c_lst = self.args_to_command(** args)
	
		tmp_dir.run('cjxl', '-d', distance / 1000.0, '-e', effort, * c_lst, src_pth, dst_pth)
		ss_score = float(tmp_dir.run('ssimulacra2', src_pth, dst_pth).stdout.decode('utf8'))
		ba_score = float(tmp_dir.run('butteraugli_main', src_pth, dst_pth).stdout.decode('utf8').splitlines()[0])

		return dst_pth.stat().st_size, ss_score, ba_score

if __name__ == '__main__' :

	codec = sys.argv[1].strip().lower()
	src_pth = Path(sys.argv[2]).resolve()

	u = {
		'jxl': JxlPrep,
		'avif': AvifPrep,
	}[codec]()

	args = ast.literal_eval(sys.argv[3]) if 2 < len(sys.argv) else dict()

	u.run(src_pth, ** args)
		


	
