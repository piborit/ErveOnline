import toml
import os
import os.path
import Utils

class SyncFolderConfig:
    def __init__(self, location, category, origin):
        if (location == 'local'):
            self.basepath = getValue(location, 'basepath')
            self.subfolder = os.path.join(self.basepath, getValue(location, category))
            self.folder = os.path.join(self.subfolder, getValue(location, origin))
            self.tmpfolder = os.path.join(self.subfolder, getValue(location, 'tmp'))
            self.backupfolder = os.path.join(self.subfolder, getValue(location, 'backup'))

        if (location == 'cloud'):
            self.basepath = getValue(location, 'basepath')
            self.subfolder = self.basepath + "/" + getValue(location, category)
            self.folder = self.subfolder + "/" + getValue(location, origin)
            self.tmpfolder = self.subfolder + "/" + getValue(location, 'tmp')

class CloudConfig:
    def __init__(self):
        self.username = getValue('cloud', 'username')
        self.password = getValue('cloud', 'password')

config = dict()

def init(configfile):
    config.update(toml.load(configfile))

def getValue(category, property):
    try:
        return config[category][property]
    except:
        return property
