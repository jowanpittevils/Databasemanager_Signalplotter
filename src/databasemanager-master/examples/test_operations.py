#%%
%reload_ext autoreload
%autoreload 2

import numpy as np
from databasemanager import *
from databasemanager.operators.shrinker import Shrinker
from signalplotter import iplot, agplot


root = 'D:\\MyFiles\\MyDatabases\\Sleep'
UserSettings.global_settings().loading_data_channels = ['c4','c3','fp1']
ds = Database(root).load_dataset('test')

#%%
ds.summary()
print(ds.unique_labels)
ds.add_background_label('NQS')
print(ds.unique_labels)

print('ds.fs: ',ds.fs)
print('ds.fs_output: ',ds.fs_output)
print('ds.number_of_channels: ',ds.number_of_channels)
print('ds.number_of_channels_output: ',ds.number_of_channels_output)

# %% 
dst = ds.copy()
dst.add_operator(FIRFilter([1,30], N=151, output_type='valid'))
dst.add_operator(Resampler(100))
dst.add_operator(Resampler(10))
dst.add_operator(Rereferencer('fp1'))
dst.add_operator(MontageMaker([('c3','c4')]))
dst.summary()

print('dst.fs: ',dst.fs)
print('dst.fs_output: ',dst.fs_output)
print('dst.number_of_channels: ',dst.number_of_channels)
print('dst.number_of_channels_output: ',dst.number_of_channels_output)


#%%
start=0
stop=start + 30
print(dst.subjects[0].recordings[0].get_data(start,stop, True).shape)

#%% resampler after resampler
dst = ds.copy()
dst.add_operator(Resampler(100))
dst.add_operator(Resampler(10))
dst.summary()
print(dst.fs)
print(dst.fs_output)
#%% resampler after resampler
dst = ds.copy()
dst.add_operator(Resampler(100))
dst.add_operator(FIRFilter([1,30], N=151, output_type='same'))

x = dst.subjects[0].recordings[0].get_data(0,300)
x.shape

#%%
print(Resampler(100).serialize())
print(Rereferencer('fp1').serialize())
print(MontageMaker([('c3','c4')]).serialize())
print(FIRFilter([1,30], N=151, output_type='valid').serialize())

#%% test offline
dst = ds.copy()
dst.add_operator(NotchFilter(50)) #Notch
dst.load_offline()
dst.add_operator(NotchFilter(10)) #Notch
x5 = np.transpose(dst.subjects[0].recordings[0].get_data(0,int(30)))
print(x5.shape)

#%%
dst = ds.copy()
dst.add_operator(NotchFilter(50)) #Notch
dst.subjects[0].add_operator(NotchFilter(100)) #Notch
x5 = np.transpose(dst.subjects[0].recordings[0].get_data(0,int(30)))
v = dst.operators
print(v)

#%% firfilter
dst = ds.copy()
x0 = np.transpose(dst.subjects[0].recordings[0].get_data(0,int(30)))
dst.add_operator(FIRFilter([0,20]))# low pass
x1 = np.transpose(dst.subjects[0].recordings[0].get_data(0,int(30)))
print(dst.operators[-1])

dst = ds.copy()
dst.add_operator(FIRFilter([10,ds.fs/2])) #high-pass
x2 = np.transpose(dst.subjects[0].recordings[0].get_data(0,int(30)))
print(dst.operators[-1])

dst = ds.copy()
dst.add_operator(FIRFilter([0.5,15])) #band-pass
x3 = np.transpose(dst.subjects[0].recordings[0].get_data(0,int(30)))
print(dst.operators[-1])

dst = ds.copy()
dst.add_operator(FIRFilter([0,5,10,125])) #band-stop
x4 = np.transpose(dst.subjects[0].recordings[0].get_data(0,int(30)))
print(dst.operators[-1])


dst = ds.copy()
dst.add_operator(NotchFilter(50)) #Notch
x5 = np.transpose(dst.subjects[0].recordings[0].get_data(0,int(30)))
print(dst.operators[-1])

sts = ['raw','0-10','10-125','0.5-15','0-5,10-125','notch(50)']
dd = np.stack((x0[:,0], x1[:,0], x2[:,0], x3[:,0], x4[:,0], x5[:,0]), 1)
iplot(dd, fs=dst.fs, channel_names=sts, channel_first=False)

# %% resampler
dst = ds.copy()
dst.add_operator(Resampler(100))
print(dst.operators[-1])
print(dst.subjects[0].recordings[0].get_data(0,int(30)).shape)

# %% montagemaker
dst = ds.copy()
dst.add_operator(MontageMaker([('c3','c4'), ('fp1', 'c3')]))
print(dst.subjects[0].recordings[0].get_data(0,int(30)).shape)
print(dst.operators[-1])

#%% rereferencer
dst = ds.copy()
dst.add_operator(Rereferencer('c3'))
print(dst.operators[-1])
print(dst.subjects[0].recordings[0].get_data(0,int(30)).shape)

# %% Shrinker
dst = ds.copy()
dst.add_operator(Shrinker(50,20))
print(dst.operators[-1])
print(dst.subjects[0].recordings[0].get_data(0,int(30)).shape)


# %%
import numpy as np
from databasemanager.operators.notchfilter import NotchFilter
from databasemanager.operators.firfilter import FIRFilter
from signalplotter import iplot, agplot

fs = 100
T = 10
f = 4

t = np.linspace(0, T, T*fs)
x = np.sin(2*np.pi*t*f)
x=np.expand_dims(x,1)

#filt = NotchFilter(4) #Notch
filt = FIRFilter([1,3],output_type='same') 
filt.set_axis(1)
filt.set_fs(fs)
y = filt.filter(np.transpose(x))
y = np.transpose(y)
print(filt.correction_samples)

iplot(x, fs=fs, auto_normalize=False, channel_first=False)
iplot(y, fs=fs, auto_normalize=False, channel_first=False)
mse = ((x - y)**2).mean(axis=0)
print(mse)




# %% serialize 

