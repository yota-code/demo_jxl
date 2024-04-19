#!/usr/bin/env python3

import sys

from cc_pathlib import Path

import same.scan
import same.grow

p = Path(sys.argv[1]).resolve()
u = same.scan.SameScan()
z_map = u.scan(p)

k = sorted(z_map).pop(0)

v = same.grow.SameGrow(u.img, z_map[k], u.block, u.block)

# p_lst = same.grow.PatchList([(2, 2)], 8, 8)
# for k in ["up", "left", "right", "down"] :
# 	print(k)
# 	v.p_lst = p_lst
# 	v.p_lst = v.p_lst.grow(k)
# 	v.plot()


# print(v.check())
# v.plot()
v.grow()
print("====")
print(v.check())
v.plot()