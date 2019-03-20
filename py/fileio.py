
###
#
# @package py.fileio


### Function to read file.
#
# @function read
# @param filename
def read(filename, encoding='utf-8'):
	BUFFER = open(filename, 'rt', encoding=encoding)
	text = BUFFER.read()
	BUFFER.close()

	# force LF line endings (\n)
	text.replace('\r\n', '\n').replace('\r', '\n')

	return text

### Function to write to file.
#
# @function write
# @param filename
# @param text
# @param encoding
def write(filename, text, encoding='utf-8'):
	# force LF line endings (\n)
	text = bytes(text, encoding)
	text.replace(b'\r\n', b'\n').replace(b'\r', b'\n')

	BUFFER = open(filename, 'wb')
	BUFFER.write(text)
	BUFFER.close()
