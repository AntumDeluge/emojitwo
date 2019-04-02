#!/usr/bin/env python

# This script is licensed on Creative Commons Zero (CC0).
# See: https://creativecommons.org/publicdomain/zero/1.0/


import os, shutil, sys

from py			import fileio
from py			import pyIsCompat
from py.cl		import args
from py.md		import markdownToText
from py.paths	import appendPath
from py.paths	import dir_release
from py.paths	import dir_svg
from py.paths	import file_license
from py.paths	import file_readme
from py.paths	import template_file
from py.theme	import copyTemplate
from py.theme	import getImagesToRemove
from py.theme	import getReleaseImages
from py.util	import compress
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

live_run = not args.contains('dry-run')
if not live_run:
	print('\nDry run: Not making any changes!\n')

if live_run:
	# create output directory
	os.makedirs(dir_release, exist_ok=True)

	if not args.contains('no-update-template') or not os.path.isfile(template_file):
		generateTemplate()

# default sizes (overridden with --sizes option)
sizes = ['16', '24']
if args.contains('size'):
	sizes = args.getValue('size', True)
else:
	sizes_copy = list(sizes[:-1])
	sizes_copy.append('and {}'.format(sizes[-1]))
	sizes_delim = ' '
	if len(sizes) > 2:
		sizes_delim = ', '
	print('\nCreating releases for image sizes {} pixels.'.format(sizes_delim.join(sizes_copy)))
	print('This can be changed by using the "--size" option.')

for S in sizes:
	# check that all sizes are numerical values
	try:
		int(S)
	except ValueError:
		print('\nERROR: "{}" is not a valid numerical value for argument "size".'.format(S))
		sys.exit(1)

# images to be included with release
include_all = args.contains('all-images')
release_images = getReleaseImages(all_images=include_all)
img_count = len(release_images)

# images that should be removed from release if found
remove_images = ()
if not include_all:
	remove_images = getImagesToRemove()

print('{} images will be included in release.'.format(img_count))

# prepare README for inclusion in release
readme_text = markdownToText(fileio.read(file_readme))

grp_count = len(sizes)
grp_idx = 0
for S in sizes:
	converted_count = 0
	replaced_count = 0
	removed_count = 0
	grp_idx += 1

	print('\nProcessing {}x{} images (group {}/{}) ...'.format(S, S, grp_idx, grp_count))

	idx = 0
	size_dir = appendPath(dir_release, '{}/emojitwo'.format(S))

	# check for previously generated release
	if remove_images and os.path.isdir(size_dir):
		print('\nChecking images from previous release ...')
		# images found in target release directory
		png_existing = os.listdir(size_dir)

		# exclude non-PNG files
		for p_idx in reversed(range(len(png_existing))):
			if not png_existing[p_idx].lower().endswith('.png'):
				png_existing.pop(p_idx)

		if not png_existing:
			print('... none found.')

		# check if files should not be included in release
		for PNG in png_existing:
			if PNG in remove_images:
				sys.stdout.write('Removing existing image from release: {}            \r'.format(PNG))
				if live_run:
					PNG = appendPath(size_dir, PNG)
					os.remove(PNG)
				removed_count += 1

	for img_name in release_images:
		idx += 1

		source = appendPath(dir_svg, '{}.svg'.format(img_name))
		target = appendPath(size_dir, '{}.png'.format(img_name))

		os.makedirs(size_dir, exist_ok=True)

		replace = os.path.isfile(target)

		# --force-update-png argument re-generates all PNG images
		if replace and not args.contains('update-png'):
			sys.stdout.write('Not updating PNG image ({}/{})          \r'.format(idx, img_count))
			continue

		if live_run:
			try:
				sys.stdout.write('Converting SVG to PNG image ({}/{}) (Ctrl+C to cancel)       \r'.format(idx, img_count))
				convertToPNG(source, target, S, S)
				if not os.path.isfile(target):
					print('\nERROR: SVG->PNG conversion failed.')
					sys.exit(1)
			except KeyboardInterrupt:
				print('\nProcess cancelled by user')
				sys.exit(0)

		converted_count += 1
		if replace:
			replaced_count += 1

	# newline after converting files
	print()

	print('\n{} new images added to release ({} updated).'.format(converted_count, replaced_count))
	if removed_count > 0:
		print('{} old images removed from release.'.format(removed_count))

	if live_run:
		copyTemplate(size_dir)
		shutil.copy(file_license, size_dir)
		fileio.write(appendPath(size_dir, 'README.txt'), readme_text)

if live_run:
	shutil.copy(file_license, dir_release)
	fileio.write(appendPath(dir_release, 'README.txt'), readme_text)

# create zip distribution archive
compress(not live_run)

print('\nDone!')
