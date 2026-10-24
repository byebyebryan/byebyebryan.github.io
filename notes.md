---
layout: default
title: Development notes
description: Decisions, experiments and practical lessons from building these projects.
permalink: /notes/
---

<header class="hero">
  <p class="eyebrow">Development notes</p>
  <h1>How the projects got here.</h1>
  <p class="lede">Decisions, experiments and practical lessons behind the tools.</p>
</header>

{% for post in site.posts %}
<article class="card note-entry">
  <p class="eyebrow">{{ post.date | date: "%b %-d, %Y" }}</p>
  <h2><a href="{{ post.url | relative_url }}">{{ post.title }}</a></h2>
  <p>{{ post.description }}</p>
</article>
{% endfor %}

<p class="back-link"><a href="{{ '/' | relative_url }}">← Selected projects</a></p>
