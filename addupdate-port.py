#!/usr/bin/python

# 2018-02-22 - BH

# Adds 'comportonly' filter to serial-adapter serial port settings,
# to quickly add new ports for testing.

# NOTE: Extremely hacky -- will burn through floors if not handled with care

import sqlite3
import json
import sys

if len(sys.argv) < 2:
  print "Please provide serial port"
  exit(1)

# open database
conn = sqlite3.connect('/home/pi/mozilla-iot/gateway/db.sqlite3')

# get the current data
c = conn.cursor()

c.execute('select value from settings where key="addons.serial-adapter"')
serrow = c.fetchone()

# modify the data
j = json.loads(serrow[0])
if 'comportonly' not in j[u'moziot'][u'config'][u'ports']:
  # add it
  j[u'moziot'][u'config'][u'ports'][u'comportonly'] = { u'comName': sys.argv[1] }
else:
  # modify
  j[u'moziot'][u'config'][u'ports'][u'comportonly'][u'comName'] = sys.argv[1]

c.execute('update settings set value = ? where key = "addons.serial-adapter"', [json.dumps(j)])
conn.commit()
conn.close()

print "Updated serial-adapter config 'comportonly' filter with '{}'".format(sys.argv[1])

