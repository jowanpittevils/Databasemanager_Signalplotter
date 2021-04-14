#%%
import numpy as np
from databasemanager import *
from signalplotter import iplot, agplot

chs = ['o2','fp1','o1','cz']
UserSettings.global_settings().loading_data_channels = chs

root = r'C:\db\toyDB'
ds = Database(root).load_dataset('ds1')
ds.summary()


#%%
x = ds.subjects[0].recordings[0].get_data(0,1205)
x.shape
x = np.expand_dims(x, 2)
x = x.transpose([2,1,0])
agplot(x, fs=250, channel_names=chs)
# %%

# %%
