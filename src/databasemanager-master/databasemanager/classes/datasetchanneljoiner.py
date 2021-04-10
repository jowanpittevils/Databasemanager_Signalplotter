#==================================================#
# Authors: Amir H. Ansari <amirans65.ai@gmail.com> #
# License: BSD (3-clause)                          #
#==================================================#

import gc
import copy
import numpy as np
from tqdm import tqdm
from prettytable import PrettyTable
from psutil import virtual_memory
from databasemanager.tsvreader import TSVReader
from databasemanager.classes.dataset import Dataset
from databasemanager.operators.operatorbase import OperatorBase
from databasemanager.operators.filterbase import FilterBase
from databasemanager.operators.resampler import Resampler
from databasemanager.operators.montagemaker import MontageMaker
from databasemanager.operators.rereferencer import Rereferencer
from databasemanager.classes.path import Path
from databasemanager.classes.listextension import ListExtension
from databasemanager.classes.subject import Subject
from databasemanager.classes.MNEfetchableinterface import MNEFetchableInterface
from databasemanager.classes.queryable import Queryable
from databasemanager.classes.criteria import Criteria
from databasemanager.classes.recordingbase import RecordingBase
from databasemanager.classes.recording import Recording
from databasemanager.classes.event import Event
from databasemanager.classes.saveable import Saveable
from databasemanager.classes.offlinedata import OfflineData
from databasemanager.classes.annotation import Annotation


  



class DatasetChannelJoiner(Dataset):
    '''
    This class is for merging multiple datasets in which everything including subjects, recordings, annotations, and events are the
    same while there channels are different. For instance, in multi-modal cases where there is one dataset for EEGs and one for ECGs.
    * for merging datasets with different subjects (equal channels) you can use 'ds1 + ds2' (and not this class).
    This class is mainly designed for recording.get_data() and annotation.get_label() functions, there is no guarantee for other functionalities.
    Its objects can be used in the datagenerator toolbox provided a proper order is designed.
    Note that this classes uses a shallow copy of the first dataset. so changing the items of this results in changing that dataset.

    parameters:
    -----------
    deatasets: a tuple or list of datasets which should be merged. It must have at least two items.
    data_mode: [case-insensitive] to return data as a list or as a matrix in recording.get_data() function.
    -- 'list' or 'l': [default] returns a list where the size of this list equals the length of the given dataset list; one item for each dataset.
    -- 'matrix' or 'm':  returns a matrix where the outputs are concatenated in the channel mode (0th mode). If the sampling frequencies do not match, an exception arises.

    e.g. if ds1 includes 1 ECG channel (250 Hz) and ds2 includes 2 EEG channels (250 Hz)
        then:
        x = DSJoinedChannels([ds1,ds2], 'list').subjects[0].recordings[0].get_data(0,1)
        print(len(x)) #--> 2
        print(x[0].shape) #--> (1, 256)
        print(x[1].shape) #--> (2, 256)

        x = DSJoinedChannels([ds1,ds2], 'matrix').subjects[0].recordings[0].get_data(0,1)
        print(x.shape) #--> (3, 256) in this order (ECG, EEG1, EEG2)
    '''
    def __init__(self, datasets: list, data_mode:str = 'list'):
        data_mode = data_mode.lower()
        self.__validate(datasets, data_mode)
        self.name = 'joind_dataset'
        self.comments = '+'.join([ds.name for ds in datasets])
        self.datasets = datasets
        self.data_mode = data_mode
        self.subjects = []
        self.operators = None
        self.offline_data = OfflineData()
        for s in self.datasets[0].subjects:
            ss = copy.copy(s)
            self.subjects.append(ss)
            for r in ss.recordings:
                r.get_data2 = self.__joint_load_data(r.name)

    def __joint_load_data(self, rec_name, *args, **dargs):
        def load_data(*args,**dargs):
            x = []
            for ds in self.datasets:
                r = ds.find_recording(rec_name, True)
                assert(r is not None)
                x.append(r.get_data(*args, **dargs))
            if(self.data_mode[0] == 'l'):
                return x
            elif(self.data_mode[0] == 'm'):
                return np.concatenate(x,0)
        return load_data

    @staticmethod
    def __validate(datasets, data_mode):
        assert(data_mode in ('list','l','matrix','m'))
        assert(isinstance(datasets, tuple) or (isinstance(datasets, list)))
        assert(datasets is not None)
        assert(len(datasets)>1)
        ref = datasets[0]
        recordings = ref.take(Criteria(Recording))
        events = ref.take(Criteria(Event))
        for ds in datasets:
            if(data_mode[0] == 'm'):
                if(ds.fs_output != ref.fs_output):
                    raise ValueError(f'The sampling frequencies of the datasets are not equal while data_mode is "matrix" ({ds.fs_output} vs. {ref.fs_output}). You can set data_mode to "list" or use a Resampler operator in the datasets.')

            if(not isinstance(ds, Dataset)):
                raise ValueError(f'All the input datasets must be a Dataset object, while one is {type(ds)}')
            if(ds != ref):
                r = ds.take(Criteria(Recording))
                for i in range(len(r)):
                    assert((i < len(recordings)) and (recordings[i].name == r[i].name))
                e = ds.take(Criteria(Event))
                for i in range(len(e)):
                    assert((i < len(events)) and (str(events[i]) == str(e[i])))


    # override MNEFetchableInterface.fetch_mne_list()
    def fetch_mne_list(self, set_annotations: bool = True):
        raise ValueError("For this class it is not implemented!")
    
    #override
    def copy(self, new_name:str = None, deep_copy_offline_data:bool = False, deep_copy_elements:bool = True):
        raise ValueError("For this class it is not implemented!")

            
    #override copyabledoubleside
    def reassign(self):
        for ds in self.datasets:
            for sub in ds.subjects:
                sub.dataset = self
                sub.reassign()
        
    def add_operator(self, operator:OperatorBase):
        assert(isinstance(operator, OperatorBase))
        for ds in self.datasets:
            for sub in self.subjects:
                for rec in sub.recordings:
                    rec.add_operator(operator)

    @property
    def fs(self):
        ls = []
        for ds in self.datasets:
            ls = ls +[sub.fs for sub in ds.subjects]
        fs = ListExtension(ls)
        return fs.similar_in_list()

    @property
    def fs_output(self):
        '''It returns the sampling frequency of the loaded data and can be affected by resampling operators (the last one).'''
        ls = [ds.fs_output for ds in self.datasets]
        fs = ListExtension(ls)
        return fs.similar_in_list()

    @property
    def number_of_channels_output(self):
        '''It returns the number of channels of the loaded data and can be affected by montagmaker operators (the last one).'''
        chlist = []
        for ds in self.datasets:
            cc = ds.number_of_channels_output
            if(cc is None):
                return None
            chlist.append(cc)
        return np.sum(np.array(chlist))

    @property
    def number_of_channels(self):
        chlist = []
        for ds in self.datasets:
            ch = ListExtension([sub.number_of_channels for sub in ds.subjects])
            cc = ch.similar_in_list()
            if(cc is None):
                return None
            chlist.append(cc)
        return np.sum(np.array(chlist))

    def __str__(self):
        ss = ""
        if(len(self)>0):
            ss = ": " + ",".join(str(sub.name) for sub in self.subjects)
        MAXLEN = 50
        if(len(ss)>MAXLEN):
            ss = ss[0:MAXLEN] + "..."
        return "<dataset {0} includs {1} subject(s){2}>".format(self.name, len(self), ss)
    
    def __repr__(self):
        line_len = 50
        title = " Dataset "
        left_line_len = (line_len-len(title))//2
        ss = "="*left_line_len + title + "="*(line_len-left_line_len-len(title)) + "\n"
        ss += (f'\nThis dataset includes multiple ({len(self.datasets)}) datasets.')
        ss += "Name: " + self.name + "\n"
        showing_comments = "".join(self.comments)
        len_showing_comments = len(showing_comments)
        maxl_comment = line_len-10-3 # 10 = len("Comments: "), 3 = len('...')
        showing_comments = showing_comments[0:maxl_comment]
        if(len_showing_comments>maxl_comment):
            showing_comments += "..."

        ss += "Comments: " + showing_comments + "\n"
        ss += "\n"
        ss += "#Subjects: {0}".format(self.number_of_subjects) + "\n"
        ss += "#Recordings: {0}".format(self.number_of_recordings) + "\n"
        ss += "#Annotations files: {0}".format(self.number_of_annotations) + "\n"
        ss += "#Events: {0}".format(self.number_of_events) + "\n"
        ss += "total duration: {0}".format(round(self.duration_sec/3600, 1)) + " hours\n"
        
        return ss
    
    def summary(self):
        print(f'This dataset includes multiple ({len(self.datasets)}) datasets.')
        for i,ds in enumerate(self.datasets):
            print(f'{i+1})')
            ds.summary()
        
    def __add__(self, other):
        raise ValueError("For this class it is not implemented!")
    def __sub__(self, other):
        raise ValueError("For this class it is not implemented!")

    @staticmethod
    def merge_datasets(datasets:list, name:str = 'merged'):
        raise ValueError("For this class it is not implemented!")

    @staticmethod
    def Subtract_datasets(ds1, ds2, name:str = 'subtracted'):
        raise ValueError("For this class it is not implemented!")

    def delete_offline(self):
        for ds in self.datasets:
            ds.delete_offline()

    def load_offline(self, max_memory_GB:float = -5, percent:float = 100):
        for ds in self.datasets:
            ds.load_offline(max_memory_GB, percent)
