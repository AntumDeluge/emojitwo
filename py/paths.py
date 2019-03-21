
### Module for handling paths
#
# @package py.paths


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
