#%%
%reload_ext autoreload
%autoreload 2


from signalplotter import iplot
import numpy as np
from databasemanager import Database, Dataset, UserSettings
from databasemanager.operators.resampler import Resampler
from databasemanager.operators.firfilter import FIRFilter
from databasemanager.operators.rereferencer import Rereferencer
from databasemanager.operators.notchfilter import NotchFilter
import time




root = r'C:\db\toyDB'
db = Database(root)
db.summary()
dsNames =  db.dataset_names

UserSettings.global_settings().loading_data_channels = ['fp1', 'fp2', 'c3', 'c4', 't3', 't4', 'o1', 'o2', 'cz']

ds = db.load_dataset('ds1')
ds.operations.append(FIRFilter([1,10],255))
ds.summary()

ds.subjects[0].recordings[0].annotations[0]
#%% apply operators before loading offline
ds = db.load_dataset('ds1')
#ds.operations.append(FIRFilter([1,10],255))
#ds.operations.append(Rereferencer('c3'))
ds.operations.append(FIRFilter([2,5],255))
ds.operations.append(NotchFilter(50))
ds.operations.append(Resampler(100))
ds.summary()
print('loading offline...')
ds.load_offline(-2)
ds.summary()
#%% apply operators after loading offline 
ds2 = db.load_dataset('ds2')
print('loading offline...')
ds2.load_offline()
#ds2.operations.append(FIRFilter([1,10],255))
#ds2.operations.append(Rereferencer('c3'))
ds2.operations.append(FIRFilter([2,5],255,approach='filtfilt'))
ds2.operations.append(NotchFilter(50))
ds2.operations.append(Resampler(100))
#%% compare after and before operators
print(f'ds  10 sec shape: { ds.subjects[0].recordings[0].get_data(0,10).shape}')
print(f'ds2 10 sec shape: {ds2.subjects[0].recordings[0].get_data(0,10).shape}')

import matplotlib.pyplot as plt
plt.plot(ds.subjects[0].recordings[0].get_data(10,20)[0,])
plt.plot(ds2.subjects[0].recordings[0].get_data(10,20)[0,])
plt.show()
print(ds2.subjects[0].recordings[0].name)

#%% merge and subtract
ds2 = ds.copy()
ds2.load_offline()
ds2.summary()

ds3 = db.load_dataset('ds2')
ds3.load_offline()
ds3.summary()




dd = (ds2-ds3)
dd.summary()

print(len(ds2.offline_data.data.keys()))
print(ds2.offline_data.data.keys())
print(len(ds3.offline_data.data.keys()))
print(ds3.offline_data.data.keys())
print(len(dd.offline_data.data.keys()))
print(dd.offline_data.data.keys())


#%%
ds2 = ds.copy()
ds.load_offline()
ds2.load_offline()

ds3 = ds2 + ds
ds3.summary()
#%% test polys
ds_p = ds.copy(deep_copy_offline_data=True)
ds_f = ds.copy(deep_copy_offline_data=True)

ds_p.operations.append(Resampler(100))
ds_f.operations.append(Resampler(100, approach='fft'))

t0 = time.time()
print('poly...')
ds_p.load_offline()
t1 = time.time()
print('fft...')
ds_f.load_offline()
t2 = time.time()
print('done')
print('poly time: ',t1-t0)
print('fft  time: ',t2-t1)

x_p = ds_p.subjects[0].recordings[0].get_data(0, 10)
print(x_p.shape)
x_f = ds_f.subjects[0].recordings[0].get_data(0, 10)
print(x_f.shape)
iplot(np.transpose(x_f))
iplot(np.transpose(x_f))


# %%
ds.operations.append(Resampler(100))
ds.load_offline(-5)
print('ds: ',len(ds.offline_data))
ds2 = ds.copy(deep_copy_offline_data=False)
print('ds2: ',len(ds2.offline_data))
ds2.delete_offline()
print('ds2: ',len(ds2.offline_data))
print('ds: ',len(ds.offline_data))
ds.delete_offline()
print('ds: ',len(ds.offline_data))

#%% {run it after the first cell}
ds2 = ds.copy(deep_copy_offline_data=False)
ds2.load_offline(-5)
x1 = ds2.subjects[0].recordings[0].get_data(
                                        0,
                                        10,
                                        compensate_filter_shrinking=False,
                                        fource_to_load_from_file=False)
print(x1.shape)
ds2.operations.append(Resampler(10))
x2 = ds2.subjects[0].recordings[0].get_data(
                                        0,
                                        10,
                                        compensate_filter_shrinking=False,
                                        fource_to_load_from_file=False)
print(x2.shape)
iplot(np.transpose(x1))
iplot(np.transpose(x2))

#%% {run it after the first cell}
t0 = time.time()
x1 = ds.subjects[0].recordings[0]._get_data_in_sample(
                                        0,
                                        500,
                                        compensate_filter_shrinking=False,
                                        fource_to_load_from_file=False)
print(x1.shape)
t1 = time.time()
x2 = ds.subjects[0].recordings[0]._get_data_in_sample(
                                        0,
                                        500,
                                        compensate_filter_shrinking=False,
                                        fource_to_load_from_file=True)
t2 = time.time()
print(x2.shape)
print('mse: ',((x1-x2)**2).sum())
print('offline time: ',t1-t0)
print('lazy time: ',t2-t1)
print('ratio:', round((t2-t1)/(t1-t0)))


#%% speed

N = 10000 
w = 30
stop = int(w*ds.fs)
print('tested on N: {}, window size: {}, fs: {}'.format(N, w, ds.fs))
t = time.time()
for i in range(N):
    x = ds.subjects[0].recordings[0]._get_data_in_sample(
                                        0,
                                        stop,
                                        compensate_filter_shrinking=False,
                                        fource_to_load_from_file=False)

elapsed_online = time.time() - t    
print('online: {}ms per load.'.format(elapsed_online/N*1000))
print('online for 50K windows, 100 epochs: {}h'.format(elapsed_online/N*50000*100/3600))
t = time.time()
for i in range(N):
    x = ds.subjects[0].recordings[0]._get_data_in_sample(
                                        0,
                                        stop,
                                        compensate_filter_shrinking=False,
                                        fource_to_load_from_file=True)

elapsed_offline = time.time() - t

print('offline: {}ms per load.'.format(elapsed_offline/N*1000))
print('offline for 50K windows, 100 epochs: {}h'.format(elapsed_offline/N*50000*100/3600))
print('ratio:', round(elapsed_offline/elapsed_online))
# %%
ds.delete_offline()




