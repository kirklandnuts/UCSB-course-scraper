#!python3
# Created by Nathan Fritter, Timothy Nguyen, and Brittany Cain


## -- DEPENDENCIES --
import bs4 as bs
import os
from datetime import datetime
import argparse
import csv


## -- FUNCTIONS --
# precondition: the first argument is the list of dicts returned from extract_elements()
#   the second argument is the desired filename of the output file
# postcondition: this function will output the inputted list of rows to a CSV file named as was described
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


# https://stackoverflow.com/questions/17330139/python-printing-a-dictionary-as-a-horizontal-table-with-headers
def print_table(my_dict, col_list=None):
   """ Pretty print a list of dictionaries (myDict) as a dynamically sized table.
   If column names (colList) aren't specified, they will show in random order.
   Author: Thierry Husson - Use it as you want but don't blame me.
   """
   if not col_list: col_list = list(my_dict[0].keys() if my_dict else [])
   my_list = [col_list] # 1st row = header
   for item in my_dict: my_list.append([str(item[col] or '') for col in col_list])
   col_size = [max(map(len,col)) for col in zip(*my_list)]
   format_str = ' | '.join(["{{:<{}}}".format(i) for i in col_size])
   my_list.insert(1, ['-' * i for i in col_size]) # Seperating line
   for item in my_list: print(format_str.format(*item))




    #
    # output_dir = args.output_directory
    # current_time = datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
    # output_name = dept_string + current_time + '.csv'
    #
    # stats_elements = extract_elements(get_rows(stats_path))
    # cs_elements = extract_elements(get_rows(cs_elements))
    # math_elements = extract_elements(get_rows(math_elements))
    #
    # output_to_csv(stats_elements, output_name)
    # output_to_csv(cs_elements, output_name)
    # output_to_csv(math_elements, output_name)



# -- TESTING --
data_dir = os.path.join(os.getcwd(), 'data')
stats_path = os.path.join(data_dir, 'pstat-fall-2017.html')
cs_path = os.getcwd() + '/CMPSC.html'
math_path = os.getcwd() + '/MATH.html'

# TODO:
#   1) output to google sheets via google sheets API or some module
#   2) write main functionality
