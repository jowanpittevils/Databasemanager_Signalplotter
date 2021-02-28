
#%% databse
import numpy as np
from databasemanager import *

root = 'C:\\db\\toyDB'
db = Database(root)
db.summary()

dsNames =  db.dataset_names

#%%
# set config on config.ini
# or the settings
#UserSettings.global_settings().loading_data_channels = ['c4','c3','fp1']
#ds = db.load_dataset('ds_train_tcp_ar')

#% dataset
UserSettings.global_settings().loading_data_missing_channel_type = 'error'
UserSettings.global_settings().loading_data_channels = ['fp1','fp2','t3','t4','o1','o2','c3','c4']
ds = db.load_dataset('ds1')
ds.add_operator(Resampler(100))
ds.summary()
#%%

rec = ds.subjects[0].recordings[0]
print(rec)
# print(rec.fs_output)
# x = rec.get_data(0, 10)
# print(x.shape)

events = rec.annotations[0].events
#for e in events:
#    if(e.has_overlap_range())
print(events)

# %%
