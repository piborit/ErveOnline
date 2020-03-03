import os
import os.path
import logging
import sys

import LoggerFactory
import Utils

from ConfigUtils import CloudConfig
from pcloud import PyCloud

def upload(localSyncFolderConfig, cloudSyncFolderConfig):
    cloudConfig = CloudConfig()

    try:
        pyCloud = PyCloud(cloudConfig.username, cloudConfig.password)

        pyCloud.createfolderifnotexists(path=cloudSyncFolderConfig.folder)
        pyCloud.createfolderifnotexists(path=cloudSyncFolderConfig.tmpfolder)

        for filename in os.listdir(localSyncFolderConfig.folder):
            LoggerFactory.getLogger().info("filename=" + filename + "," + "from=" + localSyncFolderConfig.folder)
            LoggerFactory.getLogger().info("-> upload to=" + cloudSyncFolderConfig.folder);
            pyCloud.uploadfile(files=[os.path.join(localSyncFolderConfig.folder, filename)], path=cloudSyncFolderConfig.tmpfolder, progresshash='0')
            LoggerFactory.getLogger().info("-> move to=" + localSyncFolderConfig.backupfolder);
            Utils.moveToFolder(filename, localSyncFolderConfig.folder, localSyncFolderConfig.backupfolder)
            LoggerFactory.getLogger().info("-> rename from=" + cloudSyncFolderConfig.tmpfolder + "," + "to=" + cloudSyncFolderConfig.folder);
            pyCloud.renamefile(path=cloudSyncFolderConfig.tmpfolder + '/' + filename, topath=cloudSyncFolderConfig.folder + '/', filename=filename);
    except:
        LoggerFactory.getLogger().error(sys.exc_info())
