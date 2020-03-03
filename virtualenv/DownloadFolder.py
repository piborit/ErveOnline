import os
import os.path
import logging
import sys
import urllib

from ConfigUtils import SyncFolderConfig
from ConfigUtils import CloudConfig

from pcloud import PyCloud
import LoggerFactory
import Utils


def download(localSyncFolderConfig, cloudSyncFolderConfig, backup):
    cloudConfig = CloudConfig()

    try:
        pyCloud = PyCloud(cloudConfig.username, cloudConfig.password)

        folderinfo = pyCloud.createfolderifnotexists(path=cloudSyncFolderConfig.folder)
        listFolderinfo = pyCloud.listfolder(path=cloudSyncFolderConfig.folder)

        metadata = listFolderinfo["metadata"]
        contents = metadata["contents"]
        backupfolder = os.path.join(localSyncFolderConfig.backupfolder, Utils.timestamp())
        for file in contents:
            if (not file["isfolder"]):
                filename = file["name"]
                LoggerFactory.getLogger().info("filename=" + filename + "," + "from=" + cloudSyncFolderConfig.folder)
                filelink = pyCloud.getfilelink(path=cloudSyncFolderConfig.folder + "/" + filename)
                downloadlink = 'https://' + filelink["hosts"][0] + filelink["path"]
                LoggerFactory.getLogger().info("-> download to=" + localSyncFolderConfig.tmpfolder);
                urllib.request.urlretrieve(downloadlink, os.path.join(localSyncFolderConfig.tmpfolder, filename));
                if backup:
                    LoggerFactory.getLogger().info(
                        "-> backup from=" + localSyncFolderConfig.tmpfolder + "," + "to=" + backupfolder)
                    Utils.copyToFolder(filename, localSyncFolderConfig.tmpfolder, backupfolder)
                LoggerFactory.getLogger().info(
                    "-> rename from=" + localSyncFolderConfig.tmpfolder + "," + "to=" + localSyncFolderConfig.folder)
                os.rename(os.path.join(localSyncFolderConfig.tmpfolder, filename),
                          os.path.join(localSyncFolderConfig.folder, filename))
                LoggerFactory.getLogger().info(
                    "-> delete from=" + cloudSyncFolderConfig.folder)
                pyCloud.deletefile(path=cloudSyncFolderConfig.folder + "/" + filename)
    except:
        LoggerFactory.getLogger().error(sys.exc_info())
