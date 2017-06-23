# Created by Nathan Fritter, Timothy Nguyen, and Brittany Cain


## -- HEADER --
import bs4 as bs
import urllib.request
import os

## -- FUNCTIONS --

def

# precondition: the argument is a list of stripped strings (which is returned by get_rows())
# postcondition: the function returns a list of dicts, each dict containing all the elements of interest for each
#   course in the list
def extract_elements(row_list):
    courses = []
    for row in row_list:
        course = {}
        course['course_code'] = row[0]
        course['course_title'] = row[3]
        course['time'] = row[-4]
        course['location'] = row[-3]
        course['professor'] = row[-6]
        course['course_size'] = row[-2]
        course['days'] = row[-5]
        # FIX DAYS ######
        # if row[-5] == 'INSTRUCTOR APPROVAL REQUIRED PRIOR TO REGISTRATION.':
        #
        # else:
        #     course['days'] = row[-5]
        courses.append(course)
    return(courses)

# precondition: the first argument is the html file to be parsed
#   the second argument is a string representation of a dept to be passed into extract_elements
# postcondition: the function returns a list of dicts each representing a course contained within the department
def get_rows(path):
    page = open(path)
    soup = bs.BeautifulSoup(page, 'html.parser')
    row_html_list = soup.select('tr[class="CourseInfoRow"]')
    row_list = []
    for row_html in row_html_list:
        row = list(row_html.stripped_strings)
        if row[-1]:
            row_list.append(row)
    return(row_list)


    # for row in rows_html:
    #     print(list(row.stripped_strings))
    #     rows_list.append(list(row.stripped_strings))
    # return(rows_list)
    # course = {}
    # for i in range(6):
    #     [i]
    #     elements = list(row.stripped_strings)
    #     course['course_code'] = elements[0]
    #     course['course_title'] = elements[3]
    #     course['days'] = elements[25]
    #     course['time'] = elements[26]
    #     course['location'] = elements[27]
    #     course['professor'] = elements[24]
    #     course['course_size'] = elements[28]
    #     print(course)

stats_path = os.getcwd() + '/PSTAT.html'
cs_path = os.getcwd() + '/CMPSC.html'
math_path = os.getcwd() + '/MATH.html'

