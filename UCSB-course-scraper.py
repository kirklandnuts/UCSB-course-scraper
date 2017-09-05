# ======================
# IMPORTS
# ======================
import bs4 as bs
import requests
import argparse
import os
import csv

# Define URL
URL = "https://my.sa.ucsb.edu/public/curriculum/coursesearch.aspx"

# Define class types to run this with
SUBJECTS = ["PSTAT",
            "MATH",
            "CMPSC"]

# Define quarters and corresponding numbers with it
QUARTERS = {"WINTER": 1,
            "SPRING": 2,
            "SUMMER": 3,
            "FALL": 4}


# ======================
# FUNCTIONS
# ======================
def get_session_info():
    '''
    this function makes aspx requests and returns the html response
        :param subject: one of "PSTAT", "MATH", or "CMPSC" (not case-sensitive)
        :param quarter: one of "SPRING", "SUMMER", "FALL", or "WINTER" (not case-sensitive)
        :param year: year of interest
        :param session_info: a dictionary containing session info required to make aspx request
        :return: html response from aspx request with arguments as query parameters
    '''

    headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    }

    # This part comes from:
    # https://github.com/hgielar/GOLD-schedule-exporter/blob/master/GOLD_Schedule_Tracker.py

    sesh = requests.Session() # create a session
    sesh.headers.update(headers) # load desired headers
    req = sesh.get(URL) # get response from URL
    content = bs.BeautifulSoup(req.content, "html.parser") # parse html response with BeautifulSoup

    # Scrape HTML to retrieve these values, will be used later on when logging in the first time
    # Using the first set of form data
    session_info = {}
    session_info['SESSION'] = sesh
    session_info['VIEWSTATE'] = content.find(id = "__VIEWSTATE")['value']
    session_info['VIEWSTATEGENERATOR'] = content.find(id = "__VIEWSTATEGENERATOR")['value']
    session_info['EVENTVALIDATION'] = content.find(id = "__EVENTVALIDATION")['value']
    session_info['KEYSandCOOKIES'] = sesh.cookies.get_dict()
    session_info['COOKIE'] = session_info['KEYSandCOOKIES']["ASP.NET_SessionId"]

    return session_info


def get_class_html(subject, quarter, year, session_info):
    '''
    this function makes aspx requests and returns the html response
        :param subject: one of "PSTAT", "MATH", or "CMPSC" (not case-sensitive)
        :param quarter: one of "SPRING", "SUMMER", "FALL", or "WINTER" (not case-sensitive)
        :param year: year of interest
        :param session_info: a dictionary containing session info required to make aspx request
        :return: html response from aspx request with arguments as query parameters
    '''
    # aspx form takes year and quarter in the form of a 5 digit integer
    #   the first 4 digits represent the year and the last digit represents the quarter
    #   1: winter, 2: spring, 3: summer, 4: fall
    # here, we convert accordingly
    full_number = int(str(year) + str(QUARTERS[quarter]))

    session_info = get_session_info()

    # Here we enter the fields of interest and necessary states
    # Classes, quarter, course levels
    formData = {b"__VIEWSTATE": session_info['VIEWSTATE'],
            b"__VIEWSTATEGENERATOR": session_info['VIEWSTATEGENERATOR'],
            b"__EVENTVALIDATION": session_info['EVENTVALIDATION'],
            b"__ASP.NET_SessionId": session_info['COOKIE'],
            b"ctl00$pageContent$courseList": subject,
            b"ctl00$pageContent$quarterList": full_number, # Represents 2017 and "fourth" quarter of year
            b"ctl00$pageContent$dropDownCourseLevels": "Undergraduate", # Undergrad classes
            b"ctl00$pageContent$searchButton.x": 24,
            b"ctl00$pageContent$searchButton.y": 7
    }

    session = session_info['SESSION']
    req2 = session.post(URL, data = formData)

    return req2


def output_to_csv(dept_courses, output_name):
    f = open(output_name, 'w')
    w = csv.DictWriter(f, dept_courses[0].keys())
    w.writeheader()
    w.writerows(dept_courses)
    f.close()


# precondition: the argument is a list of stripped strings (which is returned by get_rows())
# postcondition: the function returns a list of dicts, each dict containing all the elements of interest for each
#   course in the list
def extract_elements(row_list):
    courses = []
    for row in row_list:
        n_days = len(row[-5])
        if (n_days < 6) & (n_days > 1): # filtering out edge cases (canceled/special courses) as well as sections
            course = {}
            course['course_code'] = row[0]
            course['course_title'] = row[3]
            course['time'] = row[-4]
            course['location'] = row[-3]
            course['professor'] = row[-6]
            course['course_size'] = row[-2]
            course['days'] = row[-5]
            courses.append(course)
    return courses


# precondition: the first argument is the html file to be parsed
#   the second argument is a string representation of a dept to be passed into extract_elements
# postcondition: the function returns a list of lists each representing a course contained within the department
def get_rows(html_response):
    soup = bs.BeautifulSoup(html_response, 'html.parser')
    row_html_list = soup.select('tr[class="CourseInfoRow"]')
    row_list = []
    for row_html in row_html_list:
        row = list(row_html.stripped_strings)
        if row[-1]:
            row_list.append(row)
    return(row_list)


def courses_to_csv(quarter, year, session_info, output_dir):
    for subject in SUBJECTS:
        html_resp = get_class_html(subject, quarter, year, session_info)
        filename = subject + '-' + quarter + str(year) + '.csv'
        filepath = os.path.join(output_dir, filename)
        dept_dict = extract_elements(get_rows(html_resp.text))
        output_to_csv(dept_dict, filepath)
        print(subject , 'courses for', quarter, str(year), 'outputted to', filepath)

# ======================
# MAIN
# ======================
if __name__ == '__main__':
    print('UCSB Data Science Course Info Scraper\nDeveloped by NATHAN FRITTER and TIMOTHY NGUYEN\n' + '='*50)

    parser = argparse.ArgumentParser(description='Scrape UCSB\'s course listings and output data to CSV')
    parser.add_argument('quarter')
    parser.add_argument('year')
    parser.add_argument('-o', '--output_directory', default='.',
                        help = 'manually designate output file')

    args = parser.parse_args()
    quarter = args.quarter.upper()
    year = args.year
    out_dir = args.output_directory

    sesh = get_session_info()
    courses_to_csv(quarter, year, sesh, out_dir)
