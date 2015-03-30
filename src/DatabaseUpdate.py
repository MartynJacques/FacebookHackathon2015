import MySQLdb
import json

import DatabaseSettings

import time

db = MySQLdb.connect(host=DatabaseSettings.dbhostname, user="hack", passwd="fb2015", db="fbhack2015")

cursor = db.cursor()

import controller
from models import UrlInfo

current_milli_time = lambda: int(round(time.time() * 1000))
run_time = current_milli_time()
five_mins = (1000 * 60 * 5)

while True:
    cursor.execute("SELECT * FROM sites")

    numrows = int(cursor.rowcount)

    print "Found %d sites" % numrows

    for i in range(0,numrows):
        url = cursor.fetchone()[0]

        print "Updating %s..." % url

        testResponse = UrlInfo()
        testResponse.url = url
        url = url.replace("http://","")
        url = url.replace("www.", "")
        facebookInteractions = {'likes':10, 'shares':4}
        testResponse.interactions['facebook'] = controller.get_facebook(url)
        testResponse.interactions['twitter'] = controller.get_twitter(url)
        testResponse.interactions['google'] = controller.get_google(url)

        statement = "INSERT INTO InteractionCounts (website, json) VALUES (%s, %s)"

        json_output = json.dumps(testResponse.interactions)

        insert_cursor = db.cursor()

        # execute SQL select statement
        insert_cursor.execute(statement, (url, json_output))

        db.commit()

    sleep_time = five_mins - (current_milli_time() - run_time)
    time.sleep(sleep_time / 1000.0)
    run_time = current_milli_time();