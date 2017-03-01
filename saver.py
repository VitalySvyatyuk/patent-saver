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
import time
import fileinput
import sys


if os.path.exists("tmp"):
    shutil.rmtree("tmp")
if os.path.isfile("errors.txt"):
    os.remove("errors.txt")
if os.path.isfile("errors2.txt"):
    os.remove("errors2.txt")

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

print "Searching '" + QUERY + "' from " + YEAR_FROM + " to " + YEAR_TO

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

    try:
        testfile = urllib.URLopener()
        testfile.retrieve(url, filename)
    except:
        time.sleep(1)
        testfile = urllib.URLopener()
        testfile.retrieve(url, filename)
        with open('errors.txt', 'a') as errors:
            errors.write(url + " " + filename + "\n")

def add_retriever(url, filename):
    try:
        newfile = urllib.URLopener()
        newfile.retrieve(url, filename)
        print "Success"
    except:
        print "Fail"
        with open("errors2.txt", "a") as err2:
            err2.write(url + " " + filename + "\n")

fl = "{0}_from_{1}_to_{2}.csv".format(query_filename, YEAR_FROM, YEAR_TO)
open(fl, 'a').close()

threads = []
for i, j in zip(date_list1, date_list2):
    t = threading.Thread(target=retriever, args=(i, j,))
    threads.append(t)

thread_of_threads = []
started = []

print "Downloading..."

for x in threads:
    # time.sleep(0.04)
    x.start()
    started.append(x)
    if threads.index(x) % 100 == 0:
        for x in started:
            # time.sleep(0.01)
            x.join()
        started = []

for x in started:
    x.join()

if os.path.isfile("errors.txt"):
    print "Second attempt..."
    with open("errors.txt", 'r+') as err:
        thre = []
        for er in err:
            url, filename = er.split(" ")
            filename = filename.replace("\n", "")
            t = threading.Thread(target=add_retriever, args=(url, filename,))
            thre.append(t)
        for l in thre:
            time.sleep(0.1)     
            l.start()
        for l in thre:
            l.join()

with open(fl, 'w') as write_to:
    writer = csv.writer(write_to, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
    writer.writerow(['id', 
                     'title', 
                     'assignee', 
                     'inventor/author', 
                     'priority date', 
                     'filing/creation date', 
                     'publication date', 
                     'grant date', 
                     'result link'])
    for csv_file in os.listdir("tmp"):
        with open('tmp/' + csv_file, 'rb') as f:
            reader = csv.reader(f)
            for row in reader:
                if row[0] != "id":
                    if row[0] != "search URL:":
                        writer.writerow(row)

print "Success! File -> " + str(fl)

if os.path.isfile("errors.txt"):
    os.remove("errors.txt")
if os.path.isfile("errors2.txt"):
    os.remove("errors2.txt")
if os.path.exists("tmp"):
    shutil.rmtree("tmp")