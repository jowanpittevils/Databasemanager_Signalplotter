#==================================================#
# Authors: Amir H. Ansari <amirans65.ai@gmail.com> #
# License: BSD (3-clause)                          #
#==================================================#

import sys
import numpy as np
import math
import mne
from datetime import datetime
from scipy.signal import decimate, resample
from databasemanager.EDF.channelMapper import mapper
from databasemanager.EDF.edfchannelinfo import EDFChannelInfo
from databasemanager.classes.channelinfolist import ChannelInfoList

class edf(object):
    '''
        channels=None: all standard channels. It can also be type of channels (e.g. EEG or ECG). To see or modify the channel names or types set edf.ini config file
        fs_type={'similar', 'uptomax'}. If it sets to similar, all channels must have similar frequency, otherwise an exceptions is raised.
        if 'uptomax' is selected, the fs is upsampled to the maximum available frequency.
        missing_channel={'error','skip'}
    '''
    @property
    def fs(self):
        return self.channels_info.fs_common

    @property
    def start_of_recording(self):
        return datetime.utcfromtimestamp(self.mne_raw.info['meas_date'][0])


    def __init__(self, filepath, channels=None, fs_type='similar', missing_channel=None):
        if(missing_channel is None):
            if(channels is None):
                missing_channel = 'skip'
            else:
                missing_channel = 'error'
        assert(missing_channel in ('error','skip'))
        assert(fs_type in ('similar', 'uptomax'))

        self.filepath = filepath

        #Load mapping config
        mapperobj = mapper()

        #get all channels if 'channels' is channel type (e.g. 'eeg')
        channels_by_type = mapperobj.get_channels_by_type(channels)
        if(channels_by_type is not None):
            channels = channels_by_type

        #check if all 'channels' are standard
        if(channels is None):
            channels = mapperobj.get_standard_channels()
        else:
            for ch in channels:
                if(not mapperobj.is_standard_key(ch)):
                    raise BaseException(ch + ' is not a standard channel. Please update channelMapper.py!')
        
        temp_r = mne.io.read_raw_edf(filepath, preload=False, verbose=0)
        ch_names = temp_r.ch_names 
        infile_fsList = temp_r._raw_extras[0]['n_samps']
        del temp_r
        all_infile_channel_names = set(ch_names)
        channels_info = ChannelInfoList([])
        for ind,ch in enumerate(ch_names):
            infile_name = ch
            infile_fs = infile_fsList[ind]
            name = mapperobj.find_matched_standard_key(infile_name)
            if(name is not None and name in channels):
                index = channels.index(name)
                channels_info.append(EDFChannelInfo(name, None, index, infile_name, infile_fs, ind))
        
        if(len(channels_info) != len(channels)): #missing channels
            if(missing_channel == 'error'):
                raise BaseException('There are some missing channels in: {}'.format(filepath))
            else:
                print('WARNING: {} has some missing channels!'.format(filepath))

        if(len(channels_info)>0):
            if(channels_info.similar_in_list('infile_fs') is not None):
                for ch in channels_info:
                    ch.fs = ch.infile_fs
            elif(fs_type == 'similar'):
                chstr = ','.join([str((c.infile_name, c.infile_fs)) for c in channels_info])
                chstr = f'path: {self.filepath}, channels: {chstr}'
                raise BaseException('The sampling frequencies of the selected channels are different! If you want to upsample them, change the fs_type to "uptomax". '+ chstr) 
            elif(fs_type == 'uptomax'):
                pass
            else:
                raise BaseException('The fs_type is unknown.')

            all_selected_channel_names = set([ch.infile_name for ch in channels_info])
            #mne does not support '-' in channel names: e.g. ECG-0 and ECG-1 both are counted at 'ECG'
            problemList = [c for c in all_selected_channel_names if '-'in c]
            assert(len(problemList)==0, f'mne does not support "-" in the target channel names: {str(problemList)}')
            excluded_channels = all_infile_channel_names - all_selected_channel_names

            #mne does not support '-' in channel names: e.g. ECG-0 and ECG-1 both are counted at 'ECG'
            extra_excluded = [ex for ex in excluded_channels if '-' in ex]
            extra_excluded = [ex.split('-')[0] for ex in extra_excluded]
            excluded_channels = set(list(excluded_channels) + extra_excluded)

            self.mne_raw = mne.io.read_raw_edf(filepath,exclude = list(excluded_channels), preload=False, verbose=0)

            #rename the channels to standard one
            mapping = {ch.infile_name:ch.name for ch in channels_info}
            self.mne_raw.rename_channels(mapping)

            #reorder channels to what is asked
            #channels_info.sort(key=lambda x: x.order)
            #self.mne_raw.reorder_channels([ch.name for ch in channels_info])

            for ch in channels_info:
                ch.fs = self.mne_raw.info['sfreq']
            channels_info.sort(key = lambda x: x.order)
            self.has_content = True
        else:
            self.has_content = False
            
        self.channels_info = channels_info

