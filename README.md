# Class Listings Scraper
Web scraper for aggregating information on a list of designated UCSB classes.

## Usage
arguments:
```
python UCSB-course-scraper.py -h
UCSB Data Science Course Info Scraper
Developed by NATHAN FRITTER and TIMOTHY NGUYEN
==================================================
usage: UCSB-course-scraper.py [-h] [-c] [-o OUTPUT_DIRECTORY] quarter year

Scrape UCSB's course listings and outputs to Google Sheets (default) or CSV

positional arguments:
  quarter
  year

optional arguments:
  -h, --help            show this help message and exit
  -c, --csv             output to csv instead of to Google Sheets
  -o OUTPUT_DIRECTORY, --output_directory OUTPUT_DIRECTORY
                        manually designate output file
```

Here's how to get course info for PSTAT, MATH, and CMPCS courses for FALL 2017 and output to a google sheet:
```
$ python UCSB-course-scraper.py fall 2017
UCSB Data Science Course Info Scraper
Developed by NATHAN FRITTER and TIMOTHY NGUYEN
==================================================
Creating Google Sheet for FALL 2017
Creating worksheet for PSTAT
100%|██████████████████████████████████████████████████| 24/24 [01:04<00:00,  2.58s/row]
Creating worksheet for MATH
100%|██████████████████████████████████████████████████| 56/56 [02:35<00:00,  3.14s/row]
Creating worksheet for CMPSC
100%|██████████████████████████████████████████████████| 20/20 [00:56<00:00,  2.73s/row]
Courses for FALL 2017 outputted to https://docs.google.com/spreadsheets/d/1WlijEnWp6KCYznXJn1goYPmVMUEUBiG878_Q7BvxaSo
```
PLEASE NOTE: The Google Drive functionality will not work without the client secret (contact Timothy for it)


The data can also be outputted to CSVs in a designated output directory using the optional arguments `-c` and `-o`:
```
$ python UCSB-course-scraper.py fall 2017 -c -o ~/Documents/data-sci/class-announcements
UCSB Data Science Course Info Scraper
Developed by NATHAN FRITTER and TIMOTHY NGUYEN
==================================================
PSTAT courses for FALL 2017 outputted to /Users/timmy/Documents/data-sci/class-announcements/PSTAT-FALL2017.csv
MATH courses for FALL 2017 outputted to /Users/timmy/Documents/data-sci/class-announcements/MATH-FALL2017.csv
CMPSC courses for FALL 2017 outputted to /Users/timmy/Documents/data-sci/class-announcements/CMPSC-FALL2017.csv
```

If no output directory is specified, the program will use the current working directory by default:
```

$ python UCSB-course-scraper.py fall 2017 -c
UCSB Data Science Course Info Scraper
Developed by NATHAN FRITTER and TIMOTHY NGUYEN
==================================================
PSTAT courses for FALL 2017 outputted to ./PSTAT-FALL2017.csv
MATH courses for FALL 2017 outputted to ./MATH-FALL2017.csv
CMPSC courses for FALL 2017 outputted to ./CMPSC-FALL2017.csv
```


# To-do

- implement google sheets api v4 (currently going through gspread which leverages gsheet api v3)
- generalize to all departments
