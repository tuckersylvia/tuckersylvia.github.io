#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 16 11:49:33 2016
convenience function that plots all the
color channel histograms in HSV space
by tucker sylvia
"""

import cv2
import numpy as np
from matplotlib import pyplot as plt
import argparse
import os

def hsv_hist(img, bins=32):

    try:
        img = cv2.imread(img)
    except TypeError:
        img = img
        pass

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    h = np.ravel(hsv[:,:,0])
    s = np.ravel(hsv[:,:,1])
    v = np.ravel(hsv[:,:,2])

    plt.ion() # might be necessary for non-blocking behavior
    
    # trying to plot bars as colors for hue
    cm = plt.cm.get_cmap('hsv')
    hmax = np.max(h)
    hNorm = [float(i)/hmax for i in h]


    Y, X = np.histogram(hNorm, bins)
    xspan = X.max() - X.min()
    C = [cm(((x-X.min())/xspan)) for x in X]
    plt.figure()
    plt.bar(X[:-1],Y,color=C,width=X[1]-X[0])
    #plt.colorbar(orientation='horizontal')
    # no mappable colorbar doing it manually as above
    
    #plt.show() # put only one call to show at the end to pop up both figures at once

    # plotting individual component subplots
    plt.figure(figsize=(16,9))
    plt.subplot(131)
    plt.hist(h, bins=bins, color='r')
    plt.xlim(0,179)
    plt.title('Hue')
    plt.hold()
    plt.subplot(132)
    plt.hist(s, bins=bins, color='g')
    plt.xlim(0,255)
    plt.title('Saturation')
    plt.subplot(133)
    plt.hist(v, bins=bins, color='b')
    plt.xlim(0,255)
    plt.title('Value')
    plt.tight_layout()
    
    plt.show()
    
    raw_input('Press [enter] key to save and close plot and exit')
    figname = '../'+expname+'-'+expview+'-HSV-hist.png'
    plt.savefig(figname)
    
    return

    
#%%

if __name__ == '__main__':
    # construct the argument parser and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--image", help="Path to the image")
    args = vars(ap.parse_args())
    source = args["image"]
    
    

    cwd = os.path.abspath(source).split('/') # split path string on slash character

    # this is assuming a consistent directory structure like:
        # /media/teraid/raider/Research/Tank Experiments/Ethanol Diapirs/ED_7/top/masked/
    expname = cwd[-4] 
    expview = cwd[-3]

    print 'Generating HSV histograms for  {}-{}'.format(expname, expview)
    raw_input('Press [enter] to continue.')
    
    try:
        hsv_hist(source)
    except Exception as e:
        print 'something wonky happened in hsv_hist'
        print str(e)
        




        

