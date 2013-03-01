---
title : dh.events : Analyse de mots clés

tags:
  - r
  - keywords analysis

layout: default
---

## transformation des données de base

Nous allons reprendre les données structurées de l'extraction des événements de calenda pour construire des jeux de données de séries temporelles et co-occurrences de mots-clés.


```r
load("data/calenda-dh.RData")

head(events, n = 12)
```

```
##          date                    keywords                  event_id
## 1  01-05-2004                             http://calenda.org/197588
## 2  15-10-2004               communication http://calenda.org/197623
## 3  30-04-2005 organisations,communication http://calenda.org/197736
## 4  01-10-2005                             http://calenda.org/197799
## 5  12-02-2007                             http://calenda.org/198084
## 6  12-03-2007                             http://calenda.org/198084
## 7  10-05-2007                   éducation http://calenda.org/198145
## 8  11-06-2007                             http://calenda.org/198160
## 9  15-10-2007                   recherche http://calenda.org/198202
## 10 09-09-2008               communication http://calenda.org/198481
## 11 10-09-2008               communication http://calenda.org/198481
## 12 11-09-2008               communication http://calenda.org/198481
##                                                                                                    title
## 1                                                       Professeur de SES pour l'animation du site DESCO
## 2                                                               60 ans de communication du développement
## 3                                                                    Culture des organisations et DISTIC
## 4                                       La presse ouvrière lyonnaise du début de la Monarchie de Juillet
## 5                                                                 eCommerce et Gouvernance de l'Internet
## 6                                                                 eCommerce et Gouvernance de l'Internet
## 7  Le Dictionnaire de pédagogie et d'instruction primaire de Ferdinand Buisson : d'une édition à l'autre
## 8                                            Agrégé-e de SES chargé-e du développement et de l'animation
## 9                                            Sciences Humaines et Sociales et éthique de la recherche   
## 10                        Le déploiement des Tics dans l'enseignement supérieur : évidences et tendances
## 11                        Le déploiement des Tics dans l'enseignement supérieur : évidences et tendances
## 12                        Le déploiement des Tics dans l'enseignement supérieur : évidences et tendances
##    count
## 1      1
## 2      1
## 3      1
## 4      1
## 5      1
## 6      1
## 7      1
## 8      1
## 9      1
## 10     1
## 11     1
## 12     1
```


Les données sont présentées sous la forme d'une ligne par événements et la liste des mots clés dans un champ unique mais séparés par des virgules. Toute la difficulté sera donc de transformer un data frame de taille `n` en un autre data frame de description atomique des mots-clés de taille :

m = somme de nombre de mots clés pour les mots événements i = 0..n

Cela sera également l'occasion de se frotter un peu à la librairie [plyr](http://plyr.had.co.nz/) spécialisé dans la manipulation de données


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

keywords <- data.frame()

add_keyword <- function(row) {
    if (row$keywords != "") {
        l_ply(strsplit(as.character(row$keywords), ","), function(item) {
            keywords <<- rbind(keywords, data.frame(event_id = row$event_id, 
                date = row$date, keyword = as.character(item)))
        })
    }
}

d_ply(events, .(date, keywords, event_id), add_keyword)

head(keywords, n = 20)
```

```
##                     event_id       date                keyword
## 1  http://calenda.org/197623 15-10-2004          communication
## 2  http://calenda.org/197736 30-04-2005          organisations
## 3  http://calenda.org/197736 30-04-2005          communication
## 4  http://calenda.org/198145 10-05-2007              éducation
## 5  http://calenda.org/198202 15-10-2007              recherche
## 6  http://calenda.org/198481 09-09-2008          communication
## 7  http://calenda.org/198481 10-09-2008          communication
## 8  http://calenda.org/198481 11-09-2008          communication
## 9  http://calenda.org/198481 12-09-2008          communication
## 10 http://calenda.org/198744 15-10-2009                  SFSIC
## 11 http://calenda.org/198744 15-10-2009            information
## 12 http://calenda.org/198744 15-10-2009          communication
## 13 http://calenda.org/198928 15-10-2009 histoire contemporaine
## 14 http://calenda.org/198928 15-10-2009              numérique
## 15 http://calenda.org/198928 15-10-2009                digital
## 16 http://calenda.org/198746 07-09-2009                  livre
## 17 http://calenda.org/198746 07-09-2009                  ebook
## 18 http://calenda.org/198746 07-09-2009                lecture
## 19 http://calenda.org/198746 07-09-2009               écriture
## 20 http://calenda.org/198746 08-09-2009                  livre
```


Que faire des mots-clés s'appliquant à des événements qui se répètent dans le temps. Nous proposons de les pondérer de la façon suivante :

1. 1/(nombre de dates)

Cela permet de reconstituer un poid de 1 quand on fait la somme de tous les événements dans le temps.

Permet également d'"étaler" le poid des évènements.

Est-ce qu'on ne perd pas la "densité" ?
