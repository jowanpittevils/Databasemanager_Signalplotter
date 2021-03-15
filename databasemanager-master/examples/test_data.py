#%%
import numpy as np
from databasemanager import *

UserSettings.global_settings().loading_data_channels = ['c3','c4']

root = r'C:\db\toyDB'
db = Database(root)
db.summary()
#%%
ds_tr = db.load_dataset('ds1')
ds_ts = db.load_dataset('ds2')
ds_tr.summary()
ds_ts.summary()

(ds_tr + ds_ts).summary()
(ds_tr - ds_ts).summary()


# %%
import mne
custom_mapping = {'LVI':0, 'ASI':1, 'HVS':2, 'TA':3}
raw = ds.fetch_mne_list(True)
(rem_events, rem_event_dict) = mne.events_from_annotations(
                                                raw[0], 
                                                chunk_duration=30,
                                                event_id=custom_mapping,)
rem_events.shape
raw[0].plot()

# %%
d = raw[0].get_data([0,1],0, int(30*ds.subjects[0].recordings[0].fs))
d.shape

#%%
from databasemanager import *
root = 'C:\\MyFiles\\MyDatabases\\Sleep'
UserSettings.instance().loading_data_channels = ['c3','c4']
ds = Database(root).load_dataset('all')
ds.summary()


# %%
