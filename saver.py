# -*- coding: utf-8 -*-

# entity name -- patent title -- filing date --       issue date --    author name --  patent number -- application number
# PATENT         title           filing/creation date publication date inventor/author
# id -- title -- assignee -- inventor/author -- priority date -- filing/creation date -- publication date -- 

import urllib
import json
import datetime
import threading
import os
import shutil
import csv
import time
import fileinput
import sys
from operator import itemgetter
from country_codes import CCODES
from queries import QUERIES


if os.path.exists("tmp"):
    shutil.rmtree("tmp")

def year_validator(date):
    try:
        date = int(date)
        if date in range(1900, 2030):
            return True
    except:
        pass

# SEARCH_IN = ""
# while SEARCH_IN.lower() != "g" and SEARCH_IN.lower() != "p":
#     SEARCH_IN = raw_input("Where to look at? Google (g), " + \
#                           "or patentsview.org (p): ")
# QUERY = ""
# while QUERY == "":
#     QUERY = raw_input("Please specify query: ")

YEAR_FROM = None
while not year_validator(YEAR_FROM):
    YEAR_FROM = raw_input("Year from: ")

YEAR_TO = None
while not year_validator(YEAR_TO):
    YEAR_TO = raw_input("Year to: ")

def CSVs(fl, assignees, assignees_grant, assignees_row, assignees_grant_row):
    rows = []
    for assign in assignees_row:
        row = []
        row.append(assign[0])
        row.append(assignees[assign[0]])
        row.append(assign[1])
        row.append(assign[2])
        rows.append(row)
    rows_sorted_by_count = sorted(rows, key=itemgetter(1), reverse=True)

    for key, value in assignees_grant.items():
        temp_list = []
        temp_list.append(key[0])
        temp_list.append(key[1])
        temp_list.append(key[2])
        temp_list.append(value)
        temp_list.append(key[3])
        temp_list.append(key[4])
        if key[1] != "":
            assignees_grant_row.append(temp_list)
    rows_gr_srt_by_assig = sorted(assignees_grant_row, key=itemgetter(0, 1))
    fl_srt_assign = "patents-by-assignee.csv"
    with open(fl_srt_assign, 'w') as write_to:
        writer = csv.writer(write_to, delimiter=',',
                                      quotechar='"', 
                                      quoting=csv.QUOTE_ALL)
        writer.writerow(['assignee', 
                         'count', 
                         'country', 
                         'country code'])
        for row in rows_sorted_by_count:
            writer.writerow(row)
    print "Success! File -> " + str(fl_srt_assign)

    fl_srt_assign_grnt = "patents-by-assignee-year.csv"
    with open(fl_srt_assign_grnt, 'w') as write_to:
        writer = csv.writer(write_to, delimiter=',',
                                      quotechar='"', 
                                      quoting=csv.QUOTE_ALL)
        writer.writerow(['assignee',
                         'grant year'
                         'filing year', 
                         'count', 
                         'country', 
                         'country code'])
        for row in rows_gr_srt_by_assig:
            writer.writerow(row)
    print "Success! File -> " + str(fl_srt_assign_grnt)

# www.patentsview.org
q = ""
for QUERY in QUERIES: #code here
    # q += '{"_text_phrase":{"patent_title":"%s"}},' % QUERY
    q += '{"_text_phrase":{"patent_abstract":"%s"}},' % QUERY
query = 'http://www.patentsview.org/api/patents/query?q={"_and":[' \
        '{"_or":[%s]},' \
        '{"_gte":{"app_date":"%s-01-01"}},' \
        '{"_lte":{"app_date":"%s-01-01"}}]}' \
        '&o={"page":1,"per_page":10000}' \
        '&f=["patent_number",' \
            '"patent_title",' \
            '"patent_date",' \
            '"patent_year",' \
            '"assignee_type",' \
            '"assignee_country",' \
            '"assignee_first_name",' \
            '"assignee_last_name",' \
            '"assignee_organization",' \
            '"app_date",' \
            '"inventor_first_name",' \
            '"inventor_last_name"]' \
            % (q[:-1], YEAR_FROM, YEAR_TO)

url = query.replace(" ", "%20")
response = urllib.urlopen(url)
dat = json.load(response)
data = dat['patents']

fl = "patents.csv"
with open(fl, 'w') as write_to:
    writer = csv.writer(write_to, delimiter=',',
                                  quotechar='"', 
                                  quoting=csv.QUOTE_ALL)
    writer.writerow(['id',  
                     'title',
                     'assignee',
                     'inventor/author',
                     'priority date', 
                     'filing/creation date',
                     'publication date',  
                     'grant date',
                     'result link', 
                     'country',
                     'country code',
                     'grant year',
                     'filing year',])
    for patent in data:
        row = []
        row.append(patent['patent_number'])
        row.append(patent['patent_title'])
        if patent['assignees'][0]['assignee_type'] in ['2', '3', '6',
                                                       '7', '8', '9']:
            row.append(patent['assignees'][0]['assignee_organization'])
        elif patent['assignees'][0]['assignee_type'] in ['4', '5']:
            row.append(patent['assignees'][0]['assignee_first_name'] + " " + \
                       patent['assignees'][0]['assignee_last_name'])
        else:
            row.append("")
        authors = ""
        for inventor in patent['inventors']:
            authors += inventor['inventor_first_name'] + \
                       inventor['inventor_last_name'] + ", "
        inventors = authors[:-2]
        row.append(inventors)
        row.append("") # priority date
        row.append(patent['applications'][0]['app_date']) # filing/creation date
        row.append("") # publication date
        row.append(patent['patent_date']) # grant date
        row.append("") # result link
        try:
            row.append(CCODES[patent['assignees'][0]['assignee_country']])
            row.append(patent['assignees'][0]['assignee_country'])
        except:
            row.append("")
            row.append("")
        row.append(patent['patent_year'])
        row.append(patent['applications'][0]['app_date'][:4]) # filing year
        row_utf = [x.encode('utf-8') for x in row]
        writer.writerow(row_utf)
print "Success! File -> " + str(fl)

assignees = {}
assignees_grant = {}
assignees_row = []
assignees_grant_row = []
with open(fl, 'r') as read_from:
    datareader = csv.reader(read_from, delimiter=',', quotechar='"')
    iterdatareader = iter(datareader)
    next(iterdatareader)
    for line in iterdatareader:
        if line[2] in assignees:
            assignees[line[2]] += 1
        else:
            assignees[line[2]] = 1
            assignees_row.append((line[2], line[9], line[10]))
        if (line[2], line[11], line[12], line[9], line[10]) in assignees_grant:
            assignees_grant[(line[2], line[11], line[12], line[9], line[10])] += 1
        else:
            assignees_grant[(line[2], line[11], line[12], line[9], line[10])] = 1
CSVs(fl, assignees, assignees_grant, assignees_row, assignees_grant_row)
