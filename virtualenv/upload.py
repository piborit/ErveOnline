import sys
import os
import os.path

import LoggerFactory
import UploadFolder
from ConfigUtils import SyncFolderConfig

import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class EventHandler(FileSystemEventHandler):
    def on_any_event(self, event):
        UploadFolder.upload(localSyncFolderConfig, cloudSyncFolderConfig)

if (len(sys.argv) != 3):
    print('Usage: upload <category> <origin>')
    sys.exit(1)

progname = sys.argv[0]
category = sys.argv[1]
origin = sys.argv[2]

localSyncFolderConfig = SyncFolderConfig('local', category, 'out')
cloudSyncFolderConfig = SyncFolderConfig('cloud', category, origin)

logger = LoggerFactory.createLogger("upload", os.path.join(localSyncFolderConfig.subfolder, "upload.log"))

if __name__ == "__main__":
    path = localSyncFolderConfig.folder
    event_handler = EventHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()