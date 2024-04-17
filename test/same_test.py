#!/usr/bin/env python3

import sys

from cc_pathlib import Path

import same.scan

p = Path(sys.argv[1]).resolve()
u = same.scan.SameScan()
r = u.scan(p)
