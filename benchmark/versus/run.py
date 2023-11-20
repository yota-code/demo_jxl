#!/usr/bin/env python3

import os
import sys

from cc_pathlib import Path

jxl_root_dir = Path(os.environ['JXL_root_DIR']).resolve()

z_map = {
	'v6b87965_d3': ['6b87965', '-d', '3.0'],
	'v136cd81_d3': ['136cd81', '-d', '3.0'],
}

cwd = Path().resolve()

for arg in cwd / "img" / "__ref__" :
	for tst, (vrs, * pos) in z_map.items() :
		print(vrs, pos)
		exe = jxl_root_dir / "build" / f"native_{vrs}" / "tools"

		src = Path(arg).resolve()
		dir = (cwd / "img" / tst).make_dirs()
		tmp = dir / f"{src.fname}.jxl"
		dst = dir / f"{src.fname}.png"

		dir.run(exe / "cjxl", * pos, src, tmp)
		dir.run(exe / "djxl", tmp, dst)

		tmp.unlink()