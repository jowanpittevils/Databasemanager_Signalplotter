
#%%
import mne
p = r'C:\db\toyDB\Data\tr_ar_492\tr_ar_492_r4.edf'


r = mne.io.read_raw_edf(p, stim_channel=None, preload=False)
r.ch_names
r.annotations
# %%
