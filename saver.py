# -*- coding: utf-8 -*-

# entity name -- patent title -- filing date --       issue date --    author name --  patent number -- application number
# PATENT         title           filing/creation date publication date inventor/author
# id -- title -- assignee -- inventor/author -- priority date -- filing/creation date -- publication date -- 


"""
1. Take data from Google Patents, give arguments: query and dates
2. Edit CSV
3. Save CSV
"""

import urllib
import json
import datetime
import threading
import os
import shutil
import csv
# from pprint import pprint


def year_validator(date):
    try:
        date = int(date)
        if date in range(1900, 2030):
            return True
    except:
        pass

QUERY = ""
while QUERY == "":
    QUERY = raw_input("Please specify query: ")

YEAR_FROM = None
while not year_validator(YEAR_FROM):
    YEAR_FROM = raw_input("Year from: ")

YEAR_TO = None
while not year_validator(YEAR_TO):
    YEAR_TO = raw_input("Year to: ")

query_url = None
query_filename = None
if " " in QUERY:
    query_url = QUERY.replace(" ", "%2B")
    query_filename = QUERY.replace(" ", "_")

print query_url, query_filename, YEAR_TO, YEAR_FROM

years = abs(int(YEAR_TO) - int(YEAR_FROM))
days = 365 * (years + 1)
base_date = None
if YEAR_FROM >= YEAR_TO:
    base_date = YEAR_FROM
else:
    base_date = YEAR_TO

base_date = base_date + "1231"
base_date = datetime.datetime.strptime(base_date, '%Y%m%d')
date_list = [datetime.datetime.strftime(base_date - datetime.timedelta(days=x), '%Y%m%d') for x in range(0, days)]
date_list1 = date_list[1:]
date_list2 = date_list[:-1]

if not os.path.exists("tmp"):
    os.makedirs("tmp")

def retriever(i, j):

    url = "https://patents.google.com/xhr/query?url=q%3D{0}%26before%3Dfiling%3A{1}%26after%3D{2}&download=true" \
    .format(query_url, j, i)
    filename = "tmp/{0}_from_{1}_to_{2}.csv".format(query_filename, i, j)

    print filename

    testfile = urllib.URLopener()
    testfile.retrieve(url, filename)

threads = []
for i, j in zip(date_list1, date_list2):
    t = threading.Thread(target=retriever, args=(i, j,))
    threads.append(t)
for x in threads:
    x.start()
for x in threads:
    x.join()

for csv in os.listdir("tmp"):


if os.path.exists("tmp"):
    shutil.rmtree("tmp")