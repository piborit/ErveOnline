import sys
import os
import time

import LoggerFactory
import DownloadFolder
from ConfigUtils import SyncFolderConfig

if (len(sys.argv) != 4):
    print('Usage: download <category> <origin> <seconds>')
    sys.exit(1)

progname = sys.argv[0]
category = sys.argv[1]
origin = sys.argv[2]
seconds = int(sys.argv[3])

localSyncFolderConfig = SyncFolderConfig('local', category, 'in')
cloudSyncFolderConfig = SyncFolderConfig('cloud', category, origin)

logger = LoggerFactory.createLogger("download", os.path.join(localSyncFolderConfig.subfolder, "download.log"))

while (True):
    start = time.time()
    DownloadFolder.download(localSyncFolderConfig, cloudSyncFolderConfig)
    stop = time.time()
    delta = stop - start
    if (delta < seconds):
        time.sleep(seconds - delta)