---
title: "Home"
layout: homelay
permalink: /
---

<h1 class="home-hero">{{ site.name }}</h1>
<p class="home-hero-sub">{{ site.title }}, {{ site.institution }}</p>

<div class="chip-container" markdown="0">
<a href="{{ '/research' | relative_url }}" class="chip">LISA Global Fit</a>
<a href="{{ '/research' | relative_url }}" class="chip">Extreme mass ratio inspirals</a>
<a href="{{ '/research' | relative_url }}" class="chip">Galactic Foreground</a>
<a href="{{ '/research' | relative_url }}" class="chip">Noise (mis)modelling</a>
<a href="{{ '/research' | relative_url }}" class="chip">Fast waveforms</a>
</div>

Welcome to my personal website! I am Alessandro Santini, a PhD candidate at the Max Planck Institute for Gravitational Physics (Albert Einstein Institute), and my work focuses on extracting astrophysical information from gravitational wave data.

Explore my website to learn more about me and my research, and feel free to reach out for any questions or potential collaborations!
<p style="margin: var(--space-4) 0 0;"><a href="{{ '/about' | 
relative_url }}">About me &rarr;</a></p>

<p style="margin: var(--space-4) 0 0;"><a href="{{ '/research' | relative_url }}">About my research &rarr;</a></p>

<!-- <div class="banner-frame" markdown="0">
<img src="{{ '/images/research/mojito-animation.gif' | relative_url }}" alt="Feynman diagrams" width="1400" height="449" loading="lazy">
<div class="banner-caption">Time evolution of a LISA-like data stream</div>
</div> -->

{% capture selected %}{% bibliography --query @*[selected=true] %}{% endcapture %}
{% if selected contains "pub-entry" %}
## Selected publications

<div class="section-card selected-pubs" markdown="0">
{{ selected }}
<p style="margin: var(--space-4) 0 0;"><a href="{{ '/publications' | relative_url }}">All publications &rarr;</a></p>
</div>
{% endif %}
