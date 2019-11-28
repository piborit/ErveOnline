import sys
import os
import time
import getopt

import LoggerFactory
import DownloadFolder
import ConfigUtils
from ConfigUtils import SyncFolderConfig


progname = sys.argv[0]
configfile = 'config.toml'
category = ''
origin = ''
seconds = 60
backup = False
try:
    opts, args = getopt.getopt(sys.argv[1:], "hbc:o:s:f:", ["category=", "origin=", "seconds=", "config="])
except getopt.GetoptError:
    print('Usage: ' + os.path.basename(argv[0]) + ' -c <category> -o <origin> -s <seconds> -f <configfile> -b')
    sys.exit(2)
for opt, arg in opts:
    if opt == '-h':
        print(os.path.basename(argv[0]) + ' -c <category -o <origin> -s <seconds> -f <configfile> -b')
        sys.exit()
    elif opt == '-b':
        backup = True
    elif opt in ("-c", "--category"):
        category = arg
    elif opt in ("-o", "--origin"):
        origin = arg
    elif opt in ("-s", "--seconds"):
        seconds = int(arg)
    elif opt in ("-f", "--config"):
        configfile = arg

ConfigUtils.init(configfile)
localSyncFolderConfig = SyncFolderConfig('local', category, 'in')
cloudSyncFolderConfig = SyncFolderConfig('cloud', category, origin)

logger = LoggerFactory.createLogger("download", os.path.join(localSyncFolderConfig.subfolder, "download.log"))

while (True):
    start = time.time()
    DownloadFolder.download(localSyncFolderConfig, cloudSyncFolderConfig, backup)
    stop = time.time()
    delta = stop - start
    if (delta < seconds):
        time.sleep(seconds - delta)
