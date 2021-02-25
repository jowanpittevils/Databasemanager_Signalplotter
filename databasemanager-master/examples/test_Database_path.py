
#%%
from databasemanager import *
from databasemanager.classes.path import Path

# %% load with string
root = r'C:\db\toyDB'
db = Database(root=root)
db.summary()


# %% load with Path object
root = r'C:\db\toyDB'
path = Path(root)
db = Database(path)
db.summary()

# %% load with customize Path object
class newPath(Path):
    @classmethod
    def get_datasetsfolder_fullpath(cls, root):
        return 'C:\\MyFiles\\MyDatabases\\Sleep\\__Datasets'# join(root,cls.DATASETSFOLDER)

UserSettings.global_settings().loading_data_missing_channel_type = 'error'
UserSettings.global_settings().loading_data_channels = ['fp1','fp2']
root = r'C:\db\toyDB'
path = newPath(root)
db = Database(path)
db.summary()
db = Database(path)
db.load_dataset('ds1').summary()
print(path.datasetsfolder_fullpath)

# %%
root = r'C:\db\toyDB'
db = Database(None, data_path=root+'/Data', datasets_path=root+'/Datasets')
db.summary()
db.load_dataset('debug').summary()


# %%
