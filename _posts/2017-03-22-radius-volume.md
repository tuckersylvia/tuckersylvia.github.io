---
layout: post
title: Radius Volume Relationships of Spheres
date: '2017-03-22 23:50:00 -0400'
author: Tucker Sylvia
published: true
mathjax: true
tags: [math, random, Stokes, physics, scaling, science]

---

### Reminder: You should still be learning something new everyday!

So I had a fairly simple question while writing my thesis the other day. I was writing about Stokes rise and buoyant settling / ascent of spherical bodies in a viscous fluid. I wanted to know what the change in terminal velocity was if you doubled the spheres volume keeping all other parameters (density contrast, ambient viscosity) constant. Below I will show you the simple relationships and assumptions I used to get an estimate for this quantity. Along the way we will touch on what I think has been the most valuable skill I have learned in my time at graduate school: **estimation and back of the envelope calculations**.

If you can reasonably estimate characteristic properties of whatever problem or system is concerning you then you can say a lot about it in a very robust way. Sure, you may not encompass all the details at all scales but you will definitely be able to make reasonable estimates and assertions. Sometimes you will hear this practice referred to as *scaling arguments, dimensional analysis, or nondimensionalization*. This is actually what differentiates most disciplines concerned with studying dynamical systems: the assumptions we make and scalings we choose define the simplifications we can make to our equations, which for most practical purposes start out the same (or are at least constructed from the same building blocks).

My masters research has focused on subduction zone geodynamics, specifically physical-tectonic-fluid dynamic analogue laboratory modeling of the viscously creeping [mantle wedge](https://en.wikipedia.org/wiki/Mantle_wedge). This project has led me down quite a few rabbit holes over the past three years and I have learned a lot of little tidbits along the way from a range of seemingly disparate fields: geology and geophysics, numerical methods and computational simulation, image processing and computer vision, electrical and mechanical engineering, differential equations and linear algebra, computer science and programming, and more. I wish I could fit all of it onto my CV but it would be *wicked* long.

(For the uninitiated, *wicked* is a term of endearment where I'm from in Rhode Island, the smallest of the United States. The best things in life are *wicked awesome*, like [Del's](https://en.wikipedia.org/wiki/Del's) frozen lemonade and coffee [Awful Awful's](https://www.google.com/search?q=awful+awful&oq=awful+a&aqs=chrome.0.0j69i57j0l4.1897j0j7&sourceid=chrome&ie=UTF-8).)

### Volume of a sphere:
Back to our scheduled programming, I needed to take a break from writing and figure out this problem.
The volume of a sphere is defined as:

$$ V = \frac{4}{3} \pi r^3 $$

We can rearrange this to calculate the radius from a known volume:

$$ r = \sqrt[3]{\frac{3}{4\pi} V} $$

Using a unit volume of Unity and doubling it we can calculate two *dimensionless* (kinda) radii to use in calculating a  scaling factor:

$$ r_1 = \sqrt[3]{\frac{3}{4\pi} (1)} = \frac{\sqrt[3]{\frac{3}{\pi}}}{2^{2/3}} \approx 0.620 $$

$$ r_2 = \sqrt[3]{\frac{3}{4\pi} (2)} = \sqrt[3]{\frac{3}{2\pi}} \approx 0.782 $$

Taking the ratio of those two yields a nice scaling factor:

$$ \frac{\sqrt[3]{\frac{3}{2\pi}}} {\frac{\sqrt[3]{\frac{3}{\pi}}}{2^{2/3}}} = \sqrt[3]{2} \approx 1.26 $$

Or in other words, a ~26% increase in radius for a doubling in volume.

This is a nice relationship to know in general for the future. It allows us to guestimate a radius from a volume *change* and not have to explicitly calculate it from known volume.

Another, probably more refined approach in contrast with the *plug-and-chug* method used above would be to rearrange the volume equation as we did above to get a function for radius r as a function of V, r(V). Then just take the derivative to get r(V)' or dr/dV, the change in radius with respect to a change in volume. This would give us a more generic function to explore other specific volume changes besides doubling. I should probably do that and plot it below...**TODO**

### Stokes Law:
Now that we know how much the radius will change for a doubling of volume we need to know what affect that will have on the Stokes terminal velocity.

Stokes law for the terminal velocity of a spherical body sinking or falling through a fluid is defined by the balance of the gravitational forces with the buoyancy and drag forces: **Fg = Fb + Fd**. A few nice breakdown articles can be found at the [World of Physics](http://scienceworld.wolfram.com/physics/StokesVelocity.html) and [WikiPedia](https://en.wikipedia.org/wiki/Stokes%27_law#Terminal_velocity_of_sphere_falling_in_a_fluid). The end result after some rearranging for terminal velocity is:

$$ v_t = \frac{2}{9} \frac{g(\rho^{'} - \rho) r^2}{\eta} $$

If we assume that the density contrast and matrix viscosity remain constant we can use the same *plug and chug* approach as before substituting in Unity and 1.26 for values of the radius.

$$  C = \frac{2}{9} \frac{g(\rho^{'} - \rho)}{\eta} = constant $$

$$ v_1 = C (1)^2 = C $$

$$ v_{1.26} = C (1.26)^2 \approx 1.59 C $$

This shows that there is a ~59% increase in the terminal Stokes velocity for a sphere with double the volume in the same fluid environment. Pretty neat.

### Closing remarks:
Well, there was not really any traditional scaling analysis here but you can hopefully still see how *nondimensionalization* (in my very broad sense) can be utilized to gain insight into all kinds of problems.

We have also learned that if you let two balloons go at the same time and one contains twice the volume of helium it will ascend 60% faster than the smaller one when they reach their respective terminal velocities. The larger balloon would also accelerate faster and get to terminal velocity more quickly too, but that is not part of this story... yet. If you get in a balloon race any time soon you now know how to win.
