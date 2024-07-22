#!/usr/bin/env python3

import sys

import numpy as np
import matplotlib.pyplot as plt

from cc_pathlib import Path

src = Path(sys.argv[1])
assert src.suffix == '.json'

plt.figure()

f_map = src.load()
for k, c in [("brotli", 'tab:blue'), ("zstd", 'tab:red')] :
	s_lst = list()
	t_lst = list()
	m_map = f_map[k]
	for i in sorted(m_map, key=int) :
		s, t = m_map[i]
		s_lst.append(s)
		t_lst.append(t)
		plt.text(s, t[4], i)
	t_arr = np.array(t_lst)
	for j in range(9) :
		if j == 4 :
			plt.plot(s_lst, t_arr[:,j], 'x-', label=k, color=c)
		else :
			plt.plot(s_lst, t_arr[:,j], 'x-', alpha=1 / (0.2*(j-4)**2 + 1) , color=c)
	
plt.xlabel("size")
plt.ylabel("time")
plt.yscale('log')	
plt.legend()
plt.grid()
plt.show()
			
