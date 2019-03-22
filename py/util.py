
### Utility functions.
#
# @package py.util


import os, subprocess, sys
from zipfile import ZipFile

from py			import WIN32
from py			import info
from py.paths	import appendPath
from py.paths	import dir_release
from py.paths	import formatPath


### Retrieves number of words in a string separated by whitespace.
#
# @function getWordCount
# @tparam str string String to check.
# @treturn int
def getWordCount(string):
	w_list = []
	for W in string.replace('\t', ' ').split(' '):
		if W.strip():
			w_list.append(W)

	return len(w_list)


### Checks existence of command on system.
#
# @function getCommand
# @tparam str cmd
# @return Full path to executable or None.
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


# command to convert images
cmd_name = 'inkscape'
cmd_convert = getCommand(cmd_name)
if not cmd_convert:
	print('ERROR: "{}" command not found'.format(cmd_name))
	sys.exit(1)


### Converts SVG image to PNG for release.
#
# @function convertToPNG
# @tparam str in_path Location of source SVG.
# @tparam str out_path Location for target PNG.
# @tparam int width Width of exported PNG.
# @tparam int height Height of exported PNG.
def convertToPNG(in_path, out_path, width=None, height=None):
	args = ['--without-gui', '--file={}'.format(in_path),
		'--export-png={}'.format(out_path)]

	if width:
		args.append('--export-width={}'.format(width))
	if height:
		args.append('--export-height={}'.format(height))

	proc = subprocess.Popen(args, executable=cmd_convert)
	outs, errs = proc.communicate() # @UnusedVariable


### Compresses release into zip archive.
#
# @function compress
# @tparam bool dry_run If `True`, no action will be taken
def compress(dry_run=False):
	print('\nCreating zip distribution archive ...')

	t_name = info.getAttribute('name').lower()
	t_version = info.getAttribute('version')
	t_rel = t_name

	if t_version:
		t_rel = '{}-{}'.format(t_rel, t_version)

	t_zip = formatPath('{}.zip'.format(t_rel))

	file_list = []
	ret_dir = os.getcwd()
	os.chdir(dir_release)
	for ITEM in os.listdir(os.getcwd()):
		# ignore zip & hidden files
		if not ITEM.lower().endswith('.zip') and not ITEM.startswith('.'):
			if os.path.isfile(ITEM):
				file_list.append(ITEM)
				continue

			for ROOT, DIRS, FILES in os.walk(ITEM): # @UnusedVariable
				for F in FILES:
					file_list.append(appendPath(ROOT, F))

	if not dry_run:
		if os.path.exists(t_zip):
			os.remove(t_zip)

		Z = ZipFile(t_zip, 'w')
		for F in file_list:
			Z.write(F)
		Z.close()

	os.chdir(ret_dir)
