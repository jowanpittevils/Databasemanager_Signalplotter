#%%
#%reload_ext autoreload
#%autoreload 2

#%% databse
import numpy as np
from databasemanager import *

root = r'C:\db\toyDB'

#% dataset
UserSettings.global_settings().loading_data_missing_channel_type = 'error'
UserSettings.global_settings().loading_data_channels = ['fp1','fp2','f7','f8','t3','t4','t5','t6','o1','o2','c3','c4','p3','p4','f3','f4','cz']
ds = Database(root).load_dataset('ds1')
ds.summary()

# %%
ev_list = ds.take(Criteria(Event, lambda e: (e.duration > 1000) and (e.label == 'bckg') ))
subject_names = set([e.annotation.recording.subject.name for e in ev_list])
ds2 = ds.where((Criteria(Subject, lambda s: s.name in subject_names)))
print('total events: ', len(ev_list))
print('total subjects: ', len(subject_names))
print('new ds: ', len(ds2))



# %%
