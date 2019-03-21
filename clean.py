#!/usr/bin/env python

# Deletes compiled Python bytecode files (.pyc).
#
# This script is licensed on Creative Commons Zero (CC0).
# See: https://creativecommons.org/publicdomain/zero/1.0/


import os, shutil, sys

root = os.path.dirname(sys.argv[0])

clean_dirs = (
	root,
	'{}/py'.format(root),
)

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
