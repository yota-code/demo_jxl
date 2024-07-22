#!/usr/bin/env python3

import sys
import time

from cc_pathlib import Path

src = Path(sys.argv[1])

m_map = dict()

for i in range(1, 20) :
	dst = Path(f"{i:02d}.zstd")
	t = 0.0
	for k in range(4) :
		t0 = time.monotonic_ns()
		Path().run('zstd', f'-{i}', '--quiet', '--keep', '-o', dst, src)
		t1 = time.monotonic_ns()
		t += (t1 - t0) / 4e9
		s = dst.stat().st_size
		if dst.is_file() :
			dst.unlink()
	m_map[i] = s, t
		
with src.with_suffix('.json').config() as cfg :
	cfg['zstd'] = m_map
	
	
# txt = ret.stderr.decode('utf8').replace('%', '')
# print(i, txt.split())
# t, p = [float(k) for k in txt.split()]
# m_map[i] = dst.stat().st_size, t, p
