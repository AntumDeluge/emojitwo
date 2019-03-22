
### Handles INFO file.
#
# @package py.info


from os.path import isfile

from py         import fileio
from py.paths   import appendPath
from py.paths   import root


info = {}
info_file = appendPath(root, 'INFO')


# parse the INFO file
lines = ()
if isfile(info_file):
	lines = tuple(fileio.read(info_file).split('\n'))
else:
	print('\nWARNING: INFO file not found: {}'.format(info_file))

# only recognize lines with "="
for idx in reversed(range(len(lines))):
	L = lines[idx]
	if L.startswith('#') or '=' not in L:
		continue

	key = L.split('=')
	value = key[1].strip(' \t')
	key = key[0].strip(' \t').lower()

	if key and value:
		info[key] = value


### Retrieves value of an attribute.
#
# @function getAttribute
# @tparam str key Key to search for.
# @treturn str Value of `key` if found or `None`.
def getAttribute(key):
	key = key.lower()
	if not key in info:
		return None

	return info[key]
