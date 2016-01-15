import os, shutil, hashlib

# MD5 of a file
fmd5 = lambda f: hashlib.md5(open(f,'rb').read()).hexdigest()

# Make safe strings
def removeNonASCII(s): 
    return "".join(i for i in s 
                   if i.isalpha() or 
                      i.isdigit() or 
                      i in ',. -_()[]{}').rstrip(' \t\r\n\0')

# Make a directory
def makeDir(newDir,newDirIsFile=True):
    if newDir[0] == os.path.sep:
        newDirBld = os.path.sep
    else:
        newDirBld = ''
    if not newDirIsFile:
        newFN = newFN+os.path.sep
    for dirPart in os.path.split(
                        os.path.abspath(
                        os.path.expanduser(newDir)))[0].split(os.path.sep):
        newDirBld = os.path.join(newDirBld,dirPart)
        if not os.path.isdir(newDirBld):
            os.mkdir(newDirBld,0750)

        
# Move file to a new name and location, creating path as needed
def fileMove(oldFN,newFN,
             copy=False,
             verbose=True,
             tagCopied='_dup',
             clobber=False):
    duplicateFile = False
    fileExt = 0
    newFNParts = os.path.splitext(newFN)
    # Check for existence of new file and add an extension 
    while os.path.isfile(newFN) and not duplicateFile:
        if fmd5(oldFN) == fmd5(newFN):
            duplicateFile = True
        else:
            newFN = ( [chr(i) for i in range(48,48+10) + \
                       range(65,65+26)][fileExt] ).join(newFNParts)
            fileExt+=1
    if not duplicateFile and not oldFN == newFN:
        if verbose>1:
            print oldFN + ' sorted'
        makeDir(newFN)
        if copy:
            shutil.copy(oldFN,newFN)
            if tagCopied:
                shutil.move(oldFN,oldFN+tagCopied)
        else:
            shutil.move(oldFN,newFN)
        os.chmod(newFN,0640)
    elif duplicateFile and not oldFN == newFN:
        if clobber:
            os.remove(oldFN)
        if verbose>1:
            print oldFN + ' is: ' + os.path.sep.join(newFN.split(os.path.sep)[-4:])

# Pass a file through without changing tree
def filePassThrough(FN,rootdir,sortdir,
                    copy=False,
                    verbose=False,
                    tagCopied='',
                    clobber=False,
                    unTagged=['..','NO_TAG']):
    # Root directory for new files
    newSort = os.path.abspath(os.path.join(sortdir,os.path.join(*unTagged)))
    # subdirectory based on filename extension
    tagDir = os.path.splitext(FN)[1][1:].upper()
    # Strip the original tag directory off the file name
    baseFN = FN.replace(os.path.join(rootdir,''),'')
    while baseFN[0:len(tagDir)+1] == tagDir + os.sep:
        baseFN = baseFN[len(tagDir)+1:]
    nFN = os.path.join(newSort,
                       tagDir,
                       baseFN)
    fileMove(FN,nFN,
             verbose=verbose,
             copy=copy,
             clobber=clobber,
             tagCopied=tagCopied)