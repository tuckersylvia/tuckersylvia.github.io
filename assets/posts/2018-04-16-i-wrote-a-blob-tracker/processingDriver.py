#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
processing-driver.py

this script ties together all of the other processing scripts in
a linear stepwise fashion to facilitate processing of an entire experiment
mo' rapidly.

makes calls scripts in ~/python/scripts/pipeline
to complete the following processing steps:
    remove lens distortion
    crop to roi in batch
    threshold out diapirs in hsv space
    track diapirs around
    plotting and saving preliminary data
    then on to the notebook environment for better interactivity
    
listing out the steps of our algorithm / processing pipeline so we can try to 
automate as much as possible and preserve the user interaction and persistence
written into our scripts.

directory structure assumed to be something like:    
    .../Research/Tank Experiments/EXPTYPE/EXPNUM/VIEW/stuffwewant/...

first within an experimetnt here are top and side containing original images

start in view folder
change to original folder
run batchLensCorrector.py - this creates ../undistorted
cd to ../undistorted
run clickAndCrop.py - this saves ROI to ../crop-corners.txt
run batchCrop.py - this creates ../cropped folder using ROI
cd ../cropped

# HARDEST PART #
run hsvHist.py on a reprasentative image to get a feel for what the 
    color channel distributions look like, helps find good values for next step
run hsvThreshInteract.py - this saves thresholds to ../saved-thresholds.txt
    -do this a few times on reprasentative images from beginning, middle, and 
    end of experiment. getting good threshold values for various lighting 
    changes etc. can be tricky, might have to have separate thresholds for 
    different parts of the experiment if you cant find single set of good values
    
run batch-thresh.py - this creates ../masked folder using saved thresholds
cd ../masked
run maskTrack.py - this saves alltracks.csv, goodtracks.csv, and 
    EXPNUM-VIEW-tracks.png to VIEW directory

### end image processing ### 

FOR SIDE VIEWS:
    now open the EXPNUM-VIEW-temptracks.ipynb notebook
and load the proper thermal field, and determine scaling factors and offsets
to get the tracks onto the thermal field etc. also maybe save some exp info like
max displacements, deflections, times, lengths, etc

for top views

maybe try importing each script as a module and running the pieces we need.

Created on Mon Jan  9 13:44:55 2017

@author: tucker

Released as free and open source software under the GNU-GPLv3

"""

# imports
import os
import subprocess


# function definitions
def getGoodFileName():
    '''
    wrapper function to provide consistent interface for getting a good 
    filename from the user. also prints a handy directory listing
    call signature:
        getGoodFileName()
        
    '''
    # adding tab complete to the getgoodFileName function...
    import readline
    readline.parse_and_bind("tab: complete") 

    # print a directory listing so we can choose a file that is here
    print os.getcwd()
    subprocess.call(['ls', '-la'], shell=True) # may or may not need shell arg
    
    while(True):
        filename = raw_input('Please enter a valid file name:')
        # if it is not a file ask again
        if not os.path.isfile(filename):
            print 'Please enter a new, VALID file name... \n'
            continue
        else: # otherwise move along
            goodname = filename
            break 
    
    return goodname

def tryCall(command, shell=False):
    '''
    wrapper function to call command with subprocess.call in a 
    try/except statement for consistent behavior
    arguments:
        command - string or list of strings to construct command
            - needs to be a list if there are any arguments passed
            shell - whether to execute in a new shell, defaults to True
    call signature:
        tryCall(command, [shell=True...])
        
    '''
     
    try:
        subprocess.call(command, shell=shell)
        #print '{} successfully returned with exit code 0 \n'.format(command)
               
    except Exception as e:
        print 'something wonky happened in driver script: \n'
        print 'while working in: {}'.format(os.getcwd())
        print 'command string passed to call: {}'.format(cmd)
        print str(e)
        
    return
        
# before i start... should I wrap all this in a main function... probably
if __name__ == '__main__':

    # start in view folder
    print 'Currently working in: {} \n'.format(os.getcwd())
    
    # change to originals folder
    os.chdir('./original')
    print 'Changed to original directory \n'
    
    # run lens-corrector-batch.py
    print 'Running batchLensCorrector.py \n'
    cmd = 'batchLensCorrector.py'
    tryCall(cmd)
        
    # change to ../undistorted
    os.chdir('../undistorted')
    print 'Changed to undistorted directory \n'
    # get a valid file name for cropping ROI
    filename = getGoodFileName()
    # commands with args must be passed as a list
    cmd = ['clickAndCrop.py', '-i', filename]    
    tryCall(cmd)
        
    # now run batch-crop.py on all images with selcted ROI In THIs DIRECTORY
    cmd = 'batchCrop.py'
    tryCall(cmd)
    
    # change to ../cropped
    os.chdir('../cropped')
    print 'Changed to cropped directory \n'
    # get a valid file name for histogramming
    filename = getGoodFileName()
    # commands with args must be passed as a list
    cmd = ['hsvHist.py', '-i', filename]    
    tryCall(cmd)
    
    # now fun hsv_thresh_interact on the same image so we can use the distributions
    # to estimate filter parameters
    cmd = ['hsvThreshInteract.py', '-i', str(filename)]
    tryCall(cmd)

    # now run batch-thresh.py to threshold all images and send them to ../masked
    cmd = 'batchThreshold.py'
    tryCall(cmd)
    
    # change to ../masked
    os.chdir('../masked')
    print 'Changed to masked directory \n'
    
    # run mask-track.py
    cmd = 'maskTrack.py'
    tryCall(cmd)
    
    # END IMAGE PROCESSING
    # NOw NOTEBOOK STUFF






