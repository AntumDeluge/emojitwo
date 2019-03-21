
### List utilties.
#
# @package py.list_util


### Function to compare multiple strings.
#
# @local
# @function compareStrings
# @param strings
def hasDuplicates(*strings):
	# arguments may be str, list, or tuple
	strings_copy = []
	for I in strings:
		if type(I) in (list, tuple):
			for II in I:
				strings_copy.append(II)
		# anything else should be a string
		else:
			strings_copy.append(I)

	# FIXME: Check that all argument(s) values are strings

	# special strings
	for idx in range(len(strings_copy)):
		if strings_copy[idx].startswith('#!'):
			strings_copy[idx] = strings_copy[idx][2:]

	for current in strings_copy:
		if strings_copy.count(current) > 1:
			return True

	return False


### Checks for & removes duplicate strings from a list.
#
# @local
# @function removeDuplicates
# @param l List or tuple of items.
def removeDuplicates(l):
	list_copy = list(l)

	for idx in reversed(range(len(list_copy))):
		for I in list_copy:
			if list_copy.index(I) == idx:
				break

			if hasDuplicates(I, list_copy[idx]):
				list_copy.pop(idx)
				break

	return type(l)(list_copy)


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
