---
title : "dh.events : Analyse de mots clés"

tags:
  - r
  - keywords analysis

layout: default
---

## transformation des données de base

Nous allons reprendre les données structurées de l'extraction des événements de calenda pour construire des jeux de données de séries temporelles et co-occurrences de mots-clés.


{% highlight r %}
load("data/calenda-dh.RData")
{% endhighlight %}

{% highlight r %}
# détection des doublons
events <- events[!duplicated(events[, c("date", "title")]), ]

head(events, n = 12)
{% endhighlight %}



{% highlight text %}
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
{% endhighlight %}


Les données sont présentées sous la forme d'une ligne par événements et la liste des mots clés dans un champ unique mais séparés par des virgules. Toute la difficulté sera donc de transformer un data frame de taille `n` en un autre data frame de description atomique des mots-clés de taille :

m = somme de nombre de mots clés pour les mots événements i = 0..n

Cela sera également l'occasion de se frotter un peu à la librairie [plyr](http://plyr.had.co.nz/) spécialisé dans la manipulation de données


{% highlight r %}
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

keywords <- data.frame()

add_keyword <- function(row) {
    if (row$keywords != "") {
        l_ply(strsplit(as.character(row$keywords), ","), function(item) {
            keywords <<- rbind(keywords, data.frame(event_id = row$event_id, 
                date = as.Date(row$date, "%d-%m-%Y"), keyword = tolower(as.character(item))))
        })
    }
}

d_ply(events, .(date, keywords, event_id), add_keyword)

# remove duplicate keywords
keywords <- keywords[!duplicated(keywords), ]

head(keywords, n = 20)
{% endhighlight %}



{% highlight text %}
##                     event_id       date                keyword
## 1  http://calenda.org/197623 2004-10-15          communication
## 2  http://calenda.org/197736 2005-04-30          organisations
## 3  http://calenda.org/197736 2005-04-30          communication
## 4  http://calenda.org/198145 2007-05-10              éducation
## 5  http://calenda.org/198202 2007-10-15              recherche
## 6  http://calenda.org/198481 2008-09-09          communication
## 7  http://calenda.org/198481 2008-09-10          communication
## 8  http://calenda.org/198481 2008-09-11          communication
## 9  http://calenda.org/198481 2008-09-12          communication
## 10 http://calenda.org/198744 2009-10-15                  sfsic
## 11 http://calenda.org/198744 2009-10-15            information
## 12 http://calenda.org/198744 2009-10-15          communication
## 13 http://calenda.org/198928 2009-10-15 histoire contemporaine
## 14 http://calenda.org/198928 2009-10-15              numérique
## 15 http://calenda.org/198928 2009-10-15                digital
## 16 http://calenda.org/198746 2009-09-07                  livre
## 17 http://calenda.org/198746 2009-09-07                  ebook
## 18 http://calenda.org/198746 2009-09-07                lecture
## 19 http://calenda.org/198746 2009-09-07               écriture
## 20 http://calenda.org/198746 2009-09-08                  livre
{% endhighlight %}


### pondération des événements qui se répètent

Que faire des mots-clés s'appliquant à des événements qui se répètent dans le temps. Nous proposons de les pondérer de la façon suivante :

1. 1/(nombre de dates)


{% highlight r %}

weights <- as.data.frame(sapply(keywords$event_id, function(e) {
    1/nrow(events[events$event_id == e, ])
}))

keywords.aggregate <- cbind(keywords, weights)

colnames(keywords.aggregate)[4] <- c("weight")

rm(weights)

# vérification aggregate( keywords.aggregate$weight, list( kw =
# keywords.aggregate$keyword, id = keywords.aggregate$event_id), sum )
# doit renvoyer un tableau de kws = 1

head(keywords.aggregate[, c("keyword", "weight")])
{% endhighlight %}



{% highlight text %}
##         keyword weight
## 1 communication   1.00
## 2 organisations   1.00
## 3 communication   1.00
## 4     éducation   1.00
## 5     recherche   1.00
## 6 communication   0.25
{% endhighlight %}


### calcul de la date moyenne


{% highlight r %}
mean_date <- as.data.frame(sapply(keywords$keyword, function(e) {
    mean(keywords[keywords$keyword == e, ]$date)
}))

keywords.aggregate <- cbind(keywords.aggregate, mean_date)

colnames(keywords.aggregate)[5] <- c("mean_date")

rm(mean_date)

head(keywords.aggregate[, c("keyword", "mean_date")])
{% endhighlight %}



{% highlight text %}
##         keyword mean_date
## 1 communication     14926
## 2 organisations     12903
## 3 communication     14926
## 4     éducation     15310
## 5     recherche     15077
## 6 communication     14926
{% endhighlight %}


Cela permet de reconstituer un poid de 1 quand on fait la somme de tous les événements dans le temps.

Permet également d'"étaler" le poid des évènements.

Est-ce qu'on ne perd pas la "densité" ?

## Top 10


{% highlight r %}
keywords.count <- as.data.frame(table(unlist(keywords$keyword)))

colnames(keywords.count)[1] <- c("keyword")
colnames(keywords.count)[2] <- c("count")

keywords.count <- keywords.count[order(-keywords.count$count), ]

head(keywords.count, n = 10)
{% endhighlight %}



{% highlight text %}
##                  keyword count
## 15    digital humanities   140
## 84                   web    52
## 78              internet    49
## 9              numérique    46
## 153         informatique    43
## 149             histoire    39
## 19  humanités numériques    38
## 25  édition électronique    30
## 345          philosophie    30
## 1          communication    28
{% endhighlight %}



Rien de notable dans l'analyse du top 10. "digital humanities" (n=140) ressort grand vainqueur mais talonné par web+internet (n=101). A voir avec l'hypothèse que l'émergence du champ est possible à cause de l'existence d'une infrastructure adéquat (l'internet) qu'il soit compris ou non par les acteurs mais permet une stratégie de champ masqué.

On y retrouve également les tensions habituelles dans la traduction de "digital" qui peut se transformer en "numérique" :

- "humanités digitales" : 3
- "humanités numériques" : 38

- "digital" : 12
- "numérique" : 46

## pattern de visualisation des distributions journalières


{% highlight r %}
library(ggplot2)
theme_set(theme_bw())

viz.timeline <- function(dataset) {
    ggplot(dataset) + aes(x = date, y = reorder(keyword, -mean_date), size = weight, 
        color = reorder(keyword, -mean_date), alpha = 0.7) + geom_point() + 
        scale_y_discrete(name = "") + theme(legend.position = "none")
}
{% endhighlight %}


### distribution journalière du top 50


{% highlight r %}
# t <- keywords.aggregate[ keywords.aggregate$date > as.Date('2009-01-01')
# & keywords.aggregate$date < as.Date('2013-12-31'), ]

t <- subset(keywords.aggregate, keyword %in% keywords.count[1:50, 1])

t <- aggregate(t$weight, list(weight = t$weight, date = t$date, mean_date = t$mean_date, 
    keyword = t$keyword), sum)

# ca aurait pu être utile s'il y avait des cas d'événements qui se
# superposent ET qui utilisent les mêmes mots clés
t[t$weight > 1, ]
{% endhighlight %}



{% highlight text %}
## [1] weight    date      mean_date keyword   x        
## <0 rows> (or 0-length row.names)
{% endhighlight %}



{% highlight r %}


viz.timeline(t) + xlim(as.Date("2009-01-01"), as.Date("2013-12-31"))
{% endhighlight %}

![plot of chunk distribution_top50_time](figure/distribution_top50_time.png) 

{% highlight r %}

rm(t)
{% endhighlight %}


C'est joli mais on n'y voit pas forcément plus clair sur les patterns et la chronologie du champ sémantique. On peut en tout cas voir que les chercheurs du champ sont du genre à profiter des grandes vacances pour ne pas communiquer.

### conflits dans la disponibilité des dates


{% highlight r %}
events.duplicated_date <- events[duplicated(events[, c("date")]) | duplicated(events[, 
    c("date")], fromLast = TRUE), c("date", "title")]
events.duplicated_date <- events.duplicated_date[order(events.duplicated_date$date), 
    ]
{% endhighlight %}


On peut voir que 248 ont lieu un jour où un autre événement à lieu. Cela concerne exactement 108 jours. Soit 2.2963 événements par lors des journées chargées en communications.


{% highlight r %}
keywords.duplicated_date <- keywords[duplicated(keywords[, c("date", "keyword")]) | 
    duplicated(keywords[, c("date", "keyword")], fromLast = TRUE), ]

keywords.duplicated_date$keyword
{% endhighlight %}



{% highlight text %}
##  [1] réseaux sociaux      réseaux sociaux      digital humanities  
##  [4] digital humanities   digital humanities   digital humanities  
##  [7] histoire             histoire             digital humanities  
## [10] digital humanities   édition savante      scholarly edition   
## [13] philologie           philology            humanités numériques
## [16] digital humanities   humanités numériques digital humanities  
## [19] édition savante      scholarly edition    philologie          
## [22] philology            digital humanities   archives ouvertes   
## [25] archives ouvertes    digital humanities   digital humanities  
## [28] digital humanities   digital humanities   digital humanities  
## [31] design               post-doctorat        post-doctorat       
## [34] design               digital humanities   digital humanities  
## [37] digital studies      digital humanities   digital studies     
## [40] digital humanities   digital studies      digital humanities  
## [43] digital studies      digital humanities   digital studies     
## [46] digital humanities   digital studies      digital humanities  
## [49] digital studies      digital humanities   digital studies     
## [52] digital humanities   digital studies      digital humanities  
## [55] digital studies      digital humanities   digital studies     
## [58] digital humanities   digital studies      digital humanities  
## [61] digital studies      digital humanities   digital studies     
## [64] digital humanities   digital studies      digital humanities  
## [67] digital studies      digital humanities   digital studies     
## [70] digital humanities   digital studies      digital humanities  
## 676 Levels: communication organisations éducation recherche ... documents visuels
{% endhighlight %}



{% highlight r %}

head(keywords.duplicated_date)
{% endhighlight %}



{% highlight text %}
##                      event_id       date            keyword
## 296 http://calenda.org/202029 2010-11-18    réseaux sociaux
## 304 http://calenda.org/202115 2010-11-18    réseaux sociaux
## 363 http://calenda.org/202115 2011-04-07 digital humanities
## 373 http://calenda.org/203404 2011-04-07 digital humanities
## 391 http://calenda.org/202115 2011-05-05 digital humanities
## 401 http://calenda.org/203404 2011-05-05 digital humanities
{% endhighlight %}


12 mots-clés ont été choisi pour des événements concurrents dispersés sur 20 dates différentes. Parmi ceux-ci, on retrouve en bonnes places les usual suspects.

hypothèses :

- les chercheurs sont des feignassent et placent des événements aléatoirement mais en fonction de critères arbitraires communs comme la préférence pour la fin de semaine, le mercredi etc

---
Analyse fausse :

pourtant aucun ne semble poser de conflits en termes de mots clés, on peut donc poser l'hypothèse que les acteurs qui programment des événements concurrents le font :

1. avec la conscience de ne pas empiéter sur un territoire
2. font parti de régimes discursifs clos qui ne communiquent pas et ainsi n'ont pas conscience de la simultanéité d'autres événements
3. une concurrence intentionnelle marquée d'une stratégie d'originalité

## patterns de distribution mensuelle


{% highlight r %}
keywords.count.by_month <- aggregate(keywords.aggregate$weight, list(keyword = keywords.aggregate$keyword, 
    mean_date = keywords.aggregate$mean_date, date = as.Date(format(keywords.aggregate$date, 
        "%Y-%m-01"))), sum)

colnames(keywords.count.by_month)[4] <- c("weight")

head(keywords.count.by_month[order(-keywords.count.by_month$weight), ], n = 10)
{% endhighlight %}



{% highlight text %}
##                 keyword mean_date       date weight
## 1021 digital humanities     15342 2012-03-01  5.833
## 849  digital humanities     15342 2012-01-01  5.167
## 717  digital humanities     15342 2011-11-01  4.167
## 680            internet     15230 2011-11-01  3.182
## 594  digital humanities     15342 2011-06-01  3.111
## 787  digital humanities     15342 2011-12-01  3.083
## 661  digital humanities     15342 2011-10-01  3.000
## 938  digital humanities     15342 2012-02-01  2.417
## 1206                web     15399 2012-05-01  2.286
## 409        informatique     15198 2011-03-01  2.250
{% endhighlight %}



{% highlight r %}

viz.timeline(subset(keywords.count.by_month, keyword %in% keywords.count[1:50, 
    1])) + xlim(as.Date("2009-01-01"), as.Date("2013-12-31"))
{% endhighlight %}

![plot of chunk distribution_top50_time_monthly](figure/distribution_top50_time_monthly.png) 


### mois le plus actif


{% highlight r %}
months.weight <- aggregate(keywords.count.by_month$weight, list(date = keywords.count.by_month$date), 
    sum)

colnames(months.weight)[2] <- c("weight")

months.weight[order(-months.weight$weight), ][1:10, ]
{% endhighlight %}



{% highlight text %}
##          date weight
## 35 2012-06-01  83.39
## 28 2011-11-01  71.72
## 34 2012-05-01  68.96
## 30 2012-01-01  67.52
## 32 2012-03-01  67.22
## 41 2012-12-01  48.94
## 42 2013-01-01  47.61
## 33 2012-04-01  44.50
## 43 2013-02-01  43.78
## 31 2012-02-01  43.64
{% endhighlight %}


## Appendices

### distribution journalière de tous les événements


{% highlight r %}
t <- keywords.aggregate[keywords.aggregate$date > as.Date("2009-01-01") & keywords.aggregate$date < 
    as.Date("2013-12-31"), ]

viz.timeline(t)
{% endhighlight %}

![plot of chunk distribution_overtime](figure/distribution_overtime.png) 

{% highlight r %}

rm(t)
{% endhighlight %}