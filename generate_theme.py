#!/usr/bin/env python

import os, shutil, subprocess, sys

from py				import fileio
from py.list_util	import cleanList
from py.theme		import createThemeFile


if sys.version_info[0] < 3:
	print('\nERROR:\tUsing Python version {}. Version 3 or greater required.'.format(sys.version_info[0]))
	sys.exit(1)


WIN32 = sys.platform == 'win32'

def convertPath(path):
	if WIN32:
		path = path.replace('/', '\\\\')
		while '\\\\\\\\' in path:
			path = path.replace('\\\\\\\\', '\\\\')
	else:
		path = path.replace('\\', '/').replace('//', '/')
		while '//' in path:
			path = path.replace('//', '/')

	return path

def appendPath(p1, p2):
	appended = '{}/{}'.format(p1, p2).replace('//', '/')
	return convertPath(appended)

def getCommand(cmd):
	cmd_path = None

	try:
		if WIN32:
			cmd_list = subprocess.check_output(['where', cmd]).decode('utf-8').strip().split('\r\n')

			for CMD in cmd_list:
				if CMD.endswith('.exe'):
					cmd_path = CMD
					break
		else:
			cmd_path = subprocess.check_output(['which', cmd]).decode('utf-8').strip()
	except subprocess.CalledProcessError:
		cmd_path = None

	return cmd_path

def convertToPNG(in_path, out_path):
	subprocess.Popen([cmd_convert, '-z', in_path, '-e', out_path])

dir_root = convertPath(os.path.dirname(sys.argv[0]))
dir_release = appendPath(dir_root, 'release')
dir_export = appendPath(dir_release, 'emojitwo')
dir_svg = appendPath(dir_root, 'svg')

# command to convert images
cmd_name = 'inkscape'
cmd_convert = getCommand(cmd_name)
if not cmd_convert:
	print('ERROR: "{}" command not found'.format(cmd_name))
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

theme_file = appendPath(dir_root, 'theme.txt')

groups = {}
if os.path.isfile(theme_file):
	print('Reading existing theme file ...')

	theme_text = fileio.read(theme_file)

	BUFFER = theme_text
	while '[' in BUFFER and ']' in BUFFER:
		start = BUFFER.index('[') + 1
		end = BUFFER.index(']')

		g_name = BUFFER[start:end]
		BUFFER = BUFFER[end+1:]
		if '[' in BUFFER:
			group = tuple(BUFFER[:BUFFER.index('[')].rstrip(' \t\r\n').split('\n'))
		else:
			group = tuple(BUFFER.rstrip(' \t\r\n').split('\n'))

		groups[g_name] = cleanList(group)

print('Creating new theme file ...')
createThemeFile(theme_file, {'default': svg_files}, groups)
# copy theme file to release directory
shutil.copy(theme_file, appendPath(dir_export, 'theme'))

print('\nDone!')
