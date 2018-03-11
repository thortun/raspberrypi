import urllib2 # Most URL-handeling happens here
import urllib # Downloading images from links
import re # For handeling the hyperref-mess

from math import ceil

def fix_line(line):
	"""Replaces '%' with '\%' and '\n' with '' so latex doesn't cry"""
	line = line.replace('%', '\%')
	line = line.replace('\n', '')
	return line

def clean_line(line):
	"""Crop all HTML-shit from a line."""
	# Firstly, remove newlines
	line = line.replace("\n", " ") 
	line = line.replace("\t", " ")
	line = line.replace("<p>", "")
	line = line.replace("</p>", "")
	line = line.replace("<i>", "")
	line = line.replace("</i>", "")
	line = line.replace("<h3>", "")
	line = line.replace("</h3>", "")
	line = line.replace("<h4>", "")
	line = line.replace("</h4>", "")
	line = line.replace("<strong>", "")
	line = line.replace("</strong>", "")
	line = line.replace("<em>", "")
	line = line.replace("</em>", "")
	line = line.replace("</a>", "")
	line = line.replace("<a>", "")	
	line = line.replace(">", "")
	# Remove excessive spaces
	line = line.replace("  ", " ")
	# Fix some comma-mistakes
	line = line.replace(", ,", ", ")
	return line

def crop_whites(line):
	"""Crops the whitespaces at the beginning and end of a line"""
	# Count from the start
	if len(line) == 0:
		return ""
	while line[0] == " ":
		line = line[1:]
	# From the end
	while line[len(line) - 1] == " ":
		line = line[:-1]

	return line

def typeset_line(line):
	"""Typesets correctly from HTML to LaTeX. For instance
	text between <strong> and </strong> becomes text inside
	\\textbf{}."""

	while '<strong>' in line and '</strong>' in line:
		start = line.find("<strong>")
		end = line.find("</strong>")
		# When we have the start and end of the things, split the string and typeset in between
		before_typeset = line[:start]
		between_typeset = line[(start + 8):end]
		after_typeset = line[(9 + end):]
		# Typeset
		line = before_typeset + "\\textbf{" + between_typeset + "}" + after_typeset

	while '<em>' in line and '</em>' in line:
		start = line.find("<em>")
		end = line.find("</em>")
		# When we have the start and end of the things, split the string and typeset in between
		before_typeset = line[:start]
		between_typeset = line[(start + 3):end]
		after_typeset = line[(end + 4):]
		# Typeset

		line = before_typeset + "\\textit{" + between_typeset + "}" + after_typeset
	# Because we replaced '/' with '_or_' to make the file handeling behave correctly
	# we need to revert this to make the spell look right again
	line = line.replace('_or_', '/')
	# And some more minor changes like that fact that % is the comment symbol in LaTeX
	line = line.replace('%', '\%')
	line = line.replace('#', '')
	# As of writing this, there is a mistake on the website, where 'Telekenesis' is
	# not done right in the HTML-code. Therefore we need to do this strange replacement
	line = line.replace('._**', '</strong>')
	line = line.replace('**', '<strong>')
	return line

def remove_hyperref2(line):
	"""Removes hyperref HTML-code and replaces it 
	with the proper word"""

	matches = []
	for match in re.finditer(r'std std-ref">([^<]+)</span>', line):
		matches.append(match.group(1))
	if len(matches) == 0:
		return line

	# Matches contains the words to insert
	k = 0
	found = False
	s = ''
	for i in xrange(0, len(line)):

		if line[i:(i + 8)] == '<a class':
			found = True

		if line[i:(i + 5)] == "/span":
			found = False
			s += matches[k]
			k += 1

		if not found:
			s += line[i]
	s = s.replace('/span></a>', '')
	return s

def extract_between(line, left, right, return_index = False):
	"""Extract all information between 'left' and 'right' in the string 'line'

	If optional parameter 'return_index' is True then we also return the index 
	where we found the extraction. This helps with placing the Actions
	header in the creature PDF.
	"""
	elements = [] # List containing all strings laying between 'left' and 'right'
	found = False # In the start we have yet to find a match for 'first'
	s = "" # Temporarry string to hold the stuff between left and right
	index_list = [] # A list of the index of where we found a match

	len_left = len(left)
	len_right = len(right)
	len_line = len(line)
	for i in xrange(0, len_line):
		# Search for the start left
		if line[i:(i + len_left)] == left:
			index_list.append(i) # Append the index where we found a match
			found = True

		# We only care wether we found a match for 'right' if we already have
		# a match for 'left'
		if line[i:(i + len_right)] == right and found:
			found = False # Next search
			elements.append(s) # Append
			s = "" # Clear temp string

		# We have found a match for our search, start adding it to a temporary string
		if found:
			s += line[i]

	# We have added a bit too much to the return-strings, namely
	# we started adding characters to the matches the second we found
	# the START of 'left' in the string, so we cut that away
	for i in xrange(0, len(elements)):
		elements[i] = elements[i][len(left):]

	# If there is only one element in the list, return this element, and 
	# if we are supposed to return the index list, we do that
	if len(elements) == 1:
		if return_index:
			return elements[0], index_list
		else:
			return elements[0]
	else:
		if return_index:
			return elements, index_list
		else:
			return elements

def extract_header_h1(string):
	"""Extracts the string information in the header
	in the HTML. This is the creature name for creatures
	and spell name for spells"""
	H = extract_between(string, "<h1>", "</h1>")
	name = ''
	for c in H:
		if c == '<':
			break
		else:
			name += c
	return name

def extract_header_h2(string, return_index = False):
	"""Extracts the string information in the sub-header
	h2 in the HTML. This is the 'actions' line for creatures
	"""
	if return_index:
		header_HTML, index = extract_between(string, "<h2>", "</h2>", True)
	else:
		header_HTML = extract_between(string, "<h2>", "</h2>")
	header = ''
	for c in header_HTML:
		if c == '<':
			break
		else:
			header += c
	if return_index:
		return header, index[0]
	else:
		return header

def contains_image(HTML_string):
	"""Returns a True if the HTML_string contains an image_file"""
	if len(extract_between(HTML_string, '<a class="reference external image-reference" href="/', '"><img alt="')) == 0:
		return False
	else:
		return True

def generate_HTML_string(url):
	hdr = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8','Connection': 'keep-alive'}
	req = urllib2.Request(url, headers=hdr)

	try:
	    page = urllib2.urlopen(req)
	except urllib2.HTTPError, e:
	    print e.fp.read()

	# Place all the data in a single string
	HTML_data = ""
	for line in page:
		HTML_data += crop_whites(line) # Remove excess white spaces
	return HTML_data

def save_creature_image(HTML_string):
	"""Extracts the image file and use urllib 
	to save the image to a folder"""
	# Extract the partial name of the image url
	image_url = extract_between(HTML_string, '<a class="reference external image-reference" href="/', '"><img alt="')
	# and then add the rest of the url
	creature_name = extract_between(image_url, '_images/', '.png')

	image_url = 'https://open5e.com/' + image_url
	urllib.urlretrieve(image_url, './CreatureImages/' + creature_name + '.png')

def replace(line):
	"""Replaces some common mistakes
	to avoid errors while moving files
	"""
	line = line.replace(' ', '_')
	line = line.replace(':', '')
	line = line.replace(',', '')
	line = line.replace('/', '_or_')
	return line