
### Modules for helper Python scripts.
#
# @package py


import sys


WIN32 = sys.platform == 'win32'


### Checks if using version 3 or greater of Python interpreter.
#
# @function pyIsCompat
# @return bool
def pyIsCompat():
	return sys.version_info[0] >= 3, sys.version_info[0]
