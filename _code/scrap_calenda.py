
import codecs

import urllib2
from pyquery import PyQuery as pq


url = "http://calenda.org/search?primary=fsubject&fsubject=298"

target_dir = 'dh_calenda_events'

def parse_results(results):
  for result in results:
    entry = pq(result);

    a = entry('.title a').attr('href');
    title = entry('.title a').html()

    # print a
#    print title

    f = codecs.open("dh_calenda_events/%s.md" % a, "w", "utf-8")

    f.write(u'title: "%s"' % title)

def parse(url):
  "prelimenary parsing"

  print url

  content = pq(url = url)

  count = 0

  results = content('#results .list_entry')

  while len(results) > 0:
    parse_results(results)

    temp = int(count) + 20

    count += len(results)

    # print temp

    content = pq(url = url+'&start=%i' % temp)
    results = content('#results .list_entry')

  print count


parse(url)