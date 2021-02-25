#%%
%reload_ext autoreload
%autoreload 2

#%% databse
import numpy as np
from databasemanager import *

#root = 'C:\\MyFiles\\MyDatabases\\TempleSeizure'
root = 'C:\\db\\toyDB'
db = Database(root)
db.summary()

dsNames =  db.dataset_names

# set config on config.ini
# or the settings
UserSettings.global_settings().loading_data_channels = ['c4','c3','fp1']
#ds = db.load_dataset('ds_train_tcp_ar')

#% dataset
UserSettings.global_settings().loading_data_missing_channel_type = 'error'
#UserSettings.global_settings().loading_data_channels = ['fp1','fp2','f7','f8','t3','t4','t5','t6','o1','o2','c3','c4','p3','p4','f3','f4','cz']
ds0 = db.load_dataset('ds1')
ds0.summary()
#%%
ds = ds0.copy()
#ds.purify(Criteria(Subject, lambda s: ('12966' in s.name)))
#ds.foreach(Criteria(Event, lambda e: ('sz' in e.label)),lambda e: setattr(e,'label','seizure'))

ds.summary()
print(ds.unique_labels)
#%%
annotations = ds.take(Criteria(Annotation))
for ann in annotations:
    print(ann.name)
    r = ann.merge_similar_adjacent_event()
    if(r):
        print(len(r))

# %%
print(ds.merge_similar_adjacent_event())


# %%
