import os
import os.path
import sys
import shutil
import logging
from datetime import datetime
import LoggerFactory

def timestamp():
    dateTimeObj = datetime.now()
    timestampStr = dateTimeObj.strftime("%d-%m-%Y_%H-%M-%S-%f")
    return timestampStr

def moveToFolder(filename, fromfolder, tofolder):
    try:
        if not os.path.isdir(tofolder):
            os.mkdir(tofolder)
        shutil.move(os.path.join(fromfolder, filename), os.path.join(tofolder, filename))
    except:
        LoggerFactory.getLogger().error(sys.exc_info())

def copyToFolder(filename, fromfolder, tofolder):
    try:
        if not os.path.isdir(tofolder):
            os.mkdir(tofolder)
        shutil.copy(os.path.join(fromfolder, filename), os.path.join(tofolder, filename))
    except:
        LoggerFactory.getLogger().error(sys.exc_info())
