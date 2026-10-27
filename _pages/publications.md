---
title: "Publications"
layout: page
permalink: /publications/
---

# Publications

<input type="text" class="pub-search" id="pubSearch" placeholder="Filter by title, author, or year...">

<div class="section-card" id="pubList">
{% comment %}Each heading only appears when its list has entries.{% endcomment %}
{% capture preprints %}{% bibliography --query @unpublished %}{% endcapture %}
{% capture articles %}{% bibliography --query @article %}{% endcapture %}
{% capture proceedings %}{% bibliography --query @inproceedings %}{% endcapture %}
{% if preprints contains "pub-entry" %}
<h2>Preprints</h2>

{{ preprints }}
{% endif %}
{% if articles contains "pub-entry" %}
<h2>Refereed Journal Articles</h2>

{{ articles }}
{% endif %}
{% if proceedings contains "pub-entry" %}
<h2>Refereed Conference Proceedings</h2>

{{ proceedings }}
{% endif %}
</div>
