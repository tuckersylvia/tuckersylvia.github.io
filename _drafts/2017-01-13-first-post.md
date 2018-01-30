---
title: First post!
date: 2017-01-12 19:50:00 -05:00
published: true
layout: post
author: Tucker Sylvia
mathjax: false
description: "brief descriptive blurb for post listings and SEO"
tags:
- testing
- jekyll
---

### First post is here, checking excerpt

Well it seems that this would be thw way to test the blogging functionality of Jekyll ang GitHub Pages...

<ul>
  {% for post in site.posts %}
    <li>
      <a href="{{ post.url }}">{{ post.title }}</a>
    </li>
  {% endfor %}
</ul>

lets see how that worked... i dont think it will because its not in a layout but we will see

ill be damned it did now lets try the code syntax highlighting

{% highlight python linenos %}

import numpy as np
from matplotlib import pyplot as plt

def something(x,y,z):

    # checking syntax highlighting capabilities
    if x % y == z:
        print 'its a miricle!'
        return x*y*z

x = np.random(100)
y = np.exp(x)

plt.scatter(x,y)

{% endhighlight %}

and the verdict is... it worked!

Now lets try to see if we can execute js:
first lets try to include and highlight it

{% highlight javascript %}
{% include alert_msg.js %}
{% endhighlight %}

now lets try to include and run it

<script type="text/javascript" charset="utf-8">
  $(document).ready(function(){
    $("#submit").click(function(e){
      {% include alert_msg.js %}

      return false;
    })
  });
</script>

howd we do?

testing new page timestamp features:

### method 1)
Last modified at: {{ page.last-modified-date | date: '%B %d, %Y' }}

does not work on gh pages (--safe flag) because this uses custom plugin / Hooks there are other plugins (jekyll-last-modified-at and jekyl-last-modified ruby script), none whitelisted by or work with  gh pages

another workaround way is using site.time which will output the time of building / generation, not sure if this will be useful in live deployment (all files might end up with same build time?) but might be worth a shot...

### method 2)
Last ~~modified~~ *built* at: {{ site.time | date: '%B %-d, %Y' }}

see if live refresh is working or is it
