import MySQLdb
import DatabaseSettings
import requests
import json
import xml.dom.minidom
from bs4 import BeautifulSoup
from xml.dom import minidom
import re
import datetime
import string

db = MySQLdb.connect(host=DatabaseSettings.dbhostname, user="hack", passwd="fb2015", db="fbhack2015")

facebook_url = "http://api.facebook.com/restserver.php?method=links.getStats&urls="
twitter_url = "http://cdn.api.twitter.com/1/urls/count.json?url="
google_url = "https://plusone.google.com/_/+1/fastbutton?url=http://"
user_agent = "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"

non_decimal = re.compile(r'[^\d.]+')

def get_facebook(url):
  data =  get_url(facebook_url + url)
  if data:
    xmldoc = minidom.parseString(data)
    results = {}
    results['likes'] =              int(extract_count(xmldoc, 'like_count'))
    results['comments'] =           int(extract_count(xmldoc, 'comment_count'))
    results['total_interactions'] = int(extract_count(xmldoc, 'total_count'))
    results['clicks'] =             int(extract_count(xmldoc, 'click_count'))
    results['shares'] =             int(extract_count(xmldoc, 'share_count'))
    return results
  else:
    return None

def extract_count(doc, tag):
  return doc.getElementsByTagName(tag)[0].childNodes[0].data

def get_twitter(url):
  data = get_url(twitter_url + url)
  if data:
    dict_obj = json.loads(data)
    del dict_obj['url']
    return dict_obj
  else:
    return None

def get_google(url):
  data = get_url(google_url + url)
  if data:
    soup = BeautifulSoup(data)
    count = soup.find(id='aggregateCount').string
    count = filter(lambda x: x in string.printable, count)
    count = count.replace(">", "")
    if count[-1] == "k":
      count = str(1000 * int(float(count[:-1])))
    elif count[-1] == "M":
      count = str(1000000 * int(float(count[:-1])))
    return {'plus_ones' : int(count)}
  else:
    return None

def get_url(url):
  headers = {
      'User-Agent': user_agent
  }
  response = requests.get(url, headers=headers)
  if response.status_code == 200:
    return response.text
  else:
    return None

def add_if_not_present(url):
  cursor = db.cursor()
  cursor.execute('SELECT * FROM sites WHERE name=\"' + url + '\"')
  numrows = int(cursor.rowcount)
  if numrows == 0:
    cursor.execute("INSERT INTO sites (name) VALUES (\'" + url + "\')")
  db.commit()

def get_history(url):
  cursor = db.cursor()
  cursor.execute('SELECT * FROM InteractionCounts WHERE website=\"' + url + '\"')
  numrows = int(cursor.rowcount)
  results = []
  for i in range(0,numrows):
    item = cursor.fetchone()
    timestamp = long(unix_time_millis(item[1]))
    json_data = json.loads(item[2])
    results.append( {'timestamp' : timestamp, 'interactions' : json_data})
  db.commit()
  return {'data' : results}

def get_history_num(url):
  cursor = db.cursor()
  cursor.execute('SELECT * FROM InteractionCounts WHERE website=\"' + url + '\"')
  numrows = int(cursor.rowcount)
  db.commit()
  return numrows

def unix_time(dt):
    epoch = datetime.datetime.utcfromtimestamp(0)
    delta = dt - epoch
    return delta.total_seconds()

def unix_time_millis(dt):
    return unix_time(dt) * 1000.0