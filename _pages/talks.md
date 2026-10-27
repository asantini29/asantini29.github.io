---
title: "Talks"
layout: page
permalink: /talks/
math: true
---

# Talks

{% comment %}Talks come from myCV's data/talks.yml (see scripts/sync_cv.py).{% endcomment %}
{% assign talks = site.data.talks | where_exp: "t", "t.website != false" %}
{% assign groups = "invited:Invited Talks|contributed:Contributed Talks|poster:Posters" | split: "|" %}

{% for group in groups %}
{% assign type = group | split: ":" | first %}
{% assign entries = talks | where: "type", type %}
{% if entries.size > 0 %}
<div class="section-card" markdown="0">
<h2>{{ group | split: ":" | last }}</h2>
{% for talk in entries %}{% include talk.html talk=talk %}{% endfor %}
</div>
{% endif %}
{% endfor %}

{% unless talks.size > 0 %}
<p class="text-muted">No talks listed yet. Add entries to <code>data/talks.yml</code> in the myCV repository.</p>
{% endunless %}
