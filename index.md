---
title: home
---

<h2>readings</h2>

<h3>articles</h3>

{% for p in site.categories.articles %}
- <a href="{{ p.url }}">{{ p.title }}</a>
{% endfor %}

<h3>books</h3>

{% for p in site.categories.books %}
- <a href="{{ p.url }}">{{ p.title }}</a>
{% endfor %}