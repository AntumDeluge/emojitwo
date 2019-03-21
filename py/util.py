
### Utility functions.
#
# @package py.util


import subprocess

from py import WIN32


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
def convertToPNG(in_path, out_path):
	subprocess.Popen([cmd_convert, '-z', in_path, '-e', out_path])