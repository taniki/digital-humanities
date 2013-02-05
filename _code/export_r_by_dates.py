# -*- coding: utf-8 -*-

import glob
import codecs
import yaml
import time
import json
source_dir = 'dh_calenda_events/'

def parse_date(date):
  date = date.split(' ', 1)[1]

  date = date.replace(u'janvier', '01')
  date = date.replace(u'février', '02')
  date = date.replace(u'mars', '03')
  date = date.replace(u'avril', '04')
  date = date.replace(u'mai', '05')
  date = date.replace(u'juin', '06')
  date = date.replace(u'juillet', '07')
  date = date.replace(u'août', '08')
  date = date.replace(u'septembre', '09')
  date = date.replace(u'octobre', '10')
  date = date.replace(u'novembre', '11')
  date = date.replace(u'décembre', '12')

  date_decoded = time.strptime(date,"%d %m %Y")

  return date_decoded

def parse_event(f):
  event_file = codecs.open(f, "r", "utf-8")

  [ x, metadata, abstract, content ] = event_file.read().split('---', 3)

  metadata = yaml.load(metadata)

  data = []
  
  for date in metadata['dates']:
    l = {}

    l['date'] = time.strftime("%Y-%m-%d",parse_date(date))
    l['keywords'] = ','.join(metadata['keywords'])
    l['title'] = metadata['title']
    l['event_id'] = metadata['permalink']

    data.append(l)

  return data


def open_events():
  events_by_date = []

  for f in glob.glob(source_dir+'*.md'):
    events_by_date.extend( parse_event(f) )

  output = codecs.open('dates_events.json', "w", "utf-8")

  output.write(json.dumps(events_by_date))

 # print events_by_date

open_events()