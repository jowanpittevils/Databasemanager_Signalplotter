#%%
from databasemanager.operators.firfilter import FIRFilter
from databasemanager.operators.notchfilter import NotchFilter
from databasemanager.operators.resampler import Resampler
from databasemanager.operators.montagemaker import MontageMaker
from databasemanager.operators.rereferencer import Rereferencer
from databasemanager.operators.shrinker import Shrinker
import numpy as np
from databasemanager import *
from datagenerator.generators.randomsubjectgenerator import RandomSubjectGenerator
from signalplotter import iplot, gplot

chs = ['cz','fp1','fp2','c3','c4','t3','t4','o1','o2']
UserSettings.global_settings().loading_data_channels = chs
root = 'C:\\MyFiles\\MyDatabases\\Sleep'
ds = Database(root).load_dataset('preterm_nina_train_13')


#%%
dst = ds.copy()
dst.operations.append_filter(FIRFilter([0.5,40],151, approach='filter'))
dst.summary()

import time
batch_size = 64
N = batch_size*10
frame = 30
t = time.time()
for i in range(int(N)):
    x = dst.subjects[0].recordings[0].get_data(0,int(dst.fs_output*frame),True)
print(x.shape)
elapsed = time.time() - t    
print('frame lenght (s): ', frame)
print('# channel: ', dst.number_of_channels_output)
print('# loads: ', N)
print('Total seconds: ', elapsed)
print('ms per segment load: ', round(elapsed*1000/N))
print('ms per batch load: ', round(elapsed*1000/N*batch_size))



# %%
