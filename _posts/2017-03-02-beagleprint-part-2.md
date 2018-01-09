---
title: Beagleprint Part 2
date: 2017-03-02 00:50:00 Z
published: false
tags:
- 3dprinting
- beaglebone
- octoprint
- server
- software
- linux
- hobby
layout: post
author: Tucker Sylvia
---

### Because one must have network control...

Here is the second and most likely last installment in the 3d printer - Beaglebone - Octoprint saga.

I hope to cover all of the software stuff here because I feel that most of the relevant hardware info was covered in [Part1](link to part one here).

### Non Printer Hardware
The Duplicator i# runs a Melzi board with a Repetier ased firmware. Octoprint picks it up no problem over USB/TTY with a reasonably modern kernal.

### Beaglebone Black
I am using a Beaglebone Black Rev A6. I jumped on the Beaglebone bandwagon early and I don't care. This thing cost me $55 in May 2013(14?) and still has the balls to run a full Debian system with a few daemons on like 1 Amp including accessories. The A6 is a little crippled compared the the newer C/Green revision of the board, but half a gig of RAM and 2 gigs of eMMC still works for me. I run it off the SD card slot anyway which I will get too in a few. These things go for a little less now and have a full gig of RAM and 4gb of eMMC with the same TI ARM cortex A7 processor (I think, don't quote me).

Whatever the specs and cost, Beaglebone Blacks (Greens) are a great RasPi alternative and have a little more capability as a Linux server. The Beaglebones are also lacking a bit in graphics capability compared to the Pi, but for a headless server that is not a factor. When I am running prints serving over the LAN or a VPN it uses around 3% CPU to control the print and maintain the server connection *including the webcam*. The only thing that uses a lot of resources is rendering the timelapse with **FFMPEG** which I think I have a work around for by compiling some libraries (libjpeg and libgphoto2, maybe libavtools etc.) and not using the ARM .debs.


### Octoprint config
Once you get a reasonable server up (OctoPi is dead easy for RasPi users, otherwise read on) the Octoprint setup is easy.

To get the Beaglebone Black (or Green or whawtever other SBC) ready you need to at least get a new copy of whatever OS you want to run. For me this was a Jessie image from the eLinux Beaglebone builds page. They offer standalone and installable versions. I chose the 4 Gb standalone version because I knew I would be running it off the SD slot indefinitely. If you want to flash it to the onboard eMMC you need to know the available capacity so you can use one of the prefab images or load your root on the onboard flash and everything else onto come other storage.

This is **not** a guide in Linux how-to, but I will tell you how I did it. With the old revisions of the board it is not feasible to use one of the prefab images to flash the onboard eMMC. It is not hard to enable the flasher on a smaller /custom image, and there is documentation to do that. I used the newest Debian Jessie image and dd'd it to an sd card:
~~~
dd if=beaglebone-image.iso of=/path/to/device
~~~
There are a few ways to do this, like if you download a zipped version:
~~~
xzcat file-i-downloaded.xz | dd /path/to/device
~~~

Seems like a problem you can find the answer to if you are reading this.

After that boot and disable all the BS you don't need: Apache, NodeJS, any other services that are on by default you don't want. Now would also be a good time to create a new user and add it to some privaleged groups:


#### getting in from the internet
You have options here

##### ssh tunneling

### issues, resets, bad serial, etc. probably need a nice new usb cable.
