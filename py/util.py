
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
