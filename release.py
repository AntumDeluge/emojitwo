#!/usr/bin/env python

# This script is licensed on Creative Commons Zero (CC0).
# See: https://creativecommons.org/publicdomain/zero/1.0/


import os, sys

from py			import pyIsCompat
from py.cl		import args
from py.paths	import appendPath
from py.paths	import dir_export
from py.paths	import dir_svg
from py.theme	import copyTemplate
from py.util	import convertToPNG
from template	import init as generateTemplate


py_compat, py_ver = pyIsCompat()
if not py_compat:
	print('\nERROR:\tUsing Python version {}. Version 3 or greater required.'.format(py_ver))
	sys.exit(1)


# create output directory
os.makedirs(dir_export, exist_ok=True)

# SVG input files
svg_files = os.listdir(dir_svg)

idx = len(svg_files) - 1
while idx >= 0:
	if not svg_files[idx].lower().endswith('.svg'):
		svg_files.pop(idx)

	idx -= 1

svg_count = len(svg_files)
idx = 0

live_run = not args.contains('dry_run')

for SVG in svg_files:
	idx += 1
	sys.stdout.write('Converting SVG to PNG image ({}/{}): {}                         \r'.format(idx, svg_count, SVG))

	source = appendPath(dir_svg, SVG)
	target = appendPath(dir_export, '{}.png'.format(os.path.basename(SVG).split('.')[0]))

	if os.path.isfile(target) and not args.contains('update_png'):
		print('Not updating PNG: {}'.format(target))
		continue

	if live_run:
		try:
			convertToPNG(source, target)
			if not os.path.isfile(target):
				print('\nERROR: SVG->PNG conversion failed.')
				sys.exit(1)
		except KeyboardInterrupt:
			print('\nProcess cancelled by user')
			sys.exit(0)

# newline after converting files
print()

if live_run:
	generateTemplate()

copyTemplate(dir_export)

print('\nDone!')
