# This code is taken from
# http://stackoverflow.com/questions/1480356/how-to-submit-query-to-aspx-page-in-python
# Import various libraries
import urllib, bs4, requests
#import urllib2

url = "https://my.sa.ucsb.edu/public/curriculum/coursesearch.aspx"

#the http headers are useful to simulate a particular browser (some sites deny
#access to non-browsers (bots, etc.)
#also needed to pass the content type. 
"""
headers = {
    'HTTP_USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
    'HTTP_ACCEPT': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Content-Type': 'application/x-www-form-urlencoded'
}
"""
headers = {
  "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
  "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
  
}

# we group the form fields and their values in a list (any
# iterable, actually) of name-value tuples.  This helps
# with clarity and also makes it easy to later encoding of them.

# This part comes from:
# https://github.com/hgielar/GOLD-schedule-exporter/blob/master/GOLD_Schedule_Tracker.py
sesh = requests.Session()
sesh.headers.update(headers)
req = sesh.get(url)
content = bs4.BeautifulSoup(req.content, "html.parser")
# Scrape HTML to retrieve these values, will be used later on when logging in
VIEWSTATE = content.find(id = "__VIEWSTATE")['value']
VIEWSTATEGENERATOR = content.find(id = "__VIEWSTATEGENERATOR")['value']
EVENTVALIDATION = content.find(id = "__EVENTVALIDATION")['value']


formData = (
   # Here are the fields of interest
   # Classes, quarter, course levels

   ("__VIEWSTATE", VIEWSTATE),
   ("__VIEWSTATEGENERATOR", VIEWSTATEGENERATOR),
   ("__EVENTVALIDATION", EVENTVALIDATION),
   ('ctl00$pageContent$courseList', 'PSTAT'),
   #(r'ctl00$pageContent$courseList', 'MATH')
   #(r'ctl00$pageContent$courseList', 'CMPSC')
    # Pick out the subjects we want to take
   ('ctl00$pageContent$quarterList', 20174), # Represents 2017 and "fourth" quarter of year
   ('ctl00$pageContent$dropDownCourseLevels', 'Undergraduate'), # Undergrad classes
   ('ctl00$pageContent$searchButton.x', 24),
   ('ctl00$pageContent$searchButton.y', 7),
)


formData2 = {b"__VIEWSTATE": VIEWSTATE,
            b"__VIEWSTATEGENERATOR": VIEWSTATEGENERATOR,
            b"__EVENTVALIDATION": EVENTVALIDATION,
            b"ctl00$pageContent$courseList": "PSTAT",
            b"ctl00$pageContent$quarterList": 20174, # Represents 2017 and "fourth" quarter of year
            b"ctl00$pageContent$dropDownCourseLevels": "Undergraduate", # Undergrad classes
            b"ctl00$pageContent$searchButton.x": 24,
            b"ctl00$pageContent$searchButton.y": 7
}

# These have to be encoded    
# encodedFormData = urllib.parse.urlencode(formData)

"""
req = urllib2.Request(uri, encodedFields, headers)
# Here is the actual call to the http site.
f = urllib2.urlopen(req)   
"""  


req = sesh.post(url, data = formData)
# text = sesh.get() 
print(type(req)) 

class_info = bs4.BeautifulSoup(req.text, "html.parser")
print(type(class_info))

html_text = urllib.request.urlopen(url, data = formData2)

# IF YOU GET AN SSL CERTIFICATE ERROR FOLLOW BELOW:
# http://stackoverflow.com/questions/42098126/mac-osx-python-ssl-sslerror-ssl-certificate-verify-failed-certificate-verify

# *** here would normally be the in-memory parsing of f 
#     contents, but instead I store this to file
#     this is useful during design, allowing to have a
#     sample of what is to be parsed in a text editor, for analysis.

try:
  fout = open('tmp.html', 'wb')
except:
  print('Could not open output file\n')

fout.writelines(html_text.readlines())
fout.close()
