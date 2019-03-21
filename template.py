#!/usr/bin/env python

# This script is licensed on Creative Commons Zero (CC0).
# See: https://creativecommons.org/publicdomain/zero/1.0/


import os, sys

from py			import pyIsCompat
from py.paths	import dir_svg
from py.paths	import appendPath
from py.paths	import root as dir_root
from py.theme	import updateTemplate


def init():
	py_compat, py_ver = pyIsCompat()
	if not py_compat:
		print('\nERROR:\tUsing Python version {}. Version 3 or greater required.'.format(py_ver))
		sys.exit(1)


	# SVG input files
	svg_files = os.listdir(dir_svg)

	idx = len(svg_files) - 1
	while idx >= 0:
		if not svg_files[idx].lower().endswith('.svg'):
			svg_files.pop(idx)

		idx -= 1

	updateTemplate(appendPath(dir_root, 'theme.txt'), {'default': svg_files})


if __name__ == '__main__':
	init()
	print('\nDone!')