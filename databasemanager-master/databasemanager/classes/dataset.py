#==================================================#
# Authors: Amir H. Ansari <amirans65.ai@gmail.com> #
# License: BSD (3-clause)                          #
#==================================================#

import gc
import copy
from tqdm import tqdm
from prettytable import PrettyTable
from psutil import virtual_memory
from databasemanager.tsvreader import TSVReader
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
from databasemanager.classes.saveable import Saveable
from databasemanager.classes.offlinedata import OfflineData
from databasemanager.classes.annotation import Annotation


class Dataset(MNEFetchableInterface, Queryable, Saveable):
    # override MNEFetchableInterface.fetch_mne_list()
    def fetch_mne_list(self, set_annotations: bool = True):
        mne_list = []
        temp_none = [mne_list.extend(subject.fetch_mne_list(set_annotations)) for subject in self.subjects]
        return mne_list
    
    #override
    def copy(self, new_name:str = None, deep_copy_offline_data:bool = False, deep_copy_elements:bool = True):
        '''
        This function make a deep copy from the dataset and return a new object of dataset.
        new_name: the new name of the dataset. If None, it copies from the source.
        deep_copy_offline_data: if it is True, it copy (deeply) all loaded offline data!! 
        deep_copy_elements: if it is True, the enitre database (apart from the offline data that should be set by 'deep_copy_offline_data') will be copied
                            and there will be no connections between the original and the copied datasets. If it is false, only the first level attributes will be copied (shallow copying) and the deeper levels (Subjects, events, etc.) are the same.
        '''
        if(not deep_copy_offline_data):
            temp_offline_data = self.offline_data
            self.offline_data = OfflineData()
        if(deep_copy_elements):
            res = copy.deepcopy(self)
        else:
            res = copy.copy(self)

        if(not deep_copy_offline_data):
            self.offline_data = OfflineData(
                                    temp_offline_data.data, 
                                    temp_offline_data.fs, 
                                    None)
            self.offline_data.applied_operations = copy.deepcopy(temp_offline_data.applied_operations)
            res.offline_data = self.offline_data
            del temp_offline_data

        if(new_name is not None):
            res.name = new_name
        return res

            
    #override copyabledoubleside
    def reassign(self):
        for sub in self.subjects:
            sub.dataset = self
            sub.reassign()

    def __init__(self, path: Path, name: str, subjects: list, comments: str = None):
        self.path = Path._get_path(path)
        self.name = name
        self.subjects = subjects
        self.offline_data = OfflineData()
        if(comments is None):
            comments = ""
        self.comments = comments
        self.delete_offline()
        self.reassign()

    def add_operator(self, op:OperatorBase):
        '''
        It gets an operator and assigns it to all of its subjects.
        '''
        assert(isinstance(op, OperatorBase))
        for s in self.subjects:
            s.add_operator(op.copy())
        
    @staticmethod
    def load_dataset(path, name:str = 'all', verbose:bool = True):
        '''
        This function load the given dataset and returns a dataset object.
        name: the name of the dataset
        verbose: to show extra information while loading
        '''
        path = Path._get_path(path)
        dspath = path.get_dataset_fullpath(name)
        if(name.lower() == 'all'):
            subject_names = path.get_all_subject_names()
            comments = ''
        else:
            subject_names,comments = TSVReader.read_rows(dspath, True)
            subject_names = Dataset.__find_subject_names_reqursively(path, subject_names)

        subjects = []
        if(verbose):
            subject_names = tqdm(subject_names)
        for i,subject_name in enumerate(subject_names):
            subjects.append(Subject(path, subject_name))
#                print('{} out of {}) {} is loaded. '.format(i,len(subject_names), subject_name))

        return Dataset(path, name, subjects, comments)

    def find_recording(self, recording_name, case_sensitive:bool = False):
        '''This function gets a recording name and returns the corresponding recording object, if it is found; otherwise, returns None.'''
        if(case_sensitive):
            recording_name = recording_name.lower()
        for s in self.subjects:
            for r in s.recordings:
                n = r.name
                if(case_sensitive):
                    n = n.lower()
                if(n==recording_name):
                    return r
        return None

    @staticmethod
    def __find_subject_names_reqursively(path, init_name_list):
        all_names = []
        for name in init_name_list:
            if(Dataset.exist(path, name)):
                dspath = path.get_dataset_fullpath(name)
                names,_ = TSVReader.read_rows(dspath, True)
                all_names.extend(Dataset.__find_subject_names_reqursively(path, names))
            else:
                all_names.append(name)
        return Dataset.__remove_repeated_from_last(all_names)

    @staticmethod
    def __remove_repeated_from_last(searching_list):
        res = []
        for item in searching_list:
            if(item not in res):
                res.append(item)
        return res

    @staticmethod
    def exist(path, name):
        return (name in path.datasets_list_names)

    def __len__(self):
        if(self.subjects is None):
            return 0
        return len(self.subjects)
    
    @property
    def subject_names(self):
        res = []
        if(self.subjects is None):
            return res
        return [s.name for s in self.subjects]

    @property
    def number_of_subjects(self):
        return len(self)

    @property
    def number_of_recordings(self):
        return sum(sub.number_of_recordings for sub in self.subjects)

    @property
    def number_of_annotations(self):
        return sum(sub.number_of_annotations for sub in self.subjects)

    @property
    def number_of_events(self):
        return sum(sub.number_of_events for sub in self.subjects)

    @property
    def fs(self):
        fs = ListExtension([sub.fs for sub in self.subjects])
        return fs.similar_in_list()

    @property
    def fs_output(self):
        '''It returns the sampling frequency of the loaded data and can be affected by resampling operators (the last one).'''
        fs_output = ListExtension([sub.fs_output for sub in self.subjects])
        return fs_output.similar_in_list()

    @property
    def number_of_channels_output(self):
        '''It returns the number of channels of the loaded data and can be affected by montagmaker operators (the last one).'''
        res = ListExtension([sub.number_of_channels_output for sub in self.subjects])
        return res.similar_in_list()

    @property
    def duration_sec(self)->float:
        dur_sec = [sub.duration_sec for sub in self.subjects]
        return sum(dur_sec)
    
    @property
    def number_of_channels(self):
        ch = ListExtension([sub.number_of_channels for sub in self.subjects])
        return ch.similar_in_list()

    @property
    def unique_labels(self):
        if(self.subjects is None):
            return None
        lbl = ListExtension()
        non = [lbl.extend_append(sub.unique_labels,'add') for sub in self.subjects]
        return set(lbl)

    def __str__(self):
        ss = ""
        if(len(self)>0):
            ss = ": " + ",".join(str(sub.name) for sub in self.subjects)
        MAXLEN = 50
        if(len(ss)>MAXLEN):
            ss = ss[0:MAXLEN] + "..."
        return "<dataset {0} includs {1} subjects{2}>".format(self.name, len(self), ss)
    
    def __repr__(self):
        line_len = 50
        title = " Dataset "
        left_line_len = (line_len-len(title))//2
        ss = "="*left_line_len + title + "="*(line_len-left_line_len-len(title)) + "\n"
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

    @property
    def operators(self):
        NonuniformRes = '<<Non-uniform operators>>'
        recs = self.take(Criteria(RecordingBase))
        opsList = [op.operators for op in recs]
        refOps = opsList[0]
        for i in range(1,len(opsList)):
            ops = opsList[i]
            if(len(ops) != len(refOps)):
                return NonuniformRes
            for j in range(len(ops)):
                if(not(ops[j].equals(refOps[j], True))):
                    return NonuniformRes
        return refOps


    def show_all_operators(self):
        ops = self.operators
        if(isinstance(ops, str)):
            print(ops)
        else:
            for o in ops:
                print(str(o))

    def summary(self):
        print(repr(self))
        t = PrettyTable(['#','Subject', '#Rec', '#Events', '#Dur (h)'])
        for i,subject in enumerate(self.subjects):
            non = t.add_row([str(i),subject.name, str(subject.number_of_recordings), str(subject.number_of_events), str(round(subject.duration_sec/3600,1))])
        print(t)
        print("\nApplying Operations:")
        self.show_all_operators()
        print("="*50 + "\n")

        
    def __add__(self, other):
        return Dataset.merge_datasets([self, other])
    def __sub__(self, other):
        return Dataset.Subtract_datasets(self, other)

    @staticmethod
    def merge_datasets(datasets:list, name:str = 'merged'):
        if(len(datasets)==0):
            return None
        subjects = []
        for dataset in datasets:
            for sub in dataset.subjects:
                if(sub.name not in [s.name for s in subjects]):
                    subjects.append(sub)
                else:
                    print('{} subject already exists. It is skipped in merging.'.format(sub.name))
        ds = Dataset(datasets[0].path, name, subjects)

        ds.offline_data = None
        for dataset in datasets:
            if(ds.offline_data and dataset.offline_data):
                ds.offline_data = ds.offline_data + dataset.offline_data
            elif(dataset.offline_data):
                ds.offline_data = dataset.offline_data
        return ds

    @staticmethod
    def Subtract_datasets(ds1, ds2, name:str = 'subtracted'):
        snames = ds2.subject_names
        subjects = [s for s in ds1.subjects if s.name not in snames] 
        ds = Dataset(ds1.path, name, subjects)
        ds.offline_data = ds1.offline_data - ds2.offline_data
        return ds

    @staticmethod
    def memory_usage_psutil():
        ''' return the (memory usage, memory available, totam memory) in GB'''
        mem = virtual_memory()
        toGig = (2**30)
        return (mem.used/toGig, mem.available/toGig, mem.total/toGig)
        
    def delete_offline(self):
        '''It removes all loaded offline recordings if there are.'''
        self.offline_data = OfflineData()
        gc.collect()

    @staticmethod
    def __par_offload(rec):
        x = rec.get_data(start=0,stop=None,compensate_filter_shrinking=False,out_of_range='error')
        return {rec: x}


  

    def load_offline(self, max_memory_GB:float = -5, percent:float = 100):
        '''
        This function load some or all of the recordings and keep them to speed up the later call of the 'get_data' function. 
        If it calles multiple time, the loaded recordings will not be reloaded (it resumes). to reset it call 'delete_offline()'.
        
        parameters:
        -----------
        max_memory_GB: (in Gigabytes)
            -- if it is possitive, it defines the maximum phisical memory that should occupied at the loading time. when it is reached, the loading will be stopped.
            -- if it is negative, it means the minimum avail able memory. e.g. -5 means loading continues as long as 5GB of RAM is free.
            -- None or 0 means no limitation
        percent: (e.g. 100, 50, 20) defines the number (/total) of recordings to be loaded. e.g. 50% means halve of the recordings will be loaded.
        '''
        if(percent is None):
            percent = 100
        rec_list = self.take(Criteria(RecordingBase, lambda x:True))
        N = len(rec_list)
        if(max_memory_GB is not None):
            (used, _, total) = self.memory_usage_psutil()
            if(max_memory_GB <= 0):
                th_mem = total + max_memory_GB #= total-(-max_memory_GB)
            else:
                th_mem = max_memory_GB
        data = self.offline_data.data
        for i,rec in enumerate(tqdm(rec_list)):
            gc.collect()
            perc = int(i*100/N)
            if(rec.name in data.keys()):
                continue
            if(max_memory_GB is not None):
                (used, _, _) = self.memory_usage_psutil()
                if(used >= th_mem):
                    print('Stopped loading due to the memory threshold.')
                    break
            if(perc > percent):
                print('Stopped loading due to the percent threshold.')
                break
            data.update(OfflineData._load_offline_one_recording(rec))
        self.offline_data = OfflineData(data, self.fs_output, self.operators)
        print('Offline loading is done. {} recordings are ready to be used in offline mode.'.format(len(self.offline_data)))

    def intersect_subjects(self, subject_names:list):
        '''
        This function keeps only the intersection of the dataset subjects and given subject names exist.
        The rest of subjects will be removed from the dataset and its loaded offline_data.
        It returns nothing.
        '''
        self.subjects = [s for s in self.subjects if s.name in subject_names]
        self.reassign()
        recording_names = self.foreach(Criteria(RecordingBase), lambda r: r.name)
        if(self.offline_data is not None):
            self.offline_data = self.offline_data.intersection_recordings(recording_names)


    def merge_similar_adjacent_event(self, only_if_extra_infos_are_the_same:bool = False):
        '''
        This function merges all the events in which they are consequetive (end of one is exactly the start of the other)
        and merge them together. It first sorts the events.
        parameters:
        ----------
        only_if_extra_infos_are_similar: if it is true, only the events that are adjacent and have exactly the same extra_info (4th column in the annotation file) will be merged (None is equal to None).

        return:
        the total number of removed events
        '''
        r = self.foreach(Criteria(Annotation),lambda a: len(a.merge_similar_adjacent_event(only_if_extra_infos_are_the_same)))
        return sum(r)

    def add_background_label(self, label:str):
        ''' 
        It adds events in all intervals where no event was assign by the annotators.
        Th intervals start from the beginning till the end of each recording. 
        e.g. in a recording with length of 100s. [(10,50,'AAA')] -> [(0,10,'bck'),(10,50,'AAA'),(50,100,'bck')]
        It can be very usefull in 2-class problems where only one label is annotated (e.g. seizures detection). 
        This functions will sort the events.
        It returns nothing.

        parameters:
        -----------
        label: the label of the background (e.g. non-seizure)
        '''
        recs = self.take(Criteria(RecordingBase))
        for r in recs:
            r.add_background_label(label=label, start=0, end=r.duration)
