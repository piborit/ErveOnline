import sys
import os

import LoggerFactory
import DownloadFolder
from ConfigUtils import SyncFolderConfig

if (len(sys.argv) != 3):
    print('Usage: download <category> <origin>')
    sys.exit(1)

progname = sys.argv[0]
category = sys.argv[1]
origin = sys.argv[2]

localSyncFolderConfig = SyncFolderConfig('local', category, 'in')
cloudSyncFolderConfig = SyncFolderConfig('cloud', category, origin)

logger = LoggerFactory.createLogger("download", os.path.join(localSyncFolderConfig.subfolder, "download.log"))

DownloadFolder.download(localSyncFolderConfig, cloudSyncFolderConfig)