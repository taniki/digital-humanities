---
title: Une analyse des évenements en SHS en Python et R

tags:
  - outils
  - code
  - r
  - lexicometry

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


```r
library("rjson")
library("plyr")
library("zoo")
```

```
## Attaching package: 'zoo'
```

```
## The following object(s) are masked from 'package:base':
## 
## as.Date, as.Date.numeric
```

```r

json_file <- "../dates_events.json"
json_data <- fromJSON(readLines(json_file))
```

```
## Warning: incomplete final line found on '../dates_events.json'
```

```r

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
```

```
##           ym count
## 177 Oct 0015     9
## 288 Jan 0025     9
## 360 Jan 0031     6
## 165 Oct 0014     5
## 170 Mar 0015     5
## 171 Apr 0015     5
## 173 Jun 0015     5
## 179 Dec 0015     5
## 214 Nov 0018     5
## 326 Mar 0028     5
## 328 May 0028     5
## 350 Mar 0030     5
```

```r

kw <- unique(data.frame(event_id = events$event_id, keywords = events$keywords))
kw <- subset(kw, keywords != "")
kw <- unlist(strsplit(tolower(as.character(kw$keywords)), split = ","))

keywords.freq <- as.data.frame(table(unlist(kw)))

# cleaning the workspace
rm(kw, json_data, json_file)

head(keywords.freq[order(-keywords.freq$Freq), ], n = 12)
```

```
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
```


### nettoyage des données avec open refine

## analyse

### temporalités


```r
plot(events.count_by_month)
```

![plot of chunk unnamed-chunk-2](figure/unnamed-chunk-2.png) 


L'analyse des séries temporelles nous montre surtout la dépendance aux cycles académiques organisés autour (ou entres) les grandes vacances scolaires contrairement à l'année civile. Les données couvrant une faible fenêtre de temps ne nous permettent pas de conclure à grand chose.

Pour le sport :

- montrer les cycles et la montée annuelle puis déclin
- à comparer avec les cycles annuels de la vie académique

### fréquence des mots clés


```r
library("ggplot2")

keywords.freq.top50 <- transform(keywords.freq[order(-keywords.freq$Freq), ][1:50, 
    ], Var1 = reorder(Var1, -Freq))

# barplot( keywords.freq$Freq[ order( - keywords.freq$Freq ) ][1:50],
# names.arg = keywords.freq$Var1[ order( - keywords.freq$Freq ) ][1:50],
# las = 2, cex.names = 0.5, horiz = TRUE )

ggplot(keywords.freq.top50, aes(x = Var1, y = Freq)) + geom_bar(stat = "identity") + 
    theme(axis.text.x = element_text(angle = 90, hjust = 1))
```

![plot of chunk unnamed-chunk-3](figure/unnamed-chunk-3.png) 


### co-occurences

## futurs

- voir la différence avec l'ensemble des événements
- produire une cartographie
- détection des entités nommées

## todo
