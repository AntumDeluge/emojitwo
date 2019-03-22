
### Command line handling.
#
# @package py.cl


import sys


# arguments supplied from the command line
args = tuple(sys.argv[1:])


### Checks if arguments were supplied.
#
# @function hasArgs
# @treturn bool `True` if the argument list is not empty.
def hasArgs():
	return len(args) > 0


### Checks if an argument was supplied.
#
# @function argsContain
# @tparam str key Argument to check for.
# @tparam[opt] short If `True`, check for short arguments beginning with a single dash.
# @treturn bool `True` if `key` is found in the arguments list.
def argsContain(key, short=False):
	if not hasArgs():
		return False

	if short and len(key) == 1:
		return '-{}'.format(key) in args

	return '--{}'.format(key) in args
