#!/usr/bin/env python
# -*- coding: utf_8 -*
#
# A Script to batch correct photo distortion for a GoPro Hero2 using the Lenfun database.
# Should be usable for any camera in the lensfun db.
# Alex Mandel 2014
# tech@wildintellect.com
#
# modified to use exiftool to determine camera parameters and lookup in lensfundb
# by tucker sylvia Feb 2016
#

import lensfunpy # Lensfun
import cv2 # OpenCV library
import os
from multiprocessing import Pool
import exiftool

#Test image /Pictures/gopro/farm/color/3D_R0971.JPG
def get_exif_data(photo):
    """Get embedded EXIF data from image file.
    Using exiftool.py, wrapper for perl ExifTool, gets all EXIF data including
    maker notes.
    See:
    https://github.com/smarnach/pyexiftool
    http://www.sno.phy.queensu.ca/~phil/exiftool/
    """
    try:
        with exiftool.ExifTool() as et:
            metadata = et.get_metadata(photo)
    except:
        print "Problem retreiving metadata with exiftool"

    """
    #print out all the keys:value pairs int he exif dict - debugging
    for key in sorted(metadata):
        print "%s: %s" %(key, metadata[key])
    """

    return metadata

def photolist(directory):
    '''get list of photos in the directory'''
    #TODO: support raw file sorting too instead and in addition to jpg
    extension = ".jpg"
    list_of_files = [filen for filen in os.listdir(directory) if filen.lower().endswith(extension)]
    return(list_of_files)

def process_photos(photos):
    ''' Single threaded iteration of photo list'''
    results = [correct_photo(photo) for photo in photos]
    return(results)

def multi_process(photos):
    ''' Multithreaded/Core variant that does multiple photos in parallel'''
    pool = Pool(processes=8) #2 is safe number of threads/cores, up the number if you have more
    pool.map(correct_photo, photos)
    pool.close()
    pool.join()
    return

def correct_photo(photo):
    '''Apply distortion correction'''

    #exif = get_exif_data(photo)
    #exif.get('Make')
    #exif.get('Model')

    # https://pypi.python.org/pypi/lensfunpy/0.12.0
    # Camera(Maker: NIKON CORPORATION; Model: NIKON D90; Mount: Nikon F AF; Crop Factor: 1.5; Score: 0),
    #TODO: set camera parameters from exif data and lensfun
    exif_dict = get_exif_data(photo)

    cam_maker = exif_dict['EXIF:Make'] #"NIKON CORPORATION"
    cam_model = exif_dict['EXIF:Model'] # "NIKON D90"
    #lens = "Nikkor AF-S 18-105mm f/3.5-5.6G DX ED VR"

    #Query the Lensfun db for camera parameters
    db = lensfunpy.Database()
    cam = db.find_cameras(cam_maker, cam_model)[0]
    lens = db.find_lenses(cam)[0]

    # print some info to the console
    print '|FRAME INFO|'
    #focalLength = lens.min_focal #2.5
    focalLength = exif_dict['MakerNotes:FocalLength']
    print 'Focal Length = {:6.4f} mm'.format(focalLength)
    aperture = exif_dict['EXIF:FNumber']
    print 'F Stop = {}'.format(aperture)
    distance = exif_dict['MakerNotes:FocusDistance']
    print 'Focus Distance = {:6.4f} m'.format(distance)

    im = cv2.imread(photo)
    height, width = im.shape[0], im.shape[1]

    mod = lensfunpy.Modifier(lens, cam.crop_factor, width, height)
    mod.initialize(focalLength, aperture, distance)

    undistCoords = mod.apply_geometry_distortion()
    # INTER_AREA best for Decimation, LANCZOS best for upsampling (slowest), NEAREST=fastest
    #imUndistorted = cv2.remap(im, undistCoords, None, cv2.INTER_LANCZOS4)
    imUndistorted = cv2.remap(im, undistCoords, None, cv2.INTER_NEAREST)

     #Set output filename
    fileName, fileExtension = os.path.splitext(photo)
    try:
        os.mkdir("../undistorted")
    except Exception as e:
        if os.path.isdir("../undistorted"):
            print 'undistorted folder already exists, proceeding'
            pass
        else:
            print 'something wonky when trying to create undistorted folder'
            print str(e)
            
    undistortedImagePath = "".join(["../undistorted/", fileName,"_undistorted",fileExtension])
    cv2.imwrite(undistortedImagePath, imUndistorted)

    #Change the order of colors to RGB for Pil (Pillow)
    #cvRgbImage = cv2.cvtColor(imUndistorted, cv2.COLOR_BGR2RGB)
    #pil_im = Image.fromarray(cvRgbImage)

    '''
    #update the metadata for the new files
    exif_dict = piexif.load(photo)
    #exif_dict = piexif.load(pil_im.info["exif"])

    exif_dict["0th"][piexif.ImageIFD.Model] = "HD2 U"
    exif_dict["0th"][piexif.ImageIFD.Make] = "GoPro"
    exif_dict["Exif"][piexif.ExifIFD.FocalLength] = (250,100)
    #it's actually 21.5 but exif barfs on float
    exif_dict["Exif"][piexif.ExifIFD.FocalLengthIn35mmFilm] = 21
    exif_bytes = piexif.dump(exif_dict)
    '''



    #Write the file with metadata, 100% or 95%
    #pil_im.save(undistortedImagePath, "jpeg", quality=100)#,exif=exif_bytes)

    #pil_im.save(undistortedImagePath, "jpeg", quality=95)
    #piexif.insert(exif_bytes, undistortedImagePath)




