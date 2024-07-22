#!/usr/bin/env python3

import time

import numpy as np
import matplotlib.pyplot as plt

from cc_pathlib import Path

def run_brotli(i, src) :
	Path().run('brotli', '--keep', '-q', i, src)
	
def run_zstd(i, src) :
	Path().run('zstd', f'-{i}', '--quiet', '--keep', src)

def run_lzip(i, src) :
	Path().run('lzip', f'-{i}', '--keep', src)

def run_gzip(i, src) :
	Path().run('gzip', f'-{i}', '--keep', src)

class BenchMark() :
	r_lst = [
		('brotli', '.br', run_brotli, 1, 12, "tab:blue"),
		('zstd', '.zst', run_zstd, 1, 20, "tab:red"),
		('lzip', '.lz', run_lzip, 1, 10, "tab:green"),
		('gzip', '.gz', run_gzip, 1, 10, "tab:orange"),
	]
	
	def __init__(self, src) :
		self.src = Path(src).resolve()
		self.res = self.src.with_suffix('.json')
		
		assert self.src.is_file()
		
		if not self.res.is_file() :
			self.run()
			
		self.plot()
		
	def run(self) :
		for name, ext, func, start, stop, color in self.r_lst :
			m_map = dict()
			for i in range(start, stop) :
				dst = Path(self.src.name + ext)
				t_lst = list()
				for k in range(9) :
					t0 = time.monotonic_ns()
					func(i, self.src)
					t1 = time.monotonic_ns()
					s = dst.stat().st_size
					t_lst.append((t1 - t0) / 4e9)
					if dst.is_file() :
						dst.unlink()
				m_map[i] = s, sorted(t_lst)

			with self.res.config() as cfg :
				cfg[name] = m_map

	def plot(self) :
		plt.figure(figsize=(16,12))

		plt.title('.'.join(self.res.name.split('.')[:-1]))
		f_map = self.res.load()
		for name, ext, func, start, stop, color in self.r_lst :
			s_lst = list()
			t_lst = list()
			i_lst = list()
			m_map = f_map[name]
			for i in sorted(m_map, key=int) :
				s, t = m_map[i]
				i_lst.append(i)
				s_lst.append(s)
				t_lst.append(sorted(t)[1:-1])
			t_arr = np.array(t_lst)
			t_mean = np.mean(t_arr, axis=1)
			t_dev = np.std(t_arr, axis=1)
			for i, s, t in zip(i_lst, s_lst, t_mean) :
				plt.text(s, t, i)
			
			plt.plot(s_lst, t_mean, 'x-', label=name, color=color)
			plt.fill_between(s_lst, t_mean - t_dev, t_mean + t_dev, color=color, alpha=0.3)
			
		plt.xlabel("size")
		plt.ylabel("time")
		plt.yscale('log')	
		plt.legend()
		plt.grid()
		plt.savefig(self.res.with_suffix('.png'))
		plt.show()

		
if __name__ == '__main__' :
	import sys
	u = BenchMark(sys.argv[1])

