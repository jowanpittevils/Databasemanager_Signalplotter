# %%
import time
import mne
from EDF.ezEDF import edf

edfPath = 'C:\\MyFiles\\My Data\\Amir\\AmirDataBase\\database\\Data\\r_e55555\\e55555a.edf'
print('='*30)
print('edf path: ',edfPath)
print('edf duration: ~ 1 h')
print('edf size: ~ 43 MB')
print('='*30)
# %%
print('Loading by MNE ...')
tf0 = time.time()
mneObj = mne.io.read_raw_edf(edfPath)
mne_data = mneObj.get_data()
tf1 = time.time()
print('Done. elapsed sec: ', tf1-tf0)
print('='*30)
# %%
print('Loading by ezEDF ...')
tf0 = time.time()
edfObj = edf(edfPath)
edf_data = edfObj.read()
tf1 = time.time()
print('Done. elapsed sec: ', tf1-tf0)
print('='*30)

#%%
edfpath = 'C:\\MyFiles\\MyDatabases\\tt.edf'