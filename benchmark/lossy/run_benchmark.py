#!/usr/bin/env python3

#!/usr/bin/env python3

import ast
import base64
import collections
import hashlib
import math
import os
import sys
import tempfile

import imageio.v3 as iio
import matplotlib.pyplot as plt

from cc_pathlib import Path

jxl_root_dir = Path(os.environ['JXL_root_DIR'])

"""
un fichier résultat par image, nommé d'après le checksum
"""

# max norm is butteraugli, pnorm is the 3-norm butteraugli
#Encoding              kPixels    Bytes          BPP  E MP/s  D MP/s     Max norm  SSIMULACRA2   PSNR        pnorm       BPP*pnorm   QABPP   Bugs
# Score = collections.namedtuple("Score", ['pixel_count', 'bytes', 'bpp', 'enc_spd', 'dec_spd', 'butteraugli', 'ssimulacra2', 'psnr', 'butteraugli3', 'pnorm_bpp', 'qa_bpp', 'bugs'])


class JxlCodec() :

	key = 'jxl'
	
	jxl_settings = {
		"d" : [0.05, 0.06, 0.07, 0.08, 0.09, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.8, 1.0, 1.2, 1.4, 1.5, 1.6, 1.8, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0],
		"e" : [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
	}

	# jxl_settings = {
	# 	"d" : [0.1, 0.5, 1.0, 2.0],
	# 	"e" : [1, 3, 5, 7]
	# }


	jxl_efforts = [
		"lightning", "thunder", "falcon",
		"cheetah", "hare", "wombat",
		"squirrel", "kitten", "tortoise",
		"glacier"
	]

	def __init__(self) :
		self.version = Path().run("cjxl", "--version").stdout.decode('utf8').splitlines()[0]
	
	@property
	def todo(self) :
		b_set = set()
		for distance in self.jxl_settings['d'] :
			for effort in self.jxl_settings['e'] :
				b_set.add(f"d{distance}:{self.jxl_efforts[effort]}")
		return b_set
	
class AvifCodec() :

	key = 'jxl'

	avif_settings = {
		"q" : [100, 99, 98, 97, 96, 95, 94, 93, 92, 91, 90, 88, 86, 84, 80, 78, 76, 74, 72, 70, 68, 64, 60, 55, 50],
		"s" : [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
	}

	# avif_settings = {
	# 	"q" : [100, 95, 92, 90],
	# 	"s" : [3, 7, 10]
	# }


	def __init__(self) :
		self.version = Path().run("avifenc", "--version").stdout.decode('utf8').splitlines()[0]

	@property
	def todo(self) :
		b_set = set()
		for quality in self.avif_settings['q'] :
			for speed in self.avif_settings['s'] :
				b_set.add(f"q{quality}:s{speed}")
		return b_set

class Benchmark() :

	cwd = jxl_root_dir / "benchmark" / "lossy"

	def __init__(self, image_pth) :

		self.c_map = {
			'jxl' : JxlCodec(),
			'avif' : AvifCodec()
		}

		self.image_pth = Path(image_pth).resolve()
		self.image_hsh = self.compute_hash(self.image_pth)	

		self.result_pth = self.cwd / "_result" / f"{self.image_hsh}.json"

		if self.result_pth.is_file() :
			self.result_map = self.result_pth.load()
		else :
			self.result_map = {'__info__': dict()}
			image_iio = iio.imread(self.image_pth)
			self.result_map['__info__']['shape'] = image_iio.shape
			self.result_map['__info__']['size'] = self.image_pth.stat().st_size
			self.result_pth.save(self.result_map, verbose=True)

	def compute_hash(self, pth) :
		return base64.urlsafe_b64encode(hashlib.blake2b(pth.read_bytes(), digest_size=24, salt=b'jxl').digest()).decode('ascii')
		
	def run(self) :
		c_set = set()
		for k, codec in self.c_map.items() :
			c_set |= set((k + ':' + v) for v in codec.todo - self.result_map[k].get(codec.version, dict()).keys())
		c_lst = sorted(c_set)

		print(c_lst, len(c_lst))

		a_lst = c_lst[:8]

		while a_lst :
			ret = Path().run("benchmark_xl", "--codec=" + ','.join(str(a) for a in a_lst), f"--input={self.image_pth}")
			res = ret.stdout.decode('utf8')

			is_result = False
			for line in res.splitlines() :
				if line.startswith('----') :
					is_result = True
					continue
				if line.startswith("Aggregate:") :
					break
				if is_result :
					s_lst = line.split()
					m, * flags = s_lst.pop(0).split(':')
					kpixels, bytes, bpp, enc_spd, dec_spd, butteraugli_m, ssimulacra2, psnr, butteraugli_3, pnorm_bpp, qa_bpp, bugs = s_lst
					with self.result_pth.config() as cfg :
						if m not in cfg :
							cfg[m] = dict()
						codec = self.c_map[m]
						if codec.version not in cfg[m] :
							cfg[m][codec.version] = dict()
						cfg[m][self.c_map[m].version][':'.join(flags)] = [
							ast.literal_eval(i) for i in (bytes, enc_spd, dec_spd, ssimulacra2, butteraugli_m, butteraugli_3, psnr)
						]

			a_lst = c_lst[:8]
			c_lst = c_lst[8:]

def plot(self, image_hsh) :
	result_pth = self.result_dir / f"{image_hsh}.tsv"

	if result_pth.is_file() :
		result_lst = result_pth.load()
	else :
		raise FileNotFoundError
	
	m_map = collections.defaultdict(set)
	
	for line in result_lst :
		if line.startswith('#') :
			continue
		l_lst = line.split('\t')
		k = l_lst.pop()
		v_lst = [ast.literal_eval(v) for v in v_lst]
		c = k.split(':')[0]

		m_map[c].append(())
		
		m = {'avif' : 'v', 'jxl': '^'}[c]

if __name__ == '__main__' :
	
	for arg in sys.argv[1:] :
		b = Benchmark(arg).run()


# import numpy as np
# import plotly.graph_objects as go
# import matplotlib.pyplot as plt

# if False :
# 	fig = plt.figure()
# 	ax = fig.add_subplot(projection='3d')

# 	for k in ['avif', 'jxl'] :
# 		x_lst, y_lst, z_lst = list(), list(), list()
# 		for key, score in r_map.items() :
# 			if key.startswith(k) :
# 				x_lst.append(score.bpp)
# 				y_lst.append(score.enc_spd)
# 				z_lst.append(score.ssimulacra2)
# 		print(len(x_lst))
# 		ax.scatter(x_lst, y_lst, z_lst)

# 	ax.set_xlabel('bpp')
# 	ax.set_ylabel('enc_spd')
# 	ax.set_zlabel('ssimulacra2')

# 	plt.show()

# if True :
# 	fig = plt.figure()
# 	ax3 = fig.add_subplot(1, 2, 1, projection='3d')
# 	ax2 = fig.add_subplot(1, 2, 2)
# 	for k in ['avif', 'jxl'] :
# 		effort_map = collections.defaultdict(lambda : {'bpp': dict(), 'spd': dict(), 'score': dict()})
# 		x_lst, y_lst, z_lst = list(), list(), list()
# 		for key, score in r_map.items() :
# 			if key.startswith(k) :
# 				if k == 'avif' :
# 					effort = int(key.split('@')[0].split(':')[2][1:])
# 					quality = int(int(key.split('@')[0].split(':')[1][1:]))
# 				elif k == 'jxl' :
# 					effort = effort_lst.index(key.split('@')[0].split(':')[-1])
# 					quality = float(key.split('@')[0].split(':')[1][1:])
# 				effort_map[effort]['bpp'][quality] = math.log(score.bpp)
# 				effort_map[effort]['spd'][quality] = math.log(score.enc_spd)
# 				effort_map[effort]['score'][quality] = score.ssimulacra2
# 				x_lst.append(math.log(score.bpp))
# 				y_lst.append(math.log(score.enc_spd))
# 				z_lst.append(score.ssimulacra2)
# 		ax3.plot_trisurf(x_lst, y_lst, z_lst, alpha=0.6666)
# 		for effort in effort_map :
# 			x_lst = [effort_map[effort]['bpp'][quality] for quality in sorted(effort_map[effort]['bpp'])]
# 			y_lst = [effort_map[effort]['spd'][quality] for quality in sorted(effort_map[effort]['spd'])]
# 			z_lst = [effort_map[effort]['score'][quality] for quality in sorted(effort_map[effort]['score'])]
# 			if k == 'avif' :
# 				ax3.plot(x_lst, y_lst, z_lst, '--')
# 			elif k == 'jxl' :
# 				ax3.plot(x_lst, y_lst, z_lst)
# 			ax2.plot(x_lst, z_lst, '+-', color='tab:green' if k == 'jxl' else 'tab:red')
# 	ax2.grid()
# 	# ax2.set_xscale('log')

# 	ax2.set_xlabel('log(bpp)')
# 	ax2.set_ylabel('score')

# 	ax3.set_xlabel('log(bpp)')
# 	ax3.set_ylabel('log(spd)')
# 	ax3.set_zlabel('score')

# 	plt.show()

# if False :
# 	p_lst = list()
# 	for k, c in [('avif', 'orange'), ('jxl', 'blue')] :
# 		x_lst, y_lst, z_lst = list(), list(), list()
# 		for key, score in r_map.items() :
# 			if key.startswith(k) :
# 				x_lst.append(score.bpp)
# 				y_lst.append(score.enc_spd)
# 				z_lst.append(score.ssimulacra2)
# 		p_lst.append(go.Mesh3d(x=x_lst, y=y_lst, z=z_lst, color=c))
# 	fig = go.Figure(data=p_lst)
# 	fig.show()
		
	