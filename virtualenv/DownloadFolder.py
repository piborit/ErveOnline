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
                LoggerFactory.getLogger().info("from=" + cloudSyncFolderConfig.folder + "," + "filename=" + filename + "," + "to=" + localSyncFolderConfig.folder)
                filelink = pyCloud.getfilelink(path=cloudSyncFolderConfig.folder+"/"+filename)
                downloadlink = 'https://' + filelink["hosts"][0] +  filelink["path"]
                urllib.request.urlretrieve(downloadlink, os.path.join(localSyncFolderConfig.tmpfolder, filename));
                if backup: Utils.copyToFolder(filename, localSyncFolderConfig.tmpfolder, backupfolder)
                os.rename(os.path.join(localSyncFolderConfig.tmpfolder, filename), os.path.join(localSyncFolderConfig.folder, filename))
                pyCloud.deletefile(path=cloudSyncFolderConfig.folder+"/"+filename)
    except:
        LoggerFactory.getLogger().error(sys.exc_info())