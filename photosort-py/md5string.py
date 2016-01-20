#!/usr/bin/python

from PIL import Image

import hashlib
import fnmatch
import glob, os

#from PIL.ExifTags import TAGS
import pyexiv2

from optparse import OptionParser

# Configuration Variables
parser = OptionParser()
parser.add_option("-d", type=str, dest="BaseDir", 
                      default='.', help="Directory to search")
parser.add_option("-x", action="store_true", dest="exif", 
                  default=False, help="Show EXIF tages")
#parser.add_option("--lon", dest="lon", default=10. , type=float,
#                  help="Longitude", metavar="LONGITUDE")
(options, args) = parser.parse_args()



# Get a list of files
matches = []
for root, dirnames, filenames in os.walk(options.BaseDir):

    for filename in fnmatch.filter(filenames, '*.[jJ][pP]*[gG]' ):

        infile = os.path.join(root, filename)

        matches.append(infile)

# Cycle through the files
for infile in matches:

    im = Image.open(infile)
    md5=hashlib.md5(im.tostring()).hexdigest()
    print(md5+' : '+infile )
    
    # File renaming and extension cleaning
    file, ext = os.path.splitext(infile)
    ext = '.jpg'
    
    # EXIV data
    if options.exif:
        immd = pyexiv2.Image(infile)
        immd.readMetadata()

        print immd.exifKeys()
