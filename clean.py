#!/usr/bin/env python

# Deletes compiled Python bytecode files (.pyc).
#
# This script is licensed on Creative Commons Zero (CC0).
# See: https://creativecommons.org/publicdomain/zero/1.0/


import os, shutil, sys


root = os.path.dirname(sys.argv[0])

def init(args=None):
	release = args and ('--release' in args or 'release' in args)
	if release:
		print('\nCleaning release files ...')

		dir_release = '{}/release'.format(root)
		if os.path.isdir(dir_release):
			try:
				shutil.rmtree(dir_release)
			except PermissionError:
				print('\nERROR:\tCould not delete release directory: {}'.format(dir_release))
				print('\tCheck if you have write permission or if the\n\tfolder is locked by another process.')
				#sys.exit(1)
				return 1

		if os.path.exists(dir_release):
			print('\nERROR:\tCould not delete release directory: {}'.format(dir_release))
			#sys.exit(1)
			return 1

		#sys.exit(0)
		return 0

	clean_dirs = (
		root,
		'{}/py'.format(root),
	)

	print('\nCleaning compiled Python bytecode (.pyc) ...')
	for D in clean_dirs:
		# remove __pycache__ dir
		pycache = '{}/__pycache__'.format(D)
		if os.path.isdir(pycache):
			shutil.rmtree(pycache)

		# indivicual .pyc files
		for F in os.listdir(D):
			F = '{}/{}'.format(D, F)
			if os.path.isfile(F) and F.lower().endswith('.pyc'):
				os.remove(F)

	return 0


if __name__ == '__main__':
	ret = init(sys.argv[1:])
	sys.exit(ret)
