#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 20 13:04:38 2016

click and drag crop roi
straight from pyimagesearch
modified to return the roi mask to be used by other scripts

@author: tucker
"""
#%% imports and function definitions
# import the necessary packages
import argparse
import cv2
import json

# initialize global variables for
# the list of reference points and 
# boolean indicating whether cropping is being performed or not
refPt = []
cropping = False

def click_and_crop(event, x, y, flags, param):
    # grab references to the global variables
    global refPt, cropping

    # if the left mouse button was clicked, record the starting
    # (x, y) coordinates and indicate that cropping is being
    # performed
    if event == cv2.EVENT_LBUTTONDOWN:
        refPt = [(x, y)]
        cv2.circle(res,(x,y), 3, (0,0,255), -1)
        cv2.imshow('image',res)
        cropping = True

    # check to see if the left mouse button was released
    elif event == cv2.EVENT_LBUTTONUP:
        # record the ending (x, y) coordinates and indicate that
        # the cropping operation is finished
        refPt.append((x, y))
        cropping = False

        # draw a rectangle around the region of interest
        cv2.rectangle(res, refPt[0], refPt[1], (0, 255, 0), 1, cv2.LINE_AA)
        cv2.imshow("image", res)

def saveCrop(pts, fname="../crop-corners.txt", fs=3.0):
    '''
    write out dict containing rectangular roi corners to file
    takes in:
        pts - list of (x,y) point tuples
        fname - sile to save crop corner points to
        fs - scale factor used to display image
            used to scale corner locations back to full image size
    '''
    # constructing a dict from the refpts list
    # crude but works because we know our list only contains
    # two (x,y) tuples
    ptdict = {'xmin':pts[0][0]*fs,
              'ymin':pts[0][1]*fs,
              'xmax':pts[1][0]*fs,
              'ymax':pts[1][1]*fs
              }
    # dump json representation of dict to a txt file - easy to load
    json.dump(ptdict, open(fname,'w'))

    print 'sucessfully dumped ptdict to crop-corners.txt'



#%% initialization and preprocessing

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", help="Path to the image")
args = vars(ap.parse_args())
source = args["image"]

# load the image, clone it, resize it so we can see the whole frame
# and setup the mouse callback function

# hackey hardcoded source file for testing
#source = "../images/D_14-top_2_undistorted.JPG"

image = cv2.imread(source)
clone = image.copy()

fs = 3.0
sf = 1.0/fs

res = cv2.resize(image, None, fx=sf, fy=sf, interpolation=cv2.INTER_AREA)
resclone = res.copy()
cv2.namedWindow("image")
cv2.setMouseCallback("image", click_and_crop)


#%% main loop
# keep looping until the 'q' key is pressed

helptext = """
            clickAndCrop.py
            
            this script is used to select and crop a ROI from a large image
            functionality is as follows:
            r key = reset cropping region
            c key = crop selected region and display it
            s key = save the cropped image ROI corner coordinates to file
            Esc or q keys = break loop and exit
            
            """

print helptext

while True:
    # display the image and wait for a keypress
    cv2.imshow("image", res)
    key = cv2.waitKey(1) & 0xFF

    # if the 'r' key is pressed, reset the cropping region
    if key == ord("r"):
        res = resclone.copy()
        
        
        
        

    # if the 'c' key is pressed, break from the loop
    elif key == ord("c"):
        # if there are two reference points, then crop the region of interest
        # from teh image and display it
        try:
            #roi = clone[refPt[0][1]:refPt[1][1], refPt[0][0]:refPt[1][0]]
            roi = clone[refPt[0][1]*fs:refPt[1][1]*fs, refPt[0][0]*fs:refPt[1][0]*fs]
            cv2.imshow("ROI", roi)
        except:
            print "must create roi before cropping"


    # save the cropped image and coordinates to a file
    elif key == ord("s"):
        #savename = source[:-4]+'_cropped.jpg'
        #cv2.imwrite(savename, roi)
        print 'saving cropped region corners to file'
        saveCrop(refPt)

    # break loop and exit
    elif key == 27 or key == ord("q"): # 27 = Esc key
        break


#%% post and cleanup

# close all open windows
cv2.destroyAllWindows()


