#%%
#%reload_ext autoreload
#%autoreload 2

#%% databse
import numpy as np
from databasemanager import Database, Dataset, Criteria, UserSettings
from databasemanager import Subject,RecordingBase,AnnotationExtraInfo,Event
from databasemanager import EventExtraInfo, Annotation, Resampler, MontageMaker
from databasemanager.classes.datasetchanneljoiner import DatasetChannelJoiner

#root = 'C:\\MyFiles\\MyDatabases\\TempleSeizure'
root = r'C:\db\toyDB'
db = Database(root)
db.summary()

dsNames =  db.dataset_names

UserSettings.global_settings().loading_data_missing_channel_type = 'error'

#%%
ds1 = db.load_dataset('ds1', channel_names=['fp1','t3','o1','c3'])
ds1.add_background_label('NQS')
ds1.operations.append(Resampler(100))
ds1.operations.append(MontageMaker([('fp1','t3'),('t3','o1'),('o1','c3')]))
ds1.summary()

ds2 = db.load_dataset('ds1', channel_names=['resp'])
ds2.add_background_label('NQS')
ds2.operations.append(Resampler(100))
ds2.summary()

print(ds1.number_of_channels_output)
print(ds2.number_of_channels_output)

#%%
ds = DatasetChannelJoiner([ds1,ds2], data_mode='list')
print('here:', ds.subjects[0].recordings[0].name)
print('label:',ds.subjects[0].recordings[0].annotations[0].get_label(1,2))
x = ds.subjects[0].recordings[0].get_data2(1,2)
print(len(x))
print(x[0].shape)
print(x[1].shape)

# %%
ds = DatasetChannelJoiner([ds1,ds2], data_mode='matrix')
print('here:', ds.subjects[0].recordings[0].name)
x = ds.subjects[0].recordings[0].get_data2(1,2)
print(x.shape)

# %% check dataset properties
print('fs: ', ds.fs)
print('fs_output: ', ds.fs_output)
print('number of channels: ', ds.number_of_channels)
print('number of channels output: ', ds.number_of_channels_output)
print(str(ds))
print(repr(ds))

# %% check offline data
ds1.load_offline()
ds2.load_offline()
ds = DatasetChannelJoiner([ds1,ds2], data_mode='matrix')
# or after merging: 
ds.load_offline()

x = ds.subjects[0].recordings[0].get_data2(1,2)
print(x.shape)

#%% check shallow copy on subjects
print('subject level')
print('before, ds:', ds.subjects[0].name)
print('before, ds1:', ds1.subjects[0].name)
ds.subjects[0].name = 'amir'
print('after, ds:', ds.subjects[0].name)
print('after, ds1:', ds1.subjects[0].name)

# check shallow copy on recordings
print('recording level')
print('before, ds:', ds.subjects[0].recordings[0].name)
print('before, ds1:', ds1.subjects[0].recordings[0].name)
ds.subjects[0].recordings[0].name = 'amir_rec'
print('after, ds:', ds.subjects[0].recordings[0].name)
print('after, ds1:', ds1.subjects[0].recordings[0].name)


