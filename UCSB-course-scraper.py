# ======================
# IMPORTS
# ======================
import bs4 as bs
import requests
import argparse
import os
import csv
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from tqdm import trange

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
    """
    this function sends an initial response to the url to get session info

    Keyword args:
        none

    Return:
        a dictionary; contains session info required to make aspx request
    """

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


def get_dept(subject, quarter, year, session_info):
    """
    this function makes aspx requests and returns the html response

    Keyword args:
    subject -- a string; one of "PSTAT", "MATH", or "CMPSC" (not case-sensitive)
    quarter -- a string; one of "SPRING", "SUMMER", "FALL", or "WINTER" (not case-sensitive)
    year -- an int; year of interest
    session_info -- a dict; contains session info required to make aspx request

    return:
    a dictionary; contains all courses as list of dicts along with metadata (structure below)
    {
    'quarter':'FALL',
    'year':2016,
    'courses':
        [
            {
            'course_code':
            'course_title':
            'time':
            'location':
            'professor':
            'course_size':
            'days':
            },
            {
            'course_code':
            'course_title':
            'time':
            'location':
            'professor':
            'course_size':
            'days':
            },
            ...
        ]
    }
    """
    # aspx form takes year and quarter in the form of a 5 digit integer
    #   the first 4 digits represent the year and the last digit represents the quarter
    #   1: winter, 2: spring, 3: summer, 4: fall
    # here, we convert accordingly
    full_number = int(str(year) + str(QUARTERS[quarter]))

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

    soup = bs.BeautifulSoup(req2.text, 'html.parser')
    row_html_list = soup.select('tr[class="CourseInfoRow"]')
    courses = []
    for row_html in row_html_list:
        row = list(row_html.stripped_strings)
        if row[-1]:
            n_days = len(row[-5])
            if (n_days < 6) & (n_days > 1): # filtering out edge cases (canceled/special courses) as well as sections
                course = {}
                course['Code'] = row[0]
                course['Title'] = row[3]
                course['Time'] = row[-4]
                course['Location'] = row[-3]
                course['Professor'] = row[-6]
                course['Size'] = row[-2]
                course['Days'] = row[-5]
                courses.append(course)

    rdict = {
    'subject':subject,
    'quarter':quarter,
    'year':year,
    'courses':courses
    }

    return rdict


def create_sheet(name):
    scope = [
        'https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/drive'
    ]
    creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
    client = gspread.authorize(creds)
    sheet = client.create(name)
    return sheet


def output_to_csv(dept, output_dir):
    subject = dept['subject']
    courses = dept['courses']
    filename = subject + '-' + dept['quarter'] + str(dept['year']) + '.csv'
    filepath = os.path.join(output_dir, filename)
    f = open(filepath, 'w')
    w = csv.DictWriter(f, courses[0].keys())
    w.writeheader()
    w.writerows(courses)
    f.close()
    print(subject , 'courses for', dept['quarter'], str(dept['year']), 'outputted to', filepath)


def output_to_worksheet(dept, sheet):
    courses = dept['courses']
    colnames = list(courses[1].keys())
    colnames.append('Officer')
    nrows = len(courses) + 1
    ncols = len(colnames)
    worksheet = sheet.add_worksheet(title=dept['subject'], rows=nrows, cols=ncols)
    print("Creating worksheet for", dept['subject'])
    # output headers
    for i in trange(nrows, unit = 'row'):
        if i == 0:
            for j in range(ncols):
                worksheet.update_cell(i+1, j+1, colnames[j])
        else:
            for j in range(ncols-1):
                worksheet.update_cell(i+1, j+1, courses[i-1][colnames[j]])


def courses_to_csv(quarter, year, session_info, output_dir):
    """
    writes course info to CSVs and outputs paths to files

    Keyword arguments:
    quarter -- a string; one of "SPRING", "SUMMER", "FALL", or "WINTER" (not case-sensitive)
    year -- an int; year of interest
    session_info -- a dict; contains session info required to make aspx request
    output_dir -- a string; path to output directory

    Return:
    None; outputs path to files
    """
    for subject in SUBJECTS:
        dept = get_dept(subject, quarter, year, session_info)
        output_to_csv(dept, output_dir)


def courses_to_gsheet(quarter, year, session_info):
    """
    writes course info to a google sheet and returns the link to the sheet

    Keyword arguments:
    quarter -- a string; one of "SPRING", "SUMMER", "FALL", or "WINTER" (not case-sensitive)
    year -- an int; year of interest
    session_info -- a dict; contains session info required to make aspx request

    Return:
    a string; link to sheet
    """
    sheet_name = quarter + ' ' + str(year) + ' Class Announcements'
    print("Creating Google Sheet for", quarter, str(year))
    sheet = create_sheet(sheet_name)
    for subject in SUBJECTS:
        dept = get_dept(subject, quarter, year, session_info)
        output_to_worksheet(dept, sheet)
    sheet.share('datascience.ucsb@gmail.com', perm_type='user', role='writer')
    link = 'https://docs.google.com/spreadsheets/d/' + sheet.id
    return link

# for each dept
    # create worksheet
    # write dept course contents to worksheet
        # update headers
        # for each row
            # update each column
# sheet.share('datascience.ucsb@gmail.com', perm_type='user', role='writer')
# return link to sheet


# ======================
# MAIN
# ======================
if __name__ == '__main__':
    print('UCSB Data Science Course Info Scraper\nDeveloped by NATHAN FRITTER and TIMOTHY NGUYEN\n' + '='*50)

    parser = argparse.ArgumentParser(description='Scrape UCSB\'s course listings and outputs to Google Sheets (default) or CSV')
    parser.add_argument('quarter')
    parser.add_argument('year')
    parser.add_argument('-c', '--csv', default=False, action='store_true',
                        help = 'output to csv instead of to Google Sheets')
    parser.add_argument('-o', '--output_directory', default='.',
                        help = 'manually designate output file')

    args = parser.parse_args()
    quarter = args.quarter.upper()
    year = args.year
    out_dir = args.output_directory

    sesh = get_session_info()
    if args.csv:
        courses_to_csv(quarter, year, sesh, out_dir)
    else:
        link = courses_to_gsheet(quarter, year, sesh)
        print('Courses for', quarter, str(year), 'outputted to', link)
