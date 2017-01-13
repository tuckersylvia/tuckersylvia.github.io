---
layout: default
title: Tucker Sylvia dot com
published: true
---

# Greetings Earthling!

## You have arrived to the personal website of Tucker Sylvia.
This is a pretty new and back burner project so please be patient
with the slow constrution progress. This will be my second personnal website, the first being another freely hosted deal from middle school. I don't think it is still alive but it used to reside at http://llamarkewl.gq.nu.

I am a currently masters student at the University of Rhode Island Graduate School of Oceanography. I primarily study subduction zone geodynamics using analogue laboratory models and computer vision with Chris Kincaid. Our lab group does all sorts of fluid dynamics from mantle convection to shellfish larval transport using integrated data and modeling methods.

You can reach me at: proception [at] gmail [dot] com

I have a university profile page at http://www.gso.uri.edu/profile/proception/

I plan to use this site to record all sorts of things such as general blog posts, code projects, household hacks, car maintenence, and any other info that I have spent enough effort compiling that I feel it is worth sharing. Additionally I eventually plan to create a page for my research and publications etc. Also a photo gallery would be pretty neat, we'll see how far I get. 

## For now here is a handy list of posts: 

<ul>
  {% for post in site.posts %}
    <li>
      <a href="{{ post.url }}">{{ post.title }}</a>
      {{ post.excerpt }}
    </li>
  {% endfor %}
</ul>

Insert slick social media footer here haha
