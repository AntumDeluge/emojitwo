
### Markdown input handling.
#
# @package py.md


### Converts markdown formatted text to plain text.
#
# @function markdownToText
# @tparam str input Markdown formatted text.
# @treturn str Re-formatted input to plain text.
def markdownToText(md_in):
	txt_out = md_in

	# handle braces
	idx_l = txt_out.index('[')
	idx_r = txt_out.index(']')
	while '[' in txt_out and ('][' in txt_out or '](' in txt_out) and idx_l < idx_r:
		break

	return txt_out
