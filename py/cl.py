
### Command line handling.
#
# @package py.cl


import sys
from os.path import basename

from py.sb import createStringBuilder



# usage output
script_name = basename(sys.argv[0])
if script_name.lower().endswith('.py'):
	script_name = script_name[:-3]
usage = createStringBuilder('Description\n\tHelper script for creating release.')
usage.append('\nUsage:\n\t{} [options]'.format(script_name))


### Prints usage text to stdout.
#
# @function showUsage
def showUsage():
	print('\n{}'.format(usage.toString('\n')))


### Arguments object.
#
# @class ArgsObject
class ArgsObject:
	def __init__(self):

		### Recognized arguments.
		#
		# Argument keys ending with "=" can have a value.
		# If value is not required, tuple must have third
		# option as default.
		#
		# Format:
		#    <base key>[=]: {'keys': (<short key>, <long key>), <'takes_value'>: <bool>, [<'default'>: <default value>]}
		self.Registered = {}

		### List of valid arguments input from command line.
		self.Input = {}

		# initialize argument list
		#self.parseArgs()


	# *** methods for internal use ***


	### Checks if a key argument is recognized by the system.
	#
	# @method isValid
	# @tparam str key Argument string to check.
	# @treturn bool `True` if found in valid arguments list.
	def isValid(self, key):
		return self.getBaseKey(key) != None

	### Retrieves the base key argument string.
	#
	# @method getBaseKey
	# @tparam str key Long or short key representation.
	# @treturn str String represeting the base key.
	def getBaseKey(self, key):
		for V in self.Registered:
			if key in self.Registered[V]['keys']:
				return V

		return None

	### Checks if key argument takes a value
	#
	# @method takesValue
	# @tparam str key Argument string to check.
	# @treturn bool `True` if key takes a value argument.
	def takesValue(self, key):
		return self.Registered[key]['takes_value']

	### Checks if key argument has a default value.
	#
	# @method requiresValue
	# @tparam str key Argument string to check.
	# @treturn bool `True` if a default value is not found.
	def requiresValue(self, key):
		return self.takesValue(key) and 'default' not in self.Registered[key]

	### Checks if any arguments were supplied.
	#
	# @method hasArgs
	# @treturn bool `True` if argument list is not empty.
	def hasArgs(self):
		return len(self.Input) > 0

	### Checks of key has a default value.
	#
	# @method hasDefaultValue
	# @tparam str key Key name to parse.
	# @treturn bool `True` if default string is found.
	def hasDefaultValue(self, key):
		return 'default' in self.Registered[key]

	### Retrieves default value of key.
	#
	# @method getDefaultValue
	# @tparam str key Key name to parse.
	# @treturn str Default string value or `None`.
	def getDefaultValue(self, key):
		if not self.takesValue(key) or not self.hasDefaultValue(key):
			return None

		return self.Registered[key]['default']


	# *** methods for public use ***


	### Registers a key with valid args list.
	#
	# Note: parseArgs method must be called AFTER registering keys.
	#
	# @method registerKey
	# @tparam str key String representation of base key name.
	# @tparam str k_short Short string representation.
	# @tparam str k_long Long string representation.
	# @tparam bool takes_value Whether or not this should be a key=value argument.
	# @param default Default value if not supplied from command input (`None` forces
	#	value to be explicitly declared).
	# @tparam str descr Optional description for usage information.
	def registerKey(self, key, k_short=None, k_long=None, takes_value=False, default=None, descr=None):

		def showMessage(msg, err=True):
			out = sys.stderr
			err_line = 'KeyRegisterError'
			if not err:
				out = sys.stdout
				err_line = 'KeyRegisterWarning'

			out.write('{} ({}): {}\n'.format(err_line, key, msg))

		if not k_short and not k_long:
			showMessage('Cannot register key without either short or long value.')
			sys.exit(1)

		if k_short and len(k_short) > 1:
			showMessage('Short value must be a single character.')
			sys.exit(1)

		if k_long and len(k_long) < 2:
			showMessage('Long value should be more than one character')
			sys.exit(1)

		for K in (k_short, k_long):
			if K and K.startswith('-'):
				showMessage('Cannot register long or short key beginning with dashes ("-").')
				sys.exit(1)

		# check for duplicates
		if key in self.Registered:
			showMessage('Cannot register duplicate key.')
			sys.exit(1)
		for R in self.Registered:
			if k_short and k_short == self.Registered[R]['keys'][0]:
				showMessage('Cannot register duplicate short key: {}'.format(k_short))
				sys.exit(1)
			if k_long and k_long == self.Registered[R]['keys'][1]:
				showMessage('Cannot register duplicate long key: {}'.format(k_long))
				sys.exit(1)

		self.Registered[key] = {'keys': (k_short, k_long), 'takes_value': takes_value,}
		if default:
			if takes_value:
				self.Registered[key]['default'] = default
			else:
				showMessage('Ignoring default value supplied with non-value key.', False)
		if descr:
			self.Registered[key]['description'] = descr

	### Parses command line input.
	#
	# @method parseArgs
	def parseArgs(self):
		arg_list = sys.argv[1:]

		for idx in range(len(arg_list)):
			arg = arg_list[idx]

			key_long = False
			key_short = len(arg) == 2 and arg.startswith('-') and arg.count('-') == 1
			if not key_short:
				key_long = arg.startswith('--') and not arg[2:].startswith('-')

			valid_key = True
			if not key_short and not key_long:
				valid_key = False

			if valid_key:
				key = self.getBaseKey(arg.lstrip('-'))
				if not key:
					valid_key = False
				else:
					if self.takesValue(key):
						# FIXME:
						print('Key takes value: {} (default: {})'.format(key, self.getDefaultValue(key)))
						if self.requiresValue(key):
							print('Key requires value: {}'.format(key))
					else:
						self.Input[key] = None

			if not valid_key:
				print('\nERROR: Invalid argument: {}'.format(arg))
				showUsage()
				sys.exit(1)

	### Retrieves string representation of arguments.
	#
	# TODO:
	#
	# @method toString
	# @treturn str
	def toString(self):
		sb = createStringBuilder()

		for R in self.Registered:
			arg = self.Registered[R]
			k_short = arg['keys'][0]
			k_long = arg['keys'][1]

			tmp = createStringBuilder()
			if k_short:
				tmp.append('-{}'.format(k_short))
			if k_long:
				tmp.append('--{}'.format(k_long))

			tmp.joinStrings(' | ')

			descr = self.getDescription(R)
			if descr:
				tmp.append(descr)

			# TODO: align descriptions agains longest line
			#sb.append(tmp.toString('<#!>'))
			sb.append(tmp.toString('\t'))

		return sb.toString('\n')

	### Retrieves value of key.
	#
	# @method getValue
	# @tparam str key Key name to parse.
	# @return Value for key or None.
	def getValue(self, key):
		return self.Input[key]

	### Retrieves argument description.
	#
	# @method getDescription
	# @tparam str key Key name to parse.
	# @return Description string or `None`.
	def getDescription(self, key):
		if 'description' not in self.Registered[key]:
			return None

		return self.Registered[key]['description']

	### Checks command line input for key.
	#
	# @method contains
	# @tparam str key Key argument to check for.
	# @treturn `True` if `key` was added to the argument list.
	def contains(self, key):
		return key in self.Input


# arguments supplied from the command line
args = ArgsObject()
args.registerKey('help', 'h', 'help', descr='Show this usage information.')
args.registerKey('update_png', 'f', 'force-update-png', descr='Existing PNG images will be overitten with new ones.')
args.registerKey('dry_run', 'd', 'dry-run', descr='No action is taken.')

# usage info can be updated after keys are registered
usage.append('\nOptions:')
opts_string = '\t{}'.format(args.toString().replace('\n', '\n\t'))
usage.append(opts_string)

# initialize command line input
args.parseArgs()

# immediately check for help argument
if args.contains('help'):
	showUsage()
	sys.exit(0)
