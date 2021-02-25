
#%%
import mne
p = 'C:\\MyFiles\\MyDatabases\\tt_csharper.edf'
p2 = 'C:\\MyFiles\\MyDatabases\\tt2.edf'

r = mne.io.read_raw_edf(p, stim_channel=None, preload=False)
r.ch_names
r.annotations
# %%
