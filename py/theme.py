
### Theme file creation.
#
# @package py.theme


from py				import fileio
from py.list_util	import getFirstWord
from py.sb			import createStringBuilder


### Function to generate the new theme.
#
# @function updateTemplate
# @tparam str target Target ouput file.
# @tparam dict new_groups
# @tparam dict groups Groups found in existing theme file.
def updateTemplate(target, new_groups, groups):
	# SVG images are converted to PNG
	for G in new_groups:
		if type(new_groups[G]) != list:
			new_groups[G] = list(new_groups[G])

		for idx in range(len(new_groups[G])):
			new_groups[G][idx] = new_groups[G][idx].replace('.svg', '.png')

	for G in groups:
		if type(groups[G]) != list:
			groups[G] = list(groups[G])

	for g_name in new_groups:
		if g_name not in groups:
			print('Adding new group: {}'.format(g_name))
			groups[g_name] = list(new_groups[g_name])
		else:
			for g_item in new_groups[g_name]:
				add_item = True

				for g_existing in groups[g_name]:
					add_item = g_item != getFirstWord(g_existing)

					if not add_item:
						break

				if add_item:
					groups[g_name].append(g_item)

	# Check that all listed files have ".png" suffix
	warned = False
	for G in groups:
		for idx in range(len(groups[G])):
			item_basename = getFirstWord(groups[G][idx])
			if not item_basename.endswith('.png'):
				if not warned:
					print()
					warned = True

				print('WARNING: Listed image from group "{}" does not have .png suffix: {}'.format(G, item_basename))

	sb = createStringBuilder('Name=Emojitwo')
	sb.add('Description=Emojitwo smiley theme originally released as Emojione 2.2')
	sb.add('Icon=1f44d-1f3fd.png')
	sb.add('Author=')

	# default group
	sb.add('\n[default]')
	for IMG in groups['default']:
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
