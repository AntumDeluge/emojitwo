
### Theme file creation.
#
# @package py.theme


import sys
from os.path import isfile

from py				import fileio
from py				import info
from py.list_util	import cleanList
from py.list_util	import getFirstWord
from py.paths		import appendPath
from py.paths		import template_file
from py.sb			import createStringBuilder
from py.util		import getWordCount


parsed_groups = False
t_groups = {}

### Function to parse existing template & extract groups.
#
# @local
# @function parseTemplate
# @tparam str template_file File to parse.
# @tparam bool force Forces re-parsing of template even if previously cached.
# @treturn dict Image groups found in template.
def parseTemplate(target=template_file, force=False):
	global parsed_groups

	if not parsed_groups or force:
		print('\nCaching image list from template ...')
		text = fileio.read(target)

		BUFFER = text
		while '[' in BUFFER and ']' in BUFFER:
			start = BUFFER.index('[') + 1
			end = BUFFER.index(']')

			g_name = BUFFER[start:end]
			BUFFER = BUFFER[end+1:]
			if '[' in BUFFER:
				group = tuple(BUFFER[:BUFFER.index('[')].rstrip(' \t\r\n').split('\n'))
			else:
				group = tuple(BUFFER.rstrip(' \t\r\n').split('\n'))

			t_groups[g_name] = cleanList(group)

		parsed_groups = True

	return t_groups


### Function to generate the new theme.
#
# @function updateTemplate
# @tparam str target Path to template file to be written/read.
# @tparam dict new_groups
def updateTemplate(target, new_groups):
	# groups that will be written to template
	groups = {}

	if isfile(target):
		print('Updating theme template ...')
		groups = parseTemplate(target)
	else:
		print('Creating new theme template ...')

	for G in groups:
		# ensure we are working with mutable groups
		if type(groups[G]) != list:
			groups[G] = list(groups[G])

	for G in new_groups:
		if type(new_groups[G]) != list:
			new_groups[G] = list(new_groups[G])

		for idx in range(len(new_groups[G])):
			# SVG images will be converted to PNG
			new_groups[G][idx] = new_groups[G][idx].replace('.svg', '.png')

		# clean up new groups
		new_groups[G] = cleanList(new_groups[G])

	for G in new_groups:
		if G not in groups:
			print('Adding new group: {}'.format(G))
			groups[G] = list(new_groups[G])
			continue

		# iterate through potential new items
		for I_N in new_groups[G]:
			add_item = True

			# check that the item does not already exist in the template
			for I_E in groups[G]:
				# lines beginning with "#!" denote items already exist in template
				# but will not be added release's theme file
				if I_E.startswith('#!'):
					I_E = I_E[2:]

				add_item = I_N != getFirstWord(I_E)
				if not add_item:
					break

			if add_item:
				groups[G].append(I_N)

	# check that all listed files have ".png" suffix
	warned = False
	for G in groups:
		for idx in range(len(groups[G])):
			item_basename = getFirstWord(groups[G][idx])
			if not item_basename.endswith('.png'):
				if not warned:
					print()
					warned = True

				print('WARNING: Listed image from group "{}" does not have .png suffix: {}'.format(G, item_basename))

	sb = createStringBuilder()

	t_name = info.getAttribute('name')
	t_descr = info.getAttribute('description')
	t_icon = info.getAttribute('icon')
	t_author = info.getAttribute('author')

	if t_name:
		sb.add('Name={}'.format(t_name))
	if t_descr:
		sb.add('Description={}'.format(t_descr))
	if t_icon:
		sb.add('Icon={}'.format(t_icon))
	if t_author:
		sb.add('Author={}'.format(t_author))

	# default group
	sb.add('\n[default]')
	for IMG in groups['default']:
		# add symbols
		if getWordCount(IMG) == 1 and IMG.endswith('.png'):
			try:
				tab_size = 4
				tab_groups = int(len(IMG) / tab_size)

				tabs = '\t\t\t\t\t'
				if tab_groups > 2:
					tabs = '\t'
				elif tab_groups < 2:
					tabs = '\t\t\t\t\t\t'

				char_code = int(IMG[:-4], 16)
				#IMG = '{}{}\\{}'.format(IMG, tabs, hex(char_code).lstrip('0'))
				IMG = '{}{}{}'.format(IMG, tabs, chr(char_code))
			except ValueError:
				pass

		# mark images without character to not be included in release
		if getWordCount(IMG) == 1 and not IMG.startswith('#!'):
			IMG = '#!{}'.format(IMG)

		sb.add(IMG)

	for G in groups:
		if G != 'default':
			sb.add('\n[{}]'.format(G))
			for IMG in groups[G]:
				sb.add(IMG)

	# extra newline at end of file
	sb.add('')

	# output to target file
	fileio.write(target, sb.toString('\n'))


### Gets a list of images that should be included in release.
#
# @function getReleaseImages
# @param include Image groups to be included in release
# @tparam bool all_images If `True`, will not ignore lines beginning with "#!".
# @treturn list Images that should be converted & added to release.
def getReleaseImages(include='default', all_images=False):
	image_list = []
	image_groups = parseTemplate()

	if type(include) == str:
		# asterix means include all groups of images
		if include == '*':
			for G in image_groups:
				for IMG in image_groups[G]:
					if IMG not in image_list:
						image_list.append(IMG)
		else:
			if include not in image_groups:
				sys.stderr.write('\nERROR: "{}" image group not found in template.\n'.format(include))
				sys.exit(1)

			image_list = list(image_groups[include])

	for idx in reversed(range(len(image_list))):
		IMG = image_list[idx].strip(' \t').replace('\t', ' ').split(' ')[0]

		# only working with PNG image type
		if not IMG.lower().endswith('.png'):
			image_list.pop(idx)
			continue

		if IMG.startswith('#!'):
			# lines beginning with "#!" are ignored unless `all_images` is set to `True`
			if not all_images:
				image_list.pop(idx)
				continue

			IMG = IMG[2:]

		IMG = IMG[:-4]
		image_list[idx] = IMG

	return tuple(image_list)


### Creates theme file from template for release.
#
# @function copyTemplate
# @tparam str target_dir Directory where release theme file should be created.
def copyTemplate(target_dir):
	template = fileio.read(template_file)
	target = appendPath(target_dir, 'theme')

	# ignore lines beginning with "#!"
	lines = template.split('\n')
	for idx in reversed(range(len(lines))):
		if lines[idx].startswith('#!'):
			lines.pop(idx)

	template = '\n'.join(lines)
	fileio.write(target, template)
