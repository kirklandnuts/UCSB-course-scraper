# Download libraries
import webbrowser, sys, pyperclip, requests, bs4

# First exercise: extract web URL
# To put into search bar

# Method 1
if len(sys.argv) > 1:
	# Get address from command line
	address = ' '.join(sys.argv[1:])

# Method 2
else:
	# Get address from clipboard
	# Here is address if necessary
	# 870 Valencia St, San Francisco, CA 94110
	address = pyperclip.paste()

print(address)
webbrowser.open('https://www.google.com/maps/place/' + address)


# Second exercise
# Downloading webpage with requests.get() function
# And write to a file
res = requests.get('http://www.gutenberg.org/cache/epub/1112/pg1112.txt')
print(type(res))
res.status_code == requests.codes.ok
res.raise_for_status()
print(len(res.text))
print(res.text[:250] + '\n')
playFile = open('RomeoAndJuliet.txt', 'wb')
for chunk in res.iter_content(100000):
	playFile.write(chunk)

playFile.close()

#
##
"""
To review, here’s the complete process for downloading and saving a file:
1. Call requests.get() to download the file.
2. Call open() with 'wb' to create a new file in write binary mode.
3. Loop over the Response object’s iter_content() method.
4. Call write() on each iteration to write the content to the file.
5. Call close() to close the file.
"""
##
#

# Third exercise
# Check for faulty websites
web = requests.get('http://inventwithpython.com/page_that_does_not_exist')
try:
	web.raise_for_status()
except Exception as exc:
	print('There was a problem: %s' %(exc))


# Fourth exercise
# Parse HTML website for data 
# First using a URL
web = requests.get('http://nostarch.com/')
web.raise_for_status()
noStarchSoup = bs4.BeautifulSoup(res.text, "html.parser")
print(type(noStarchSoup))

# Next if we supplied the HTML file
exampleFile = open('/Users/njfritter/myProjects/PSTAT131/PSTAT131HW1/PSTAT131HW1.html')
exampleSoup = bs4.BeautifulSoup(exampleFile, "html.parser")
print(type(exampleSoup))

# Extract div elements
"""
elems = exampleSoup.select('div')
print(type(elems))
print(len(elems))
soup.select('#author')
print(type(elems[0]))
soup.select('input[name]')
elems[0].getText()
print(str(elems[0]))
print(elems[0].attrs)
"""

# Extract paragraph elements
# HOLY FUCK IT WORKS
pElems = exampleSoup.select('p')
for i in range(0, 11):
	print(pElems[i])
	pElems[i].getText()

# Getting Data from an Element’s Attributes
h2Elem = exampleSoup.select('h2')[0]
print(str(h2Elem))
print(h2Elem.get('id'))
print(h2Elem.get('some_nonexistent_addr') == None)
print(h2Elem.attrs)

# Now show a whole bunch of h2 tags
for i in range(0, 5):
	print(h2Elem[i])
	h2Elem[i].getText()






