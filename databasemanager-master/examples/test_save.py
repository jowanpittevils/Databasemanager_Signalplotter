#%%
from databasemanager import *
from databasemanager.operators.resampler import Resampler

UserSettings.global_settings().loading_data_channels = ['c3','c4']
root = 'C:\\MyFiles\\MyDatabases\\Sleep'
db = Database(root)
ds = db.load_dataset('test')
ds.add_operator(Resampler(10))
ds.summary()

ds.load_offline()
len(ds.offline_data)

#%%
ds.save_to_file(save_offline_data=True)

# %%
from databasemanager import *
ds2 = Dataset.load_from_file()
ds2.summary()
len(ds2.offline_data)
# %%
