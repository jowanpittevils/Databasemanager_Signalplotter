#%%
#%reload_ext autoreload
#%autoreload 2

import numpy as np
from signalplotter import iplot, gplot


fs = 250
win = 10
CH = 6
samples = 2000
x = np.random.randn(samples,CH,win*fs)/5
y = np.random.randint(2,size=samples)
title='Raw data'
chn=['Fp1','Fp2','C3','C4','O1','O2']
print(chn)
fs2 = 50
x2 = np.random.randn(samples,CH,win*fs2)/5

fs3 = 10
title2='pre Processed data'
chn3=['f1','f2','f3']
x3 = np.random.randn(samples,3,win*fs3)/5
title3='features'

xx = np.random.randn(samples,CH,win*fs)/7
help(gplot)


#%% ezplot
iplot(x[0,])
iplot(x[0,],fs)
iplot(x[0,],fs,channel_names=chn)

#%% simple plot 
gplot(x)

#%% holded
fav=gplot([[x,xx]])
fav

#%% bar
fs4 = -1
title2='final features'
chn4=['fs1','fs2','fs3']
x4 = np.random.randn(samples,1,3)**2
title4='feat'

fav=gplot([[x4,x4/2,x4*3, x4/5]], fs=-1)
fav

#%% plotting with labels
fav=gplot(x,y=y)
fav

#%% plotting with title and sensitivity
fav=gplot(x,title=title, sens=0.1)
fav

#%% plotting with channel names
fav=gplot(x, y=y,title=title, fs=fs, channel_names=chn)
fav


#%% plotting multiple signals

fav=gplot([x,x2, x3], y=y,title=[title, title2, title3], fs=[fs,fs2,fs3], channel_names=[chn,chn,chn3])
fav

#%% plotting with bar
fs4 = -1
title2='final features'
chn4=['fs1','fs2','fs3','fs4']
x4 = np.random.randn(samples,1,4)**2
x4 = x4/x4.max()
title4='Probability'
#fav=gplot(x4, y=y,title=title4, fs=fs4, channelNames=chn4)
fav=gplot([[x,xx],x3,[x4,x4/2]], y=y,title=[title,title3,title4], fs=[fs,fs3,fs4], channel_names=[chn,chn3,chn4])
fav

# %% callback
import matplotlib.pyplot as plt
def myCallback(x, index):
    print('index: {0}, x.shape: {1}'.format(index, x.shape))

fav=gplot(x, y=y,title=title, fs=fs, channel_names=chn, callback = myCallback)
fav

# %%
