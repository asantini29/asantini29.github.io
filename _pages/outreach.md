---
title: "Outreach"
layout: page
permalink: /outreach/
---

# Outreach

{% comment %}Outreach comes from myCV's data/outreach.yml (see scripts/sync_cv.py).{% endcomment %}
{% assign entries = site.data.outreach | where_exp: "o", "o.website != false" %}

{% if entries.size > 0 %}
<div class="section-card" markdown="0">
{% for item in entries %}{% include talk.html talk=item %}{% endfor %}
</div>
{% else %}
<p class="text-muted">No outreach listed yet. Add entries to <code>data/outreach.yml</code> in the myCV repository.</p>
{% endif %}
