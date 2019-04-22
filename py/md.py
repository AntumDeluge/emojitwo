
### Markdown input handling.
#
# @package py.md


### Attempts to find value of a referenced link.
#
# @function getRefLink
# @tparam str label The label to search for.
# @tparam str search_text Text to search.
# @treturn str URL value or None.
def getRefLink(label, search_text):
	label = label.strip('[]')
	lines = search_text.split('\n')
	for L in lines:
		L = L.strip()
		if L.startswith('[') and ']:' in L:
			found = L[1:L.index(']:')]
			if found == label:
				url = L[L.index(']:')+2:].strip()
				return url

	return None


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

	# remove HTML code
	l = '<'
	r = '>'
	while l in txt_out and r in txt_out and txt_out.index(l) < txt_out.index(r):
		to_remove = txt_out[txt_out.index(l):txt_out.index(r)+1]
		txt_out = txt_out.replace(to_remove, '')

	# handle links
	for C in ('()', '[]',):
		CL = C[0]
		CR = C[1]

		count = txt_out.count(']{}'.format(CL))
		for I in range(count):
			idx_c = txt_out.index(']{}'.format(CL))
			idx_l = None
			idx_r = None

			# find left bracket
			idx = idx_c - 1
			while idx >= 0:
				if txt_out[idx] == '[':
					idx_l = idx
					break

				idx -= 1

			# find right brace
			idx = idx_c + 2
			while idx < len(txt_out):
				if txt_out[idx] == CR:
					idx_r = idx
					break

				idx += 1

			if idx_l and idx_r:
				to_replace = txt_out[idx_l:idx_r+1]

				tmp_text = to_replace[1:to_replace.index(']{}'.format(CL))].strip()
				tmp_url = to_replace[to_replace.index(']{}'.format(CL))+2:-1].strip()

				# parse reference
				if C == '[]' and tmp_url:
					tmp_url = getRefLink(tmp_url, txt_out)

				if tmp_url:
					txt_out = txt_out.replace(to_replace, '{} ( {} )'.format(tmp_text, tmp_url))
				else:
					txt_out = txt_out.replace(to_replace, tmp_text)

	lines_out = txt_out.split('\n')
	for idx in reversed(range(len(lines_out))):
		L = lines_out[idx]

		# clean up leading & trailing whitespace on lines
		# TODO: omit lines that begin with certain characters, such as lists
		L = L.strip()

		# remove reference links
		if L.startswith('[') and ']:' in L:
			lines_out.pop(idx)
			continue

		lines_out[idx] = L

	txt_out = '\n'.join(lines_out)

	# clean up multiple empty lines in sequence
	while '\n\n\n' in txt_out:
		txt_out = txt_out.replace('\n\n\n', '\n\n')

	return txt_out
