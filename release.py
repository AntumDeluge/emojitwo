#!/usr/bin/env python

# This script is licensed on Creative Commons Zero (CC0).
# See: https://creativecommons.org/publicdomain/zero/1.0/


import os, sys

from py			import pyIsCompat
from py.cl		import args
from py.paths	import appendPath
from py.paths	import dir_release
from py.paths	import dir_svg
from py.paths	import template_file
from py.theme	import copyTemplate
from py.util	import convertToPNG
from template	import init as generateTemplate


py_compat, py_ver = pyIsCompat()
if not py_compat:
	print('\nERROR:\tUsing Python version {}. Version 3 or greater required.'.format(py_ver))
	sys.exit(1)


if args.contains('clean'):
	# use condition to prevent IDE from organizing import
	if True: import clean

	sys.exit(clean.init(args.getValue('clean', True)))

# create output directory
os.makedirs(dir_release, exist_ok=True)

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
if not live_run:
	print('\nDry run: Not making any changes ...\n')

if live_run and (not args.contains('no-update-template') or not os.path.isfile(template_file)):
	generateTemplate()

# default size is 32x32
sizes = ['32']
if args.contains('size'):
	sizes = args.getValue('size', True)

for S in sizes:
	# check that all sizes are numerical values
	try:
		int(S)
	except ValueError:
		print('\nERROR: "{}" is not a valid numerical value for argument "size".'.format(S))
		sys.exit(1)

for S in sizes:
	size_dir = appendPath(dir_release, '{}/emojitwo'.format(S))

	for SVG in svg_files:
		idx += 1

		img_name = os.path.basename(SVG).split('.')[0]
		source = appendPath(dir_svg, SVG)
		target = appendPath(size_dir, '{}.png'.format(img_name))

		os.makedirs(size_dir, exist_ok=True)

		if os.path.isfile(target) and not args.contains('update_png'):
			sys.stdout.write('Not updating {}x{} PNG: {}                          \r'.format(S, S, img_name))
			continue

		if live_run:
			try:
				sys.stdout.write('Converting SVG to {}x{} PNG image ({}/{}) (Ctrl+C to cancel)       \r'.format(S, S, idx, svg_count))
				convertToPNG(source, target, S, S)
				if not os.path.isfile(target):
					print('\nERROR: SVG->PNG conversion failed.')
					sys.exit(1)
			except KeyboardInterrupt:
				print('\nProcess cancelled by user')
				sys.exit(0)

	copyTemplate(size_dir)

# newline after converting files
print()

print('\nDone!')
