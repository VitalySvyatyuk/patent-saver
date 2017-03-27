import requests
import urllib
import time
import json

# http://stackoverflow.com/questions/15028166/python-module-for-searching-patent-databases-ie-uspto-or-epo

access_token = "AIzaSyD7U1HcI5m9IqTpXKrRIELTLPV_NzJ1lno"
cse_id = "000145977411789292541:ifva_vwmntm"

# Build url
start=0
search_text = "+(inassignee:\"Altera\" | \"Owner name: Altera\") site:www.google.com/patents/"
# &tbm=pts sets you on the patent search
url = 'https://www.googleapis.com/customsearch/v1?key='+access_token+'&cx='+cse_id+'&start='+str(start)+'&num=1000&tbm=pts&q='+ urllib.quote(search_text)
print url
response = requests.get(url)

response.json()
f = open('Sample_patent_data'+str(int(time.time()))+'.txt', 'w')
f.write(json.dumps(response.json(), indent=4))
f.close()






# import csv
# import urllib, urllib2
# from urllib import FancyURLopener

# # url = "http://127.0.0.1:8008/"
# url = "http://patents.google.com/xhr/query?url=q%3Dartificial%2Bintelligence%26before%3Dfiling%3A20041221%26after%3D20041220&download=true"
# headers = {'User-agent' : 'Mozilla/5.0 (Windows; U; Windows NT 5.1; de; rv:1.9.1.5) Gecko/20091102 Firefox/3.5.5'}
# # urllib.request.urlretrieve(url, "file.csv")


# # req = urllib2.Request(url, None, headers=headers)
# # html = urllib2.urlopen(req).read()

# class MyOpener(FancyURLopener):
#     version = headers['User-agent']

# myopener = MyOpener()
# myopener.addheaders = [('User-Agent', headers['User-agent']), ('Accept', '*/*')]
# page = myopener.open(url)

# # response = urllib.urlopen(url)
# cr = csv.reader(page)
# for row in cr:
#   print row

# # csvstr = str(csv).strip("b'")

# # lines = csvstr.split("\\n")
# # f = open("historical.csv", "w")
# # for line in lines:
# #    f.write(line + "\n")
# # f.close()