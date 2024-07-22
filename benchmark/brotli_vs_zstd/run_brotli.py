#!/usr/bin/env python3

import sys
import time

from cc_pathlib import Path

src = Path(sys.argv[1])

m_map = dict()

def run_brotli(i, src, dst) :
	Path().run('brotli', '--keep', '-q', i, '-o', dst, src)
	
def run_zstd(i, src, dst) :
	Path().run('zstd', f'-{i}', '--quiet', '--keep', '-o', dst, src)	

r_lst = [
	('brotli', '.br', run_brotli, 1, 12),
	('zstd', '.zstd', run_zstd, 1, 20),
]


for name, ext, func, start, stop in r_lst :
	for i in range(start, stop) :
		dst = Path(f"{i:02d}{ext}")
		t_lst = list()
		for k in range(5) :
			t0 = time.monotonic_ns()
			funct(i, src, dst)
			t1 = time.monotonic_ns()
			s = dst.stat().st_size
			t_lst.append((t1 - t0) / 4e9)
			if dst.is_file() :
				dst.unlink()
		m_map[i] = s, t

	with src.with_suffix('.json').config() as cfg :
		cfg[name] = m_map

