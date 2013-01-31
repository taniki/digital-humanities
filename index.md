---
title: home
layout: index
---

<h2>Étude</h2>

<h3>Questions</h3>

<ul>
{% for p in site.tags.question %}
<li><a href="{{ p.url }}">{{ p.title }}</a></li>
{% endfor %}
</ul>

<h3>Thèmes</h3>

<ul>
{% for p in site.tags.theme %}
<li><a href="{{ p.url }}">{{ p.title }}</a></li>
{% endfor %}
</ul>

<h2>Lectures</h2>

<h3>articles</h3>

<ul>
{% for p in site.categories.articles %}
<li><a href="{{ p.url }}">{{ p.title }}</a></li>
{% endfor %}
</ul>

<h3>books</h3>

<ul>
{% for p in site.categories.books %}
<li><a href="{{ p.url }}">{{ p.title }}</a></li>
{% endfor %}
</ul>