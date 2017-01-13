---
layout: default
title: First post!
date: 2017-01-12 20:50:00 -0400
---
## This is it

Well it seems that this would be thw way to test the blogging functionality of Jekyll ang GitHub Pages...


<ul>
  {% for post in site.posts %}
    <li>
      <a href="{{ post.url }}">{{ post.title }}</a>
    </li>
  {% endfor %}
</ul>

lets see how that worked... i dont think it will because its not in a layout but we will see

