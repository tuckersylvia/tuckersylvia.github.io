---
layout: default
title: Tucker Sylvia dot com
---

# Welcome!

You have arrived to the personal website of Tucker Sylvia.
This is a pretty new and back burner project so please be patient
with the slow constrution progress. 

I am a masters student at URI-GSO studying subduction zone geodynamics.
You can reach me at: proception [at] gmail [dot] com

here is a handy list of posts 

<ul>
  {% for post in site.posts %}
    <li>
      <a href="{{ post.url }}">{{ post.title }}</a>
      {{ post.excerpt }}
    </li>
  {% endfor %}
</ul>
