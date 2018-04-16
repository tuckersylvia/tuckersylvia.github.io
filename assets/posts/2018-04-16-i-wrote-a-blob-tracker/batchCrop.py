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


def getCorners(fname='../crop-corners.txt'):
    '''
    loads two points from text file containing
    upper right and lower left corners and
    returns 4 values: xmin, xmax, ymin, and ymax
    '''
    ptsdict = json.load(open(fname))

    return ptsdict

def photolist(directory):
    '''get list of photos in the directory'''
    #TODO: support raw file sorting too instead and in addition to jpg
    extension = ".jpg"
    list_of_files = [filen for filen in os.listdir(directory) if filen.lower().endswith(extension)]
    return(list_of_files)

def process_photos(photos):
    ''' Single threaded iteration of photo list'''
    results = [crop_photo(photo) for photo in photos]
    return(results)

def multi_process(photos):
    ''' Multithreaded/Core variant that does multiple photos in parallel'''
    pool = Pool(processes=8) #2 is safe number of threads/cores, up the number if you have more
    pool.map(crop_photo, photos)
    pool.close()
    pool.join()
    return

def crop_photo(photo):
    '''crop a photo'''
    global ptsdict

    im = cv2.imread(photo)

    imCropped = im[ptsdict['ymin']:ptsdict['ymax'],
                   ptsdict['xmin']:ptsdict['xmax'], :]

     #Set output filename
    fileName, fileExtension = os.path.splitext(photo)
    try:
        os.mkdir("../cropped")
    except Exception as e:
        if os.path.isdir("../cropped"):
            print 'cropped folder already exists, proceeding'
            pass
        else:
            print 'something wonky when trying to create cropped folder'
            print str(e)

    croppedImagePath = "".join(["../cropped/", fileName,"_cropped",fileExtension])
    cv2.imwrite(croppedImagePath, imCropped)



if __name__ == '__main__':

    directory = os.getcwd()
    print 'current working directory: {}'.format(directory)
    
    try:
        os.chdir(directory)
        photos = photolist(directory)
        ptsdict = getCorners()

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
        
        
        
        