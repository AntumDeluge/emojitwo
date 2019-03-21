
### List utilties.
#
# @package py.list_util


### Function to clean whitespace list items.
#
# @function cleanList
# @param l
def cleanList(l):
	list_copy = list(l)

	idx = len(list_copy) - 1
	while idx >= 0:
		# clean leading/trailing whitespace
		list_copy[idx] = list_copy[idx].strip(' \t\r\n')

		# special lines
		if list_copy[idx].startswith('#!'):
			list_copy[idx] = '#!{}'.format(list_copy[idx][2:].lstrip(' \t'))

		if list_copy[idx] == '':
			list_copy.pop(idx)

		idx -= 1

	if type(l) == tuple:
		return tuple(list_copy)

	return list_copy


### Function to get first set of characters from a string.
#
# @function getFirtWord
# @tparam str string
def getFirstWord(string):
	return string.split(' ')[0].split('\t')[0]
