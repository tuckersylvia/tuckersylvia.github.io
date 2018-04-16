#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  2 09:43:57 2016

this script take input image source and allows for interactive
thresholding in hsv space. the results of the threshold can be saved
to a txt file in the image directory with s key. user should specify a
representative frame from a sequence so that this threshold can be
applied in batch with batch-hsv-thresh script.
can't really do this well in a notebook because plots don't refresh and 
interactive widgets are a pain in the ass and cv2 and notebooks don't play nice

@author: tucker
"""
#%% imports and function definitions

import cv2
import numpy as np
import argparse
import json
import os

def nothing(x):
    '''
    nothing function for trackbar callbacks to do... nothing!
    '''
    pass


# define a function to save the tweaked trheshold values to a file... or something
def saveThresh(lower, upper, blur, fname="../saved-thresholds.txt"):
    '''
    write out dict containing threshold min/max values to file
    '''
    # write lists / values to a file for recall
    # might be useful to turn into dict? or another data structure
    # Cpickle?
    # and the winner is a dict!
    # constructing a dict from the refpts list
    # crude but works because our list is known.
    threshdict = {'hmin':lower[0],
                  'hmax':upper[0],
                  'smin':lower[1],
                  'smax':upper[1],
                  'vmin':lower[2],
                  'vmax':upper[2],
                  'blur':blur[0],
                  'disk':blur[1],
                  'invert':blur[2]
                  }

    # dump json representation of dict to a txt file - easy to load
    json.dump(threshdict, open(fname,'w'))

    print 'sucessfully dumped threshdict to ../saved-thresholds.txt'

def getThresholds(fname='../saved-thresholds.txt'):
    '''
    loads two points from text file containing
    upper right and lower left corners and
    returns 4 values: xmin, xmax, ymin, and ymax
    '''
    threshdict = json.load(open(fname))

    return threshdict
#%% define source or get from arguments

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="Path to the image")
args = vars(ap.parse_args())
source = args["image"]

# hackey hardcoded sources used in testing and debugging
#source = "./Futurama*.avi"
#source = "./side/ED_6_side_%03d.jpg"
#cap = cv2.VideoCapture(source)
#source = "../images/D_14-top_2_undistorted.JPG"

frame = cv2.imread(source)

# scale factor for viewing entire image and scaling blur/morphological values
fs = 3.0 # factor to scale by
#%% Trackbars
# Creating a window for Trackbars to use
cv2.namedWindow('Trackbars')

# Creating track bars for each color channel min
cv2.createTrackbar('Hmin', 'Trackbars', 0, 179, nothing)
cv2.createTrackbar('Smin', 'Trackbars', 0, 255, nothing)
cv2.createTrackbar('Vmin', 'Trackbars', 0, 255, nothing)

# Creating track bars for each color channel max
cv2.createTrackbar('Hmax', 'Trackbars', 179, 179, nothing)
cv2.createTrackbar('Smax', 'Trackbars', 255, 255, nothing)
cv2.createTrackbar('Vmax', 'Trackbars', 255, 255, nothing)

# Creating track bars for alpha - blend of mask and frame weight
#cv2.createTrackbar('alpha', 'Trackbars', 0, 100, nothing)

# Creating trackbars for blur and disk kernel sizes
cv2.createTrackbar('Blur', 'Trackbars', 1, 55, nothing)
cv2.createTrackbar('Disk', 'Trackbars', 3, 77, nothing)

# Creating trackbars for inverting the mask, helpful if it is easier to mask out
# our desired objects rather than the background
cv2.createTrackbar('Invert', 'Trackbars', 0, 1, nothing)

#set some initial values

# if we have already done the masking before use that as a starting point
if os.path.isfile("../saved-thresholds.txt"):
    # load our saved threshold values
    threshdict = getThresholds()
    # set hue range
    cv2.setTrackbarPos('Hmin', 'Trackbars', threshdict['hmin'])
    cv2.setTrackbarPos('Hmax', 'Trackbars', threshdict['hmax'])
    #set saturation range
    cv2.setTrackbarPos('Smin', 'Trackbars', threshdict['smin'])
    cv2.setTrackbarPos('Smax', 'Trackbars', threshdict['smax'])
    # set value range
    cv2.setTrackbarPos('Vmin', 'Trackbars', threshdict['vmin'])
    cv2.setTrackbarPos('Vmax', 'Trackbars', threshdict['vmax'])

    # set blur and disk
    b0 = int(threshdict['blur']/fs)
    if b0 % 2 == 1:
        pass # if it is odd we are good
    else:
        b0 -= 1 # otherwise make it odd
        
    d0 = int(threshdict['disk']/fs)
    if d0 % 2 == 1:
        pass # if it is odd we are good
    else:
        d0 -= 1 # otherwise make it odd
        
    cv2.setTrackbarPos('Blur', 'Trackbars', b0)
    cv2.setTrackbarPos('Disk', 'Trackbars', d0)

    # check and set invert
    if 'invert' in threshdict.keys(): # check if it exists in our dict, old versions did not have this feature
        invert = threshdict['invert']
        cv2.setTrackbarPos('Invert', 'Trackbars', invert)
    
else: # otherwise this is the first time or we deleted our saved thresholds file
    # initialize hsv threshold values to prevent error with the first masking operation
    h0,s0,v0,a0 = 0,0,255,50
    b0, d0 = 5,19 # initial blur/disk params
    kBlurOld = b0 # keep the old blur size around for later
    invert = 0
    
    # setting initial trackbar positions
    cv2.setTrackbarPos('Hmin', 'Trackbars', h0)
    cv2.setTrackbarPos('Vmax', 'Trackbars', v0)
    #cv2.setTrackbarPos('alpha', 'Trackbars', a0)
    cv2.setTrackbarPos('Blur', 'Trackbars', b0)
    cv2.setTrackbarPos('Disk', 'Trackbars', d0)

    # setting inverted to false
    cv2.setTrackbarPos('Invert', 'Trackbars', invert)

#%% preprocessing before threshold
# resize - can also use imutils convenience functions
fs = fs # factor to scale by
sf = 1.0/fs # scale factor
frame = cv2.resize(frame, None, fx=sf, fy=sf, interpolation=cv2.INTER_AREA)
copy = frame.copy() # keep a copy

# initial blur
#b0 = cv2.getTrackbarPos('Blur', 'Trackbars')
kBlurOld = b0 # keep the old blur size around for later
frame = cv2.medianBlur(frame, b0)

#converting to HSV
hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)

# create a disk shaped structuring element once outside loop
#d0 = cv2.getTrackbarPos('Disk', 'Trackbars')
disk = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (d0,d0))

#%% main thresholding update loop

while(1):
    """
    can do all manipulations besides threshold on single frame outside of loop

    #_, frame = cap.read()

    # resize
    sf = 0.25
    res = cv2.resize(frame, None, fx=sf, fy=sf, interpolation=cv2.INTER_AREA)

    #blur
    ksize=9
    blurred = cv2.medianBlur(res, ksize)

    #converting to HSV
    hsv = cv2.cvtColor(blurred,cv2.COLOR_BGR2HSV)

    """

    # get info from Trackbars and create mask
    hmin = cv2.getTrackbarPos('Hmin', 'Trackbars')
    smin = cv2.getTrackbarPos('Smin', 'Trackbars')
    vmin = cv2.getTrackbarPos('Vmin', 'Trackbars')
    hmax = cv2.getTrackbarPos('Hmax', 'Trackbars')
    smax = cv2.getTrackbarPos('Smax', 'Trackbars')
    vmax = cv2.getTrackbarPos('Vmax', 'Trackbars')
    #alpha = cv2.getTrackbarPos('alpha', 'Trackbars')
    kBlur = cv2.getTrackbarPos('Blur', 'Trackbars')
    kDisk = cv2.getTrackbarPos('Disk', 'Trackbars')

    invert = cv2.getTrackbarPos('Invert', 'Trackbars')

    # only blur if we have moved the slider
    if kBlur > kBlurOld and kBlur %2 != 0:
        #blur
        frame = cv2.medianBlur(frame, kBlur)
        kBlurOld = kBlur

    elif kBlur < kBlurOld and kBlur %2 != 0:
        # first use copy
        frame = copy.copy()
        #blur
        frame = cv2.medianBlur(frame, kBlur)
        kBlurOld = kBlur

    #converting to HSV
    hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)

    # create a disk shaped structuring element with value from trackbar
    disk = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (kDisk,kDisk))

    # Normal masking algorithm
    lower_bounds = np.array([hmin, smin, vmin])
    upper_bounds = np.array([hmax, smax, vmax])

    # do some morphological operations to clean up the mask
    mask = cv2.inRange(hsv, lower_bounds, upper_bounds)
    #mask = cv2.erode(mask, disk, iterations=2)
    #mask = cv2.dilate(mask, disk, iterations=2)
    # checking if cv2.MORPH_OPEN gives different / better results than
    # the explicit erode then dilate (definition of open = erode then dilate)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, disk)
    #mask = cv2.bitwise_not(mask,mask)

    # invert the mask if we want to 
    if invert == 1:
        mask = cv2.bitwise_not(mask, mask)

    #show result
    result = cv2.bitwise_and(frame, frame, mask=mask)

    # rescaling alpha from 0-100 in trackbar to 0-1.0 interval
    # for use in cv2.addWeighted
    #alpha =float(alpha/100.)
    # blend the mask with the frame
    #frame = cv2.addWeighted(frame, alpha, result, (1-alpha), 0, frame)

    #stacked = np.hstack((result,mask))

    cv2.imshow('result', result)

    # break the loop
    key = cv2.waitKey(1) & 0xFF

   # 27 = Esc key
    if key == 27:
        break
    # 115 - s key - can also use ord('s')
    # save the thresholds we are using
    # to a file or whatever proves useful
    if key==115:
        blurParams = np.array([int(kBlur*fs), int(kDisk*fs), invert])
        saveThresh(lower_bounds, upper_bounds, blurParams)
        print 'saving thresholds to file'

# cleanup
#cap.release()
cv2.destroyAllWindows()


