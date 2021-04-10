#%%
from databasemanager.EDF.channelMapper import mapper
m = mapper()

print(m.chList.items())
print(m.findMatchedStandardKeys('fp1'))

# %%
from EDF.ezEDF import edf
p = 'C:\\MyFiles\\MyDatabases\\test1.edf'
edf1 = edf(p, ['fp1','fp2'], 'uptomax',None)
p=edf1.mne_raw.plot(start=60, duration=60, scalings='auto')
#%%
#p = 'C:\\MyFiles\\MyDatabases\\Sleep\\Data\\PT 79_5\\PT 79_5.EDF'
p = 'C:\\MyFiles\\MyDatabases\\test1.edf'
edf2 = edf(p, ['o1','o2','fp2','cz'], 'similar')
p=edf2.mne_raw.plot(duration=300, scalings='auto')
edf1.mne_raw.load_data



import mne
mne.concatenate_raws([edf1.mne_raw,edf2.mne_raw])
p=edf1.mne_raw.plot(duration=600, scalings='auto')

# %%
