# This code is taken from
# http://stackoverflow.com/questions/1480356/how-to-submit-query-to-aspx-page-in-python
# Import various libraries
import urllib, bs4, requests
#import urllib2

url = "https://my.sa.ucsb.edu/public/curriculum/coursesearch.aspx"

# Need to put in the User-Agent
# May need to have this changed everytime
headers = {
  "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
  "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
}

# This part comes from:
# https://github.com/hgielar/GOLD-schedule-exporter/blob/master/GOLD_Schedule_Tracker.py

# First make a session
# Then Put in the specific headers
# Enter the URL
# Then extract the HTML output using the html.parser

sesh = requests.Session()
sesh.headers.update(headers)
req = sesh.get(url)
content = bs4.BeautifulSoup(req.content, "html.parser")

# Scrape HTML to retrieve these values, will be used later on when logging in the first time
# Using the first set of form data
VIEWSTATE = content.find(id = "__VIEWSTATE")['value']
VIEWSTATEGENERATOR = content.find(id = "__VIEWSTATEGENERATOR")['value']
EVENTVALIDATION = content.find(id = "__EVENTVALIDATION")['value']

formData = (
   # Here are the fields of interest
   # Classes, quarter, course levels

   ("__VIEWSTATE", VIEWSTATE),
   ("__VIEWSTATEGENERATOR", VIEWSTATEGENERATOR),
   ("__EVENTVALIDATION", EVENTVALIDATION),
   #("__ASP.NET_SessionId", ),
   ('ctl00$pageContent$courseList', 'PSTAT'),
   #(r'ctl00$pageContent$courseList', 'MATH')
   #(r'ctl00$pageContent$courseList', 'CMPSC')
    # Pick out the subjects we want to take
   ('ctl00$pageContent$quarterList', 20174), # Represents 2017 and "fourth" quarter of year
   ('ctl00$pageContent$dropDownCourseLevels', 'Undergraduate'), # Undergrad classes
   ('ctl00$pageContent$searchButton.x', 24),
   ('ctl00$pageContent$searchButton.y', 7),
)




# These have to be encoded    
# encodedFormData = urllib.parse.urlencode(formData)

"""
req = urllib2.Request(uri, encodedFields, headers)
# Here is the actual call to the http site.
f = urllib2.urlopen(req)   
"""  


#req2 = sesh.post(url, data = formData)
#print(type(req2))
keyzNCookies = sesh.cookies.get_dict()
print(keyzNCookies)
COOKIE = keyzNCookies["ASP.NET_SessionId"]
print(COOKIE)

formData2 = {b"__VIEWSTATE": VIEWSTATE,
            b"__VIEWSTATEGENERATOR": VIEWSTATEGENERATOR,
            b"__EVENTVALIDATION": EVENTVALIDATION,
            b"__ASP.NET_SessionId": COOKIE,
            b"ctl00$pageContent$courseList": "PSTAT",
            b"ctl00$pageContent$quarterList": 20174, # Represents 2017 and "fourth" quarter of year
            b"ctl00$pageContent$dropDownCourseLevels": "Undergraduate", # Undergrad classes
            b"ctl00$pageContent$searchButton.x": 24,
            b"ctl00$pageContent$searchButton.y": 7
}

# req = sesh.post(url, data = formData)
# text = sesh.get() 
req3 = sesh.post(url, data = formData2)

listOfClasses = bs4.BeautifulSoup(req3.text, "html.parser")
print((listOfClasses))


# IF YOU GET AN SSL CERTIFICATE ERROR FOLLOW BELOW:
# http://stackoverflow.com/questions/42098126/mac-osx-python-ssl-sslerror-ssl-certificate-verify-failed-certificate-verify

classHTML = listOfClasses.contents
for line in classHTML:
    print(line)

prettyHTML = listOfClasses.prettify("utf-8")
with open("classList.html", "wb") as finalFile:
    finalFile.write(prettyHTML)
