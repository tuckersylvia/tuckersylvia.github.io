---
title: First post!
date: 2017-01-13 00:50:00 Z
tags:
- testing
- jekyll
layout: post
author: Tucker Sylvia
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
