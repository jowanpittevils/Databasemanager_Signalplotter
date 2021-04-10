#%%
import numpy as np
from databasemanager import *
import time

root = 'C:\\MyFiles\\MyDatabases\\Sleep'
UserSettings.global_settings().loading_data_channels = ['fp1', 'fp2', 'c3', 'c4', 't3', 't4', 'o1', 'o2', 'cz']
Database(root).dataset_names
ds = Database(root).load_dataset('preterm_nina_train_13')
ds.summary()
#%%
def _load_offline_one_recording(recname):
    root = 'C:\\MyFiles\\MyDatabases\\Sleep'
    UserSettings.global_settings().loading_data_channels = ['fp1', 'fp2', 'c3', 'c4', 't3', 't4', 'o1', 'o2', 'cz']
    ds = Database(root).load_dataset('preterm_nina_train_13')
    rec = ds.take(Criteria(RecordingBase, lambda rec: rec.name == recname))
    assert(len(rec)==1)
    rec = rec[0]
    x = rec.get_data(start=0,stop=None,compensate_filter_shrinking=False,out_of_range='error')
    return {rec:x}  
#%%
from joblib import Parallel, delayed
import multiprocessing

print(__name__)
if __name__ != "__main__":
    quit()

tm = time.time()
num_cores = multiprocessing.cpu_count()
recs = ds.take(Criteria(RecordingBase, lambda x: True))
recs = [rec.name for rec in recs]
res = Parallel(n_jobs=num_cores)(delayed(_load_offline_one_recording)(rec) for rec in recs)
res_list = {}
non = [res_list.update(r) for r in res]

print('par ellpsed: '+str(time.time()-tm))

#res = ds._load_offline_one_recording(recs[0])
#print(len(res_list.keys()))

#%%
tm = time.time()
ds.load_offline()
print('normal ellpsed: '+str(time.time()-tm))
