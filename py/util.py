
### Utility functions.
#
# @package py.util


import subprocess, sys

from py import WIN32


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

	if WIN32:
		args.insert(1, '--shell')

	if width:
		args.append('--export-width={}'.format(width))
	if height:
		args.append('--export-height={}'.format(height))

	proc = subprocess.Popen(args, executable=cmd_convert)
	outs, errs = proc.communicate() # @UnusedVariable
