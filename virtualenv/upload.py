import sys
import getopt
import os
import os.path

import LoggerFactory
import UploadFolder
import ConfigUtils
from ConfigUtils import SyncFolderConfig

import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class EventHandler(FileSystemEventHandler):
    def on_any_event(self, event):
        UploadFolder.upload(localSyncFolderConfig, cloudSyncFolderConfig)

progname = os.path.basename(sys.argv[0])
configfile = 'config.toml'
category = ''
origin = ''
try:
    opts, args = getopt.getopt(sys.argv[1:], "hc:o:s:f:", ["category=", "origin=", "config="])
except getopt.GetoptError:
    print('Usage: ' + progname + ' -c <category> -o <origin> -f <configfile>')
    sys.exit(2)
for opt, arg in opts:
    if opt == '-h':
        print(progname + ' -c <category -o <origin> -f <configfile>')
        sys.exit()
    elif opt in ("-c", "--category"):
        category = arg
    elif opt in ("-o", "--origin"):
        origin = arg
    elif opt in ("-f", "--config"):
        configfile = arg

ConfigUtils.init(configfile)

localSyncFolderConfig = SyncFolderConfig('local', category, 'out')
cloudSyncFolderConfig = SyncFolderConfig('cloud', category, origin)

logger = LoggerFactory.createLogger("upload", os.path.join(localSyncFolderConfig.subfolder, "upload.log"))

if __name__ == "__main__":
    path = localSyncFolderConfig.folder
    event_handler = EventHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    UploadFolder.upload(localSyncFolderConfig, cloudSyncFolderConfig)
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()