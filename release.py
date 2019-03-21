#!/usr/bin/env python

# This script is licensed on Creative Commons Zero (CC0).
# See: https://creativecommons.org/publicdomain/zero/1.0/


import os, shutil, sys

from generate_theme	import init as generateTemplate
from py			import pyIsCompat
from py.paths	import appendPath
from py.paths	import dir_export
from py.paths	import dir_release
from py.paths	import dir_svg
from py.paths	import root as dir_root
from py.util	import convertToPNG


py_compat, py_ver = pyIsCompat()
if not py_compat:
	print('\nERROR:\tUsing Python version {}. Version 3 or greater required.'.format(py_ver))
	sys.exit(1)


# remove old output files
if os.path.exists(dir_release):
	shutil.rmtree(dir_release)

# create output directory
os.makedirs(dir_export)

# SVG input files
svg_files = os.listdir(dir_svg)

idx = len(svg_files) - 1
while idx >= 0:
	if not svg_files[idx].lower().endswith('.svg'):
		svg_files.pop(idx)

	idx -= 1

svg_count = len(svg_files)
idx = 0

for SVG in svg_files:
	idx += 1
	sys.stdout.write('Converting SVG to PNG image ({}/{}): {}                         \r'.format(idx, svg_count, SVG))

	source = appendPath(dir_svg, SVG)
	target = appendPath(dir_export, '{}.png'.format(os.path.basename(SVG).split('.')[0]))

	convertToPNG(source, target)

# newline after converting files
print()

generateTemplate()

# copy theme file to release directory
theme_file = appendPath(dir_root, 'theme.txt')
shutil.copy(theme_file, appendPath(dir_export, 'theme'))

print('\nDone!')
