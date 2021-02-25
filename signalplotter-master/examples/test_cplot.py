#%%
#%reload_ext autoreload
#%autoreload 2

import numpy as np
from signalplotter import cplot


fs = 250
CH = 6
samples = fs * 3600 - 500
x = np.random.randn(CH,samples)/5
title='Raw data'
chn=['Fp1','Fp2','C3','C4','O1','O2']
print(chn)

#%%
cplot(x, fs=250, channel_first=True)

# %%
cplot(x[1,:], fs=250, channel_first=True)

# %%
cplot([[x[1,:], x[2,:]]], fs=250, channel_first=True)
