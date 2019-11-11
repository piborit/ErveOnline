import toml
import os
import os.path
import Utils

class SyncFolderConfig:
    def __init__(self, type, category, origin):
        if (type == 'local'):
            self.basepath = getValue(type, 'basepath')
            self.subfolder = os.path.join(self.basepath, getValue(type, category))
            self.folder = os.path.join(self.subfolder, getValue(type, origin))
            self.tmpfolder = os.path.join(self.subfolder, getValue(type, 'tmp'))
            self.backupfolder = os.path.join(self.subfolder, getValue(type, 'backup'), Utils.timestamp())

        if (type == 'cloud'):
            self.basepath = getValue(type, 'basepath')
            self.subfolder = self.basepath + "/" + getValue(type, category)
            self.folder = self.subfolder + "/" + getValue(type, origin)
            self.tmpfolder = self.subfolder + "/" + getValue(type, 'tmp')

class CloudConfig:
    def __init__(self):
        self.username = getValue('cloud', 'username')
        self.password = getValue('cloud', 'password')

def getValue(category, property):
    try:
      return config[category][property]
    except:
        return property

config=toml.load('config.toml')
