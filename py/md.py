
### Markdown input handling.
#
# @package py.md


### Converts markdown formatted text to plain text.
#
# @function markdownToText
# @tparam str input Markdown formatted text.
# @treturn str Re-formatted input to plain text.
def markdownToText(md_in):
	print('\nFormatting README in plain text for release ...')

	txt_out = md_in

	# remove comments
	l = '<!--'
	r = '-->'
	while l in txt_out and r in txt_out and txt_out.index(l) < txt_out.index(r):
		idx_l = txt_out.index(l)
		idx_r = txt_out.index(r)

		txt_out = '{}{}'.format(txt_out[:idx_l], txt_out[idx_r+3:])

	# handle braces
	idx_l = txt_out.index('[')
	idx_r = txt_out.index(']')
	while '[' in txt_out and ('][' in txt_out or '](' in txt_out) and idx_l < idx_r:
		break

	# clean up leading & trailing whitespace on lines
	lines_out = txt_out.split('\n')
	for idx in range(len(lines_out)):
		# TODO: omit lines that begin with certain characters, such as lists
		lines_out[idx] = lines_out[idx].strip()
	txt_out = '\n'.join(lines_out)

	# clean up multiple empty lines in sequence
	while '\n\n\n' in txt_out:
		txt_out = txt_out.replace('\n\n\n', '\n\n')

	return txt_out
