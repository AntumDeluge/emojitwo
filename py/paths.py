
### Module for handling paths
#
# @package py.paths


import sys
from os.path import dirname

from py import WIN32


### Converts node indicators for platform.
#
# @function formatPath
# @tparam str path
def formatPath(path):
	if WIN32:
		path = path.replace('/', '\\\\')
		while '\\\\\\\\' in path:
			path = path.replace('\\\\\\\\', '\\\\')
	else:
		path = path.replace('\\', '/').replace('//', '/')
		while '//' in path:
			path = path.replace('//', '/')

	return path


### Concatenates two path strings together.
#
# @function appendPath
# @tparam str p1
# @tparam str p2
# @treturn str
def appendPath(p1, p2):
	appended = '{}/{}'.format(p1, p2).replace('//', '/')
	return formatPath(appended)


# directory from where the script is launched
root = dirname(formatPath(sys.argv[0]))

# source & target directories
dir_release = appendPath(root, 'release')
dir_export = appendPath(dir_release, 'emojitwo')
dir_svg = appendPath(root, 'svg')
