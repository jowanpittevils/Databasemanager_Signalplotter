#%%
import mne
root = r'C:\db\toyDB'
p = r'C:\db\toyDB\Data\tr_ar_492\tr_ar_492_r4.edf'

temp_mne_raw = mne.io.read_raw_edf(p, exclude=('I'), preload=False)
#print(temp_mne_raw.info)
print(temp_mne_raw.info['sfreq'])
print(temp_mne_raw.info['nchan'])
print(len(temp_mne_raw))

fs=500
l_sec=(16*3600+58*60+39)
l = l_sec*fs
print(l)

# %%
from EDF.mne_edf_extensions import read_raw_edf_channelInfo
l = read_raw_edf_channelInfo(p)

# %%
