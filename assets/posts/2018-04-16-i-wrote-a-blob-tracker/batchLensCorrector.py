#!/usr/bin/env python
# -*- coding: utf_8 -*
#
# A Script to batch correct photo distortion using the Lenfun database.
# Should be usable for any camera in the lensfun db.
# 
# originally authored by Alex Mandel 2014
# tech@wildintellect.com
#
# modified by tucker sylvia feb 2016 to utilize
# my_undistort.py as module instead of standalone script
# also detects camera from image EXIF data using exiftool
# and calculates the distortion from camera properties


import os
import timeit #Add a timer
import myUndistort as mu


if __name__ == '__main__':

    #sample = "/Pictures/gopro/farm/color/3D_R0971.JPG"
    #undistortedImagePath ="testoutput.JPG"
    #sample = "/redwood/Photos/kite/gopro/2013-06-01-cloverleaf/corrected/multi"
    #directory = "/home/madadh/Pictures/odm/checkercalibration/measure"

    directory = os.getcwd()
    print 'current working directory: {}'.format(directory)
    
    try:
        os.chdir(directory)
        photos = mu.photolist(directory)

        tic=timeit.default_timer()
        #result = process_photos(photos)
        mu.multi_process(photos)
        toc=timeit.default_timer()
        totaltime = toc-tic
        nframes = len(photos)
        fps = nframes/totaltime
        #im = Image.open(sample)
        print '\n========== COMPLETE ==========\n'
        print 'Processed {:d} frames in {:6.3f} seconds, {:6.3f} fps'.format(nframes,
                 totaltime, fps)

    except Exception as e:
        print(" ".join(["Something failed because of",str(e)]))

