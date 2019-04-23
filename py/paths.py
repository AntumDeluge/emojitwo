
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
dir_svg = appendPath(root, 'svg')

# files
template_file = appendPath(root, 'template.txt')
file_license = appendPath(root, 'LICENSE.txt')
file_readme = appendPath(root, 'README.md')
