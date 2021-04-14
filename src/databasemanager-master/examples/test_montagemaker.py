#%%
import numpy as np
from signalplotter import agplot, iplot
from databasemanager.operators.montagemaker import MontageMaker
from databasemanager.operators.rereferencer import Rereferencer
from databasemanager import *


root = 'C:\\MyFiles\\MyDatabases\\Sleep'
UserSettings.global_settings().loading_data_channels = ['c4','c3','fp1']
ds = Database(root).load_dataset('test')
ds.summary()

#%% montage maker
x = ds.subjects[0].recordings[0].get_data(0,100)
print(x.shape)
cmap = [('c4','c3'),('fp1','c3')]
m = MontageMaker(cmap, ds.subjects[0].recordings[0].channel_info_list, 0)
y = m.apply(x)
print(y.shape)

c1 = x[0:1,] - x[1:2,]
c2 = x[2:3,] - x[1:2,]
cc = np.concatenate((c1,c2),0)

print(cc.shape)
iplot(np.transpose(cc))
iplot(np.transpose(y))

# %% rereferencer
x = ds.subjects[0].recordings[0].get_data(0,100)
print(x.shape)
r = Rereferencer('c3', ds.subjects[0].recordings[0].channel_info_list, 0, False)
y = r.apply(x)
print(y.shape)

c1 = x[0:1,] - x[1:2,]
c2 = x[2:3,] - x[1:2,]
cc = np.concatenate((c1,c2),0)

print(cc.shape)
iplot(np.transpose(cc))
iplot(np.transpose(y))


# %%
