#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
mask-track.py

this script takes a sequence of preprocessed images and finds binary
blobs, then tracks those blobs throughout the sequence. finally it
saves the resulting trajectory and accesory data to a file.

Created on Tue Oct 18 17:56:55 2016

@author: tucker
Released as free and open sources software under the
GNU GPL v3 licence

"""

import os
import time
import argparse

#import numpy as np
import pandas as pd

import matplotlib as mpl
import matplotlib.pyplot as plt

#import skimage as ski
from skimage.measure import regionprops, label
from skimage.filters import threshold_otsu
import trackpy as tp
import pims

# plotting config
mpl.rc('figure', figsize=(16,9))
mpl.rc('image', cmap='gray')
plt.style.use('ggplot')
plt.ion()

# first read in some command line arguments
# can provide absolute path, path relative to cwd, or use cwd by default
# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()

ap.add_argument("-d", "--display", type=int, default=1,
                help="Whether or not frames should be displayed")
ap.add_argument("-p", "--path", type=str, default='./*.jpg',
                help="path to the images, default *.jpg in cwd")
ap.add_argument("-b", "--debug", type=int, default=0,
                help="toggle for some debugging diagnostic plots")

args = vars(ap.parse_args())

DEBUGGING = args['debug']
#DEBUGGING = 1

filepath = args['path']

cwd = os.path.abspath(filepath).split('/') # split path string on slash character

# this is assuming a consistent directory structure like:
# /media/teraid/raider/Research/Tank Experiments/Ethanol Diapirs/ED_7/top/masked/
expname = cwd[-4] 
expview = cwd[-3]

print 'Tracking {}-{}'.format(expname, expview)
raw_input('Press [enter] to continue.')

# or just hard code it for now
#filepath = '/home/tucker/python/images/trackpy-test/mask/*.jpg'
# apparently implicit string concatenation occurs within parentheses
#filepath = ('/media/teraid/raider/Research/Tank Experiments/'
#            'Ethanol Diapirs/ED_6/side/masked/*.jpg'
#            )

#load frames from disk into python image sequence 
# container as single channel gray

######
# 4-19-2017
# wrapped this part in a try except thing because it was complaining about not matching
# the ./*.jpg glob because some of the directories hav the photos as .JPG instead
#####
try:
    frames = pims.ImageSequence(filepath, as_grey=True)
except IOError:
    print "no files matched glob *.jpg, trying *.JPG instead..."
    filepath = './*.JPG'
    frames = pims.ImageSequence(filepath, as_grey=True)

### end stupid hack

features = pd.DataFrame() # initialize empty dataframe
#%%
# loop through frames
# display some number of frames
nplots = len(frames)/10 # get /n frames

t0 = time.time() # start a timer

#plt.figure() # try to paint on a single figure

for num, img in enumerate(frames):
    
    # quick binarization
    binimg = img.copy() # make a copy of the frame to alter
    try:
        thresh = threshold_otsu(binimg)# get optimal threshold from otsus method
    except:
        print 'blank image at frame number {}'.format(num)
        continue # move along to the next one

    binimg[binimg>thresh] = 255 # set foreground blobs hi
    binimg[binimg<thresh] = 0 # set background lo
    labeled = label(binimg, connectivity=2) # 2 connectivity includes diagonals

    
    # loop over the labeled regions
    for region in regionprops(labeled, intensity_image=binimg):
        # might want actual img as intensity img above...
        # eliminate small features
        # max area = 1200 --> max r = ~20 pixels, way smaller than our blobs
        if region.convex_area < 800: # eliminate small features
            continue # move along to next loop iteration
        # also eliminate really large areas if we cant mask them out 
        #(ie the polybelt.com writing on the belts in some frames)
        elif region.convex_area > 30000:
            continue
        # add worthwihile features and some params
        features = features.append([{'frame': num,
                                     'x': region.centroid[1],# x=column
                                     'y': region.centroid[0],# y=row
                                     'area': region.area,
                                     'convarea': region.convex_area,
                                     'maj': region.major_axis_length,
                                     'min': region.minor_axis_length,
                                     'angle': region.orientation,
                                     'bbox': region.bbox,
                                     'thresh': thresh
                                     }])

     # end inner loop
    if num%20==0 and DEBUGGING==1:
        plt.imshow(binimg)
        #plt.scatter(region.centroid[1],region.centroid[0])
        titlestr = 'Frame # {}'.format(num)
        plt.title(titlestr)
        tp.annotate(features[features.frame==num], frames[num])
        raw_input('Press [enter] to close annotated image plot and continue.')
        plt.close()
    ''' 
    # display code
    # not working in the loop, plots stay blank
    if args['display']==1 and num%nplots==0:
            plt.figure()
            #plt.gcf()
            plt.imshow(img)
            plt.scatter(region.centroid[1],region.centroid[0])
            #titlestr = 'Frame # {}'.format(num)
            #plt.title(titlestr)
            print 'plotting a frame'
            tp.annotate(features[features.frame==num], frames[num])
            
            '''
# end outer loop

t1 = time.time()
tt = t1-t0
print 'Total feature location time: {:.2f} seconds'.format(tt)
raw_input('Press [enter] to continue to linking.')

#%%
# linking and removing short tracks

searchrange = 100 # tweak this - max pixel distance a blob can travel between frames
tracks = tp.link_df(features, searchrange, memory=9) # memory is for occlusion

# and save it to file
tracks.to_csv('../alltracks.csv')

# define a little function to get the particle frame counts
def getFrameCount(tracks):
    partcounts = []
    for i in range(len(tracks.particle.unique())):
        partcounts.append((i, tracks[tracks.particle==i].shape[0]))
        
    return partcounts

partcount = getFrameCount(tracks)
print 'Particle frame counts'
print partcount

goodtracks = pd.DataFrame()
for particle in range(len(tracks.particle.unique())):
    # if the particle is present for more than nframes keep it
    nframes = 15
    if tracks[tracks.particle==particle].shape[0]>nframes:
        goodtracks = goodtracks.append(tracks[tracks.particle==particle])

# save that biatch to file now that we have it...
goodtracks.to_csv('../goodtracks.csv')

#%%
# plotting up some results
# and look at the good tracks   
plt.ion()
 #plt.show()
# put it in a function so it doesn't block when run from terminal     

def compPlot():
    '''
    quick convenience function to pop up a plot after script runs
    '''    
   
    
    #plt.figure()
    #tp.plot_traj(goodtracks, label=True, superimpose=frames[254]*-1)
    plt.subplot(121)
    tp.plot_traj(tracks, label=True)
   #plt.draw()
    #plt.pause(0.001)
    plt.title('All tracks')
    plt.legend(loc='lower left')

    plt.subplot(122)
    #tp.plot_traj(tracks, label=True, superimpose=frames[254]*-1)
    tp.plot_traj(goodtracks, label=True)
    #plt.draw()
    #plt.pause(0.001)
    plt.title('Good tracks')
    plt.legend(loc='lower left')
    
    raw_input('Press [enter] key to save and close plot and exit')
    figname = '../'+expname+'-'+expview+'-tracks.png'
    plt.savefig(figname)
    
    return
    
compPlot()
#plt.show()
'''
plt.figure()
#tp.plot_traj(goodtracks, label=True, superimpose=frames[254]*-1)
plt.subplot(121)
tp.plot_traj(goodtracks, label=True)
plt.title('Good tracks')
plt.legend(loc='lower left')

plt.subplot(122)
#tp.plot_traj(tracks, label=True, superimpose=frames[254]*-1)
tp.plot_traj(tracks, label=True)
plt.title('All tracked blobs')
plt.legend(loc='lower left')
'''

#testframenum = 5 # pick a random test shot

#plt.figure()

#tp.annotate(features[features.frame==testframenum], frames[testframenum])

#plt.figure()
#plt.imshow(frames[testframenum])

# lets take a look at all trajectories
#plt.figure()
#plt.gca().invert_yaxis()

#plt.figure()
#minr, minc, maxr, maxc = region.bbox
#plt.Rectangle()



        
        
        
        
        
        