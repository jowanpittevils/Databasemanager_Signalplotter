#%%
#%reload_ext autoreload
#%autoreload 2

import numpy as np
from glob import glob
import ntpath
import os
import math

#%%
root = r'C:\db\toyDB'
source = root +  r'\Extra\abnormalRes2.csv'


#%% load database for extra validation

from databasemanager import *
UserSettings.global_settings().loading_data_missing_channel_type = 'error'
UserSettings.global_settings().loading_data_channels = ['fp1','fp2','t3','t4','o1','o2','c3','c4','cz']
ds = Database(root).load_dataset('all')
ds.summary()
#%%