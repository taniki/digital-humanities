---
title: Une analyse des évenements en SHS en Python et R
date: 2013-02-27

tags:
  - outils

layout: default
---




Ce codebook a pour objectif de prédéfinir une étude sur la position des *digital humanities* dans le paysage des plateformes d'équipement méthodologiques. La question du rapport entre "humanities" américaines et "sciences humaines et sociales" (francaises et européennes) est mise temporairement de côté.

Les outils que nous proposons ici sont :

- une collection de textes d'annonces et d'appel à participation à des évenements ayant lieu majoritairement dans la sphère francophone. Tout le corpus sera basé sur un scrapping de [calenda](http://calenda.org). Il s'agit d'un site de référence concernant la diffusion d'événement dans le champ académique francais. Nous laissons pour plus tard l'hypothèse que les informations fournies sont insuffisantes pour mener une étude quantitative pertinente
- une étude lexicométrique descriptive sur les mots clés fournis par les auteurs d'événements ainsi qu'une fouille de données sur les textes intégrales de présentation afin de comparé les différences lexicales et la créativité descriptive

## scrapping et corpus

La partie concernant le scrapping et le stockage architecturé des informations est documenté dans un autre document.

Le dataset de base de cette analyse sera donc un fichier json du type `dates_events.json` ayant la tête suivante :

```json
[
  ...,
  {
    "date": "2009-09-09",
    "keywords": "livre,ebook,lecture,écriture",
    "event_id": "http://calenda.org/198746",
    "title": "L’avenir du livre en questions"
  }
  ,...
]
```

## pré-analyse

### faire rentrer les données dans R


{% highlight r %}
library("rjson")
library("plyr")
library("zoo")
{% endhighlight %}



{% highlight text %}
## Attaching package: 'zoo'
{% endhighlight %}



{% highlight text %}
## The following object(s) are masked from 'package:base':
## 
## as.Date, as.Date.numeric
{% endhighlight %}



{% highlight r %}

json_file <- "../dates_events.json"
json_data <- fromJSON(readLines(json_file))
{% endhighlight %}



{% highlight text %}
## Warning: incomplete final line found on '../dates_events.json'
{% endhighlight %}



{% highlight r %}

events <- ldply(json_data, data.frame)
events$count <- rep(1, nrow(events))

t <- aggregate(events$count, list(ym = format(as.Date(events$date, "%Y-%m-%d"), 
    "%Y-%m")), sum)

# plot(ts(t$x, frequency=12, start = c(2004,5))) format(data.frame(data =
# seq(as.Date('2004-05-01'), by = '1 month', to = as.Date('2013-12-31'))
# ), '%Y-%m')

z <- zoo(1:nrow(t), as.yearmon(t$ym))

g <- seq(start(z), end(z), 1/12)

events.count_by_month <- merge(data.frame(ym = g), data.frame(ym = as.yearmon(t$ym), 
    count = t$x), by = "ym", fill = 0, all.x = TRUE)

# cleaning the workspace
rm(t, z, g)

head(events.count_by_month[order(-events.count_by_month$count), ], n = 12)
{% endhighlight %}



{% highlight text %}
##          ym count
## 95 Mar 2012    35
## 93 Jan 2012    30
## 98 Jun 2012    29
## 91 Nov 2011    24
## 97 May 2012    23
## 90 Oct 2011    22
## 96 Apr 2012    21
## 83 Mar 2011    18
## 84 Apr 2011    17
## 94 Feb 2012    17
## 78 Oct 2010    16
## 81 Jan 2011    16
{% endhighlight %}



{% highlight r %}

kw <- unique(data.frame(event_id = events$event_id, keywords = events$keywords))
kw <- subset(kw, keywords != "")
kw <- unlist(strsplit(tolower(as.character(kw$keywords)), split = ","))

keywords.freq <- as.data.frame(table(unlist(kw)))

# cleaning the workspace
rm(kw, json_data, json_file)

head(keywords.freq[order(-keywords.freq$Freq), ], n = 12)
{% endhighlight %}



{% highlight text %}
##                     Var1 Freq
## 160   digital humanities   58
## 325             internet   19
## 286 humanités numériques   17
## 101        communication   16
## 201 édition électronique   14
## 262             histoire   14
## 307         informatique   14
## 443            numérique   14
## 661                  web   14
## 28              archives   12
## 615                  tei   12
## 445         numérisation   11
{% endhighlight %}


### nettoyage des données avec open refine

## analyse

### temporalités


{% highlight r %}
plot(events.count_by_month)
{% endhighlight %}

![plot of chunk unnamed-chunk-2](figure/unnamed-chunk-2.png) 


L'analyse des séries temporelles nous montre surtout la dépendance aux cycles académiques organisés autour (ou entres) les grandes vacances scolaires contrairement à l'année civile. Les données couvrant une faible fenêtre de temps ne nous permettent pas de conclure à grand chose.

Pour le sport :

- montrer les cycles et la montée annuelle puis déclin
- à comparer avec les cycles annuels de la vie académique

### fréquence des mots clés


{% highlight r %}
library("ggplot2")

theme_set(theme_bw())

keywords.freq.top50 <- transform(keywords.freq[order(-keywords.freq$Freq), ][1:50, 
    ], Var1 = reorder(Var1, Freq))

# barplot( keywords.freq$Freq[ order( - keywords.freq$Freq ) ][1:50],
# names.arg = keywords.freq$Var1[ order( - keywords.freq$Freq ) ][1:50],
# las = 2, cex.names = 0.5, horiz = TRUE )

ggplot(keywords.freq.top50, aes(x = Var1, y = Freq)) + geom_bar(stat = "identity") + 
    # theme( axis.text.x = element_text(angle = 90, hjust = 1, vjust = 0.5) )
# +
coord_flip()
{% endhighlight %}

![plot of chunk unnamed-chunk-3](figure/unnamed-chunk-3.png) 


### co-occurences

## futurs

- voir la différence avec l'ensemble des événements
- produire une cartographie
- détection des entités nommées

## todo


{% highlight r %}
save(list = c("events"), file = "calenda-dh.RData")
{% endhighlight %}