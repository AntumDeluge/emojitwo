
### String builder functions
#
# @package py.sb


### StringBuilder class
#
# @class StringBuilder
class StringBuilder:
	def __init__(self, strings=None):
		self.Strings = []

		if strings:
			if type(strings) == str:
				self.Strings.append(strings)
			elif type(strings) in (list, tuple):
				self.Strings = list(strings)

	def insert(self, idx, string):
		self.Strings.insert(idx, string)

	def prepend(self, string):
		self.Strings.insert(0, string)

	def append(self, string):
		self.Strings.append(string)

	def add(self, string):
		return self.append(string)

	def toString(self, delim=None):
		if delim:
			return delim.join(self.Strings)
		else:
			return ''.join(self.Strings)

	def clear(self):
		self.Strings = []


### Function to create a new stringbuilder object.
#
# @function createStringBuilder
# @return new stringbuilder object
def createStringBuilder(strings=None):
	return StringBuilder(strings)
