import sys

import codecs

import urllib2
import yaml

from pyquery import PyQuery as pq
# import BeautifulSoup

try:
  category = int( sys.argv[1] )
except IndexError:
  print "first argument is necessary and shoud correspond to a category id (ex: 298)"
  exit(0)

url = "http://calenda.org/search?primary=fsubject&fsubject=%i" % category

target_dir = 'dh_calenda_events'

def parse_results(results):
  for result in results:
    entry = pq(result);

    a = entry('.title a').attr('href');
    title = entry('.title a').html()

    # print a
    print "%s: %s" % (a, title)

    f = codecs.open("dh_calenda_events/%s.md" % a, "w", "utf-8")

    metadata = {}
    metadata['title'] = "%s" % title
    metadata['permalink'] = "http://calenda.org/%s" % a

    page = pq(url = metadata['permalink'])

    kw = page('#motscles ul li').html()

    metadata['keywords'] = kw.split(', ') if kw else []
    metadata['dates'] = [ pq(d).html() for d in page('#dates ul li') ]

    f.write('---\n')
    f.write(yaml.safe_dump(metadata, default_flow_style=False))
    f.write('---\n')

    f.write( page('#resume > div').html().strip() )

    f.write('\n---\n')

    f.write( "\n".join([ l.strip() for l in page('#annonce > div').html().split('\n') ]) )


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