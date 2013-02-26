## construction du corpus

Pour construire le corpus, nous allons utiliser les techniques de base du scrapping web en effectuant de simples requêtes HTTP de parcours d'un catalogue paginé.

Le langage préféré ici est python pour des raisons d'homogénité avec les autres travaux de la plateforme [cortext](http://cortext.net).

### trouver un point de départ

Calenda met à disposition un catalogue paginé d'événements et grâce à leur attention aux standards du web, la tâche ne sera pas très compliqué. Il faut d'abord savoir quelles pages scrapper. Leur catalogue étant bien construit, un rapide tour sur le site permet de déterminer une page de départ :

```
http://calenda.org/search?primary=fsubject&fsubject=298
```

la partie qui nous intéresse ici est le `fsubject=298` et particulièrement le "298". Rien de bien foufou jusque là mais ca pourra toujours être pratique pour une analyse de plus grande échelle.

### parcourir les pages

```python
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
```

### stocker et analyser les pages

```
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
    yaml.safe_dump(metadata, f, default_flow_style=False, encoding=('utf-8'), allow_unicode=True)
    f.write('---\n')

    f.write( page('#resume > div').html().strip() )

    f.write('\n---\n')

    f.write( "\n".join([ l.strip() for l in page('#annonce > div').html().split('\n') ]) )
```

### faire tourner la machine

```
python scrap_calenda.py 298
```