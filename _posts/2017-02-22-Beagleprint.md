---
published: false
---
##Beagleprint


Well, here is going to be my first shot at a bonafide blog post. I have decided that the main purpose of this blog will be to document little side projects I complete and problems I manage to solve at home, work, hobbying, and in general. Many of the posts will probably come out as just a culmination of links and research that I have done, but for me that provides a convenient place to go back and find resources without digging through my gargantuan pile of semi-organized bookmarks.

So, without further ado, I will now present you with a description and guide to how I set up my new 3D printer and an Octorpint server running on a Beaglebone black to control it over the network.

###3D Printer and Configuration:


I really wanted a 3D printer for Christmas, and thanks to the Amazon gift card gods and many generous donations gifts from family and friends I was able to purchase a Monoprice Maker Select v2.1 (I think, versions are sketchy when dealing with rebranded Chinese stuff. This is a rebranded Wanhao Duplicator i3). I decided on this model because it has all the relevant features, a large community for support and advice, and an unbeatable price at $330.

During my primary research phase I did a lot of reading. Prior to taking the plunge I came to the conclusion that although this model requires some tinkering to get it to print optimally that is infact exactly what I was looking for in the hobby. I like to solve problems, but nobody wants a headache, which is what you get with some of the other, cheaper kits out there. This printer comes basically assembled and ready to print out of the box to get you going, then as you gain experience little issues become apparent and give you managable things to tweak, more of a ramp than a wall.

There were some other candidates: the Monoprice Maker Select Mini, genuine Prusa i3, factory Wanhao Duplicator i3 Plus (refresh of this model), basically anything in the $250-$500 range that was Cartesian and not a total turd. The deciding factor for me really was the community documentation. There are alot of i3 clones out there, but I think that the information is so readily available for this printer that it just makes sense, there are probably 10,000 of these things in active use.

I opted for the v2 over the plus because I liked the idea of an external control box. If the power supply does ever go up in flames it is not directly under the bed like the newer model. Additionally there is plenty of room for mods: I plan to add some relays to control lights and power via the Beaglebone, and eventually mount the Beaglebone itself into the control box too. Finaly, the actual hardware specs are basically identical and I couldn't justify an extra ~$100 just for the relocated controls when I could allocate those resources to buy a few spools of filament.

Speaking of filament, I bought and will continue to buy mine from MakerGeeks. They make it themselves in the USA to a very high standard, and have fantastic prices. I opted to get the limited time grab bag and bought four spools for $60, which is fscking awesome. I got two ABS and two PLA, you don't get to choose color but it's not like I have any specific projects or anything. I ended up with red and yellow PLA and black and green ABS.

When the magic man in the brown truck delivers your printer you open the box (right side up... trust me) and the unit is in three pieces that are fully wired together so you have to take some care to get it all oriented correctly. Simple instructions (could be a little more descriptive) show you where to insert like four screws and then your off. Pry the factory test print off the bed, level the bed, and print away withi one of the four models that come on the supplied SD card (which is not total and utter crap surprisingly). The files on my card were numbered, but theres a flat butterfly, a baby elephant, a cushy chair, and a swan, I think in that order, your milage may vary.

After you burn through the included "10 m" (more like 10 ft) of filament you will inevitably have some work to do. This is where all that great community documentation comes in. I have found this to be the best starting point. you will most certainly want to rpint up some parts to beef up the rigidity of the frame. I have not printed the Z braces as of yet because i want to do them in ABS and have not gotten all the settings down for good ABS prints yet. I printed the [DiiiCooler] though and holy mackeral has it helped.

You will want some extra tools too, namely a little level to check all your guide rods and frame alignment (and the table the printer is on... mine was horribly off kilter and I had to compensate with some cedar shingle wedges on the two fron feet), Xacto knife, CA glue, zip ties, acetone, rubbing alcohol, and certainly some metric hex drivers. I have found that the plastic build surface is sticky enough for both PLA and ABS as long as wou wipe it with isopropyl first to remove any grease or residue.

###Octoprint config

getting in from the internet

ssh tunneling

issues, resets, bad serial, etc. probably need a nice new usb cable.