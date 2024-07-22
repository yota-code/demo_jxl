#!/usr/bin/env python3

import os
import sys

from cc_pathlib import Path

jxl_dir = Path(os.environ["JXL_root_DIR"])
tst_dir = Path(sys.argv[1]).resolve()

assert (tst_dir / "src.png").is_file()

for version in ["v0.6.1", "v0.7.0", "v0.8.2", "v0.10.2"] :
	tst_dir.run(jxl_dir / "root" / "bin" / ("cjxl_" + version), '-d', '2.0', 'src.png', version + '.jxl')
	tst_dir.run(jxl_dir / "root" / "bin" / "djxl", version + '.jxl', version + '.png')
	
