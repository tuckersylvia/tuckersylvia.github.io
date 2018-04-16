#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 14 13:14:12 2016

@author: tucker
"""

import numpy as np
import cv2
import json
import os
import time
from multiprocessing import Pool


def getThresholds(fname='../saved-thresholds.txt'):
    '''
    loads two points from text file containing
    upper right and lower left corners and
    returns 4 values: xmin, xmax, ymin, and ymax
    '''
    threshdict = json.load(open(fname))

    return threshdict

def photolist(directory):
    '''get list of photos in the directory'''
    #TODO: support raw file sorting too instead and in addition to jpg
    extension = ".jpg"
    list_of_files = [filen for filen in os.listdir(directory) if filen.lower().endswith(extension)]
    return(list_of_files)

def process_photos(photos):
    ''' Single threaded iteration of photo list'''
    results = [thresh_photo(photo) for photo in photos]
    return(results)

def multi_process(photos):
    ''' Multithreaded/Core variant that does multiple photos in parallel'''
    pool = Pool(processes=8) #2 is safe number of threads/cores, up the number if you have more
    pool.map(thresh_photo, photos)
    pool.close()
    pool.join()
    return

def thresh_photo(photo):
    '''threshold in hsv space a photo'''
    global threshdict

    # read frame
    frame = cv2.imread(photo)
    #blur frame
    kBlur = threshdict['blur']
    frame = cv2.medianBlur(frame, kBlur)
    # convert colorspace
    hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)

     # Normal masking algorithm
    lower_bounds = np.array([threshdict['hmin'],
                             threshdict['smin'],
                             threshdict['vmin']
                             ])

    upper_bounds = np.array([threshdict['hmax'],
                             threshdict['smax'],
                             threshdict['vmax']
                             ])



    # do some morphological operations to clean up the mask
    mask = cv2.inRange(hsv, lower_bounds, upper_bounds)

    #mask = cv2.erode(mask, disk, iterations=2)
    #mask = cv2.dilate(mask, disk, iterations=2)
    # checking if cv2.MORPH_OPEN gives different / better results than
    # the explicit erode then dilate (definition of open = erode then dilate)
    kDisk = threshdict['disk']
    disk = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (kDisk,kDisk))
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, disk)
    #mask = cv2.bitwise_not(mask,mask)

    # added inversion functionality to hsvthreshInteract
    # need to be able to load it here and do that inversion if desired...
    if 'invert' in threshdict.keys():
        invert = threshdict['invert']
        if invert ==1:
            mask = cv2.bitwise_not(mask, mask)

    #show result
    result = cv2.bitwise_and(frame, frame, mask=mask)
    
    

     #Set output filename
    fileName, fileExtension = os.path.splitext(photo)
 
    try:
        os.mkdir("../masked")
    except Exception as e:
        if os.path.isdir("../masked"):
            print 'masked folder already exists, proceeding'
            pass
        else:
            print 'something wonky when trying to create masked folder'
            print str(e)
            
    ########
    # this one is for the fully masked results you want
    maskImagePath = "".join(["../masked/", fileName,"_masked",fileExtension])
    cv2.imwrite(maskImagePath, result)
    
    '''
    
    ############
    # REMINDER
    #
    # below has been modified to save half masked images
    # you did this quickly to make a movie for AGU talk 2016
    # don't forget to change it back to as above in order
    # to save fully masked images which are the ones that 
    # are actually used in processing
    #
    # END of pitiful attempt to save yourself from future aggrivation
    ############
    
    
    # blended / weighted to show backround through mask a little
    alpha = 0.5
    halfmask = cv2.addWeighted(frame, alpha, result, (1-alpha), 0, frame)
    
    ########
    # this one is tha half masked version for making a movie
    #maskImagePath = "".join(["../halfmask/", fileName,"_masked",fileExtension])
    #cv2.imwrite(maskImagePath, halfmask)
   
    '''


#%%
if __name__ == '__main__':

    directory = os.getcwd()
    print 'current working directory: {}'.format(directory)
    
    try:
        os.chdir(directory)
        photos = photolist(directory)
        threshdict = getThresholds()

        tic = time.time()

        #result = process_photos(photos)
        multi_process(photos)

        toc = time.time()
        totaltime = toc-tic

        nframes = len(photos)
        fps = nframes/totaltime

        print '###========== COMPLETE ==========###'
        print 'Processed {:d} frames in {:6.3f} seconds, {:6.3f} fps'.format(nframes,
                 totaltime, fps)

    except Exception as e:
        print(" ".join(["Something failed because of",str(e)]))