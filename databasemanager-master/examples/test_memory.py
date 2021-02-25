#%%
#%reload_ext autoreload
#%autoreload 2

from databasemanager import *
from databasemanager.classes.path import Path
#import gc
 
def log_mem():
    (mem_used, mem_rem, mem_tot) = Dataset.memory_usage_psutil()
    prec = 2
    percent = mem_used*100/mem_tot
    print('memory (GB): used {}% ({}/{}), free: {}'.format(round(percent,prec), round(mem_used,prec), round(mem_tot,prec), round(mem_rem,prec)))
    return mem_used

#%%
root = r'C:\db\toyDB'

db = Database(root)
last_mem = log_mem()
UserSettings.global_settings().loading_data_missing_channel_type = 'error'
UserSettings.global_settings().loading_data_channels = ['fp1','fp2','t3','t4','o1','o2','c3','c4']
#dsname = 'test2'
dsname = 'ds1'
ds = Dataset.load_dataset(Path(root), dsname)
mem = log_mem()
print(mem - last_mem)

if(False):
    print('='*20)
    last_mem = log_mem()

    for s in ds.subjects:
        del s.recordings
        s.recordings = None

    del ds.operations


#        gc.collect()
    mem = log_mem()
    print(mem - last_mem)
    print('='*20)


# %% splitters
import numpy as np
from databasemanager import *
from databasemanager.splitters import split_subjects, LOSO, split_recordings, K_fold
root = r'C:\db\toyDB'
UserSettings.global_settings().loading_data_channels = ['c4','c3','fp1']

m0 = log_mem()
ds = Database(root).load_dataset('ds1')
m1 = log_mem()
(dstr,dsvl) = split_subjects(ds, ratio=0.5, deep_copying=False)
m2 = log_mem()


# %%
