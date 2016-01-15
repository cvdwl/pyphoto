from PIL.ExifTags import TAGS
from PIL import Image
import os, re
from datetime import datetime


# Make safe strings
def removeNonASCII(s): 
    return "".join(i for i in s 
                   if i.isalpha() or 
                      i.isdigit() or 
                      i in ',. -_()[]{}').rstrip(' \t\r\n\0')

# Read all the EXIF tags
def get_exif(fn):
    DTkeys = ['DateTimeOriginal','DateTimeDigitized','DateTime']
    ret = {}
    m = ''
    t = []
    i = Image.open(fn)
    info = i._getexif()
    if info:
        for tag, value in info.items():
            decoded = TAGS.get(tag, tag)
            ret[decoded] = value
            if decoded == 'Model':
                m = removeNonASCII(value).rstrip(',')
        tk = [k for k in DTkeys if k in ret.keys()]
        while tk and not t:
            try:
                t = datetime.strptime(ret[tk[0]].rstrip(' \t\r\n\0'),
                                      '%Y:%m:%d %H:%M:%S')
            except:
                tk=tk[1:]
    return ret,t,m

# Generate a file name based on the EXIF timestamp, etc.
def getEXIFFileName(FN,sortdir='.',ownerTAG='_CVL'):
    try:
        exifTags,t,m = get_exif(FN)
        if not t or not m:
            return ''
        else:
            return os.path.join(sortdir,
                                m,
                                t.strftime('%Y/%m/%y%m%d-%H%M%S' + 
                                           ownerTAG+'.jpg'))
    except:
        return ''
