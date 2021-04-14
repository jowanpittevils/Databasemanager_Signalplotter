#%%
import numpy as np
from signalplotter import agplot, iplot
from scipy.signal import get_window, firwin, filtfilt
from databasemanager.operators.firfilter import FIRFilter
from databasemanager.operators.filtercorrector import FilterCorrector
from databasemanager.operators.resampler import Resampler

fs=250
f=2
t = np.arange(0,4,1/fs)
x = np.sin(t * 2 * f * np.pi)
x = np.expand_dims(x,0)
x = np.expand_dims(x,2)

#x = np.random.randn(10,1000,2)
#print('x.shape: ',x.shape)

N = 255
b = firwin(numtaps=255, cutoff=[10,40], window='hamming', fs = fs, pass_zero=False)
print('b.shape: ',b.shape)
y=filtfilt(b,1,x,axis=1)
print('y.shape: ',y.shape)

iplot(x[0,:,:], fs,auto_normalize=False)
iplot(y[0,:,:],fs,auto_normalize=False)

#agplot([[x,y]])
# %%
correct_samples=True
f = FIRFilter(cutoffs=[1,40], N=255, approach='filter')
f.set_fs(fs)
f.set_axis(1)
c = FilterCorrector(f)
c.set_axis(1)
print(x.shape)
yy = f.apply(x)
print(yy.shape)
yy = c.apply(yy)
print(yy.shape)
if(correct_samples):
    yyt = np.zeros((x.shape[0],f.correction_samples[0],x.shape[2]))
    yyt = np.concatenate((yyt,yy,yyt),1)
else:
    yyt = yy

print(yyt.shape)


r = Resampler(100)
r.set_fs(fs)
r.set_axis(1)
yyt_s = r.apply(yyt)
print(yyt_s.shape)
#agplot([[x,yyt], yyt_s])
iplot(x[0,],auto_normalize=False)
iplot(yyt[0,],auto_normalize=False)

# %%
from scipy.signal import resample
print(x.shape)
T = x.shape[1]/fs
fs_new=100
resample(x,int(fs_new*T), axis=1, window='hamming').shape


# %% test delays
from scipy.signal import lfilter, filtfilt
#x = np.array([5,2,3,4,5,6,5,4,3,2,5])
fs=100
t=np.arange(0,2,1/fs)
x = np.sin(2*np.pi*t*5)
N = 10
b = np.ones(N)/N
gp = int((N-1)/2)
a = 1
y0 = lfilter(b,a,x)
y0 = np.concatenate((y0[gp:],np.zeros(gp)))
y1 = filtfilt(b,a,x)

import matplotlib.pyplot as plt
plt.plot(x)
plt.plot(y0)
plt.plot(y1)
print(b)
#print(np.stack((x,y0,y1),0))





# %%
