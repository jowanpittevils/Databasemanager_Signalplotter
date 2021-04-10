#%%
%reload_ext autoreload
%autoreload 2

#%%
import numpy as np
from databasemanager import *
from databasemanager.splitters import split_subjects, LOSO, split_recordings, K_fold
root = 'C:\\MyFiles\\MyDatabases\\Sleep'
UserSettings.global_settings().loading_data_channels = ['c4','c3','fp1']
ds = Database(root).load_dataset('term_Kirubin_16')



#%% split_subjects
(dstr,dsvl) = split_subjects(ds, ratio=0.5)

ds.summary()
dstr.summary()
dsvl.summary()

print(type(dstr.subjects))
# %% LOSO
dataset_list = LOSO(ds)
print(len(dataset_list))

n = 5
dataset_list[n][0].summary()
dataset_list[n][1].summary()

# %% k_fold
dataset_list = K_fold(ds,3)
print(len(dataset_list))

dataset_list[0][1].summary()
dataset_list[1][1].summary()
dataset_list[2][1].summary()
# %% test add stop point
print(ds.subjects[0].recordings[0].annotations[0].events[0])
print(ds.subjects[0].recordings[0].annotations[0].events[1])
print(len(ds.subjects[0].recordings[0].annotations[0].events)) 

ds.subjects[0].recordings[0].annotations[0].add_stop_point(920)
print(ds.subjects[0].recordings[0].annotations[0].events[0])
print(ds.subjects[0].recordings[0].annotations[0].events[1])
print(ds.subjects[0].recordings[0].annotations[0].events[2])
print(len(ds.subjects[0].recordings[0].annotations[0].events))

#%% split_subjects
(dstr,dsvl) = split_recordings(ds, ratio=0.5)

ds.summary()
dstr.summary()
dsvl.summary()

# %%
