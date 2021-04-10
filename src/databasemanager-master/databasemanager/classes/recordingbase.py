 #==================================================#
# Authors: Amir H. Ansari <amirans65.ai@gmail.com> #
# License: BSD (3-clause)                          #
#==================================================#

import numpy as np
from abc import ABC, abstractmethod, abstractproperty
from databasemanager.classes.path import Path
from databasemanager.classes.annotation import Annotation
from databasemanager.classes.annotationlist import AnnotationList
from databasemanager.classes.event import Event
from databasemanager.classes.MNEfetchableinterface import MNEFetchableInterface
from databasemanager.classes.queryable import Queryable
from databasemanager.classes.listextension import ListExtension
#from databasemanager.classes.recordingoperatorlist import RecordingOperatorList
from databasemanager.operators.operatorbase import OperatorBase
from databasemanager.operators.filterbase import FilterBase
from databasemanager.operators.resampler import Resampler
from databasemanager.operators.montagemaker import MontageMaker
from databasemanager.operators.rereferencer import Rereferencer
from databasemanager.operators.interfaces.channelinfoneededinteface import ChannelInfoNeededInterface
from databasemanager.operators.interfaces.channelaxisneededinterface import ChannelAxisNeededInterface
from databasemanager.operators.interfaces.timeaxisneededinterface import TimeAxisNeededInterface
from databasemanager.operators.interfaces.fsneededinterface import FsNeededInterface

class RecordingBase(MNEFetchableInterface, Queryable, ABC):
    channel_axis = 0    
    time_axis = 1
    # should be overrode MNEFetchableInterface.fetch_mne_list()
    def fetch_mne_list(self, set_annotations: bool = True):
        raise BaseException('fetch_mne_list should be overrode in the recording subclasses! rec: {}'.format(self.name))
            
    #override copyabledoubleside
    def reassign(self):
        if(self.annotations is not None):
            for ann in self.annotations:
                ann.recording = self
                ann.reassign()

    def __init__(self, path, subject_name, file_name, file_extension, annotation_list):
        '''
            parameters:
            -----------
            path: an object of Path class or absolute string indicating the database root
            subject_name: the name of the subject
            file_name: the stem name of the recording file name without extension
            file_extension: the extension/suffix of the recording file including the dot
            annotation_list: a zip of annotation file name and annotation index
        '''
        if(isinstance(path, Path)):
            self.path = path
        elif(isinstance(path, str)):
            self.path = Path(path)
        else:
            raise BaseException('Path must be a string or an object of Path. subject name: {}, path: {}'.format(subject_name, str(path)))

        self.type = None
        self.name = file_name
        self.extension = file_extension
        self.subject_name = subject_name
        self.annotations = AnnotationList([Annotation(self.path, subject_name, annotation[0], annotation[1]) for annotation in list(annotation_list)])
        self.__operators = []
        self.reassign()

    @property
    def operators(self):
        return tuple(self.__operators)
        
    def add_operator(self, op:OperatorBase):
        assert(isinstance(op, OperatorBase))
        self.__set_operator_params(op)
        self.__operators.append(op)

    def __set_operator_params(self, op):
        if(isinstance(op, ChannelInfoNeededInterface)):
            op.set_channel_info_list(self.channel_info_list)
        if(isinstance(op, TimeAxisNeededInterface)):
            op.set_axis(self.time_axis)
        if(isinstance(op, ChannelAxisNeededInterface)):
            op.set_axis(self.channel_axis)
        if(isinstance(op, FsNeededInterface)):
            op.set_fs(self.fs_output)    

    @property
    def fullname(self):
        return self.name + self.extension

    @abstractproperty 
    def channels(self):
        return None

    @abstractproperty 
    def fs(self):
        return None
    
    @abstractproperty    
    def duration_samp(self)->int:
        return None

    @property
    def duration(self)->float:
        return self.duration_sec
    @property
    def duration_sec(self)->float:
        if(self.fs is None):
            return None
        return self.duration_samp / self.fs
        
    @abstractproperty
    def channel_info_list(self):
        pass
    
    @abstractmethod
    def get_unprocessed_data(self, start, stop):
        pass

    def get_data(self, start:float = 0, stop:float = None, compensate_filter_shrinking=True, out_of_range:str = 'error', fource_to_load_from_file:bool = False):
        '''
        Load and return the data.
        start: start of data in seconds. If it is negative, it will be set to zero.
        stop: end of data in seconds. If it is greater than the recording duration, it will be set to the recording duration. None means end of recording.
        compensate_filter_shrinking: if it is true, it counts the shrinking samples of all filters in which the output_type was set to 'valid' and compensate the shrinking.
                                    As a result, the output of the output of the get data fits to the given start-stop range. If this range is in the border of the recording, the signal is mirrered to reduce the edge distortion effect.
        out_of_range: {'error', 'fix'} (case-insensitive)
            -- 'error': rase a ValueError exception
            -- 'fix': load and returns as much data as possible in the given range.
        fource_to_load_from_file: if it is true, even if the data is ready in offline list, it loads from the file. 
        '''
        out_of_range = out_of_range.lower()
        if((not fource_to_load_from_file) and self.__can_load_from_offline() and (self.subject.dataset.offline_data.fs is not None)):
            fs = self.subject.dataset.offline_data.fs
        else:
            fs = self.fs
        duration_samp = int(self.duration_sec * fs)

        if(stop is None):
            stop_sample = duration_samp
        else:
            stop_sample = int(stop * fs)
        if(start is None):
            start_sample = 0
        else:
            start_sample = int(start * fs)
        if(start_sample < 0):
            if(out_of_range == 'error'):
                raise ValueError('The given start second is not in the recording range (it is negative)! start: {}, fs: {}, rec: {}'.format(start, fs, self.name))
            else:
                start_sample = 0
        if(stop_sample > duration_samp):
            if(out_of_range == 'error'):
                raise ValueError('The given stop second is not in the recording range (max is {}). stop: {}, fs: {}, rec: {}'.format(self.duration_sec, stop, fs, self.name))
            else:
                stop_sample = duration_samp
        return self._get_data_in_sample(start=start_sample, stop=stop_sample, compensate_filter_shrinking=compensate_filter_shrinking, fource_to_load_from_file = fource_to_load_from_file)

    def __can_load_from_offline(self):
        offline_data = self.subject.dataset.offline_data
        return ((offline_data is not None) and (len(offline_data)>0) and (self.name in offline_data.data))

    def _get_data_in_sample(self, start:int, stop:int, compensate_filter_shrinking:bool = True, fource_to_load_from_file:bool = False):
        '''
        Load and return data, start and stop are in samples.
        start: start of data in samples. If it is negative, it will be set to zero.
        stop: end of data in samples. If it is greater than the recording duration, it will be set to the recording duration.
        compensate_filter_shrinking: counts all shrinking samples in the operator list and load extra sample. 
            Therefore, the output has the duration as espected. if it is in the begining or end of recording it uses the mirror of the signal to compensate.
        fource_to_load_from_file: if it is true, even if the data is ready in offline list, it loads from the file. 
        '''
        if(compensate_filter_shrinking):
            (start, stop, augmented_start, augmented_stop) = self.__compensate_shrinking(start, stop)
        offline_data = self.subject.dataset.offline_data
        if((not fource_to_load_from_file) and self.__can_load_from_offline()):
            x = offline_data.data[self.name][:,start:stop]
        else:
            x = self.get_unprocessed_data(start, stop)

        if(compensate_filter_shrinking and augmented_start>0):
            subx = x[:,0:augmented_start]
            x = np.concatenate((np.flip(subx,1),x),1) #mirror
        if(compensate_filter_shrinking and augmented_stop>0):
            subx = x[:,x.shape[1]-augmented_stop:]
            x = np.concatenate((x,np.flip(subx,1)),1) #mirror

        l = len(self.__operators)
        for i in range(l):
            operator = self.__operators[i]
            if((not fource_to_load_from_file) and self.__can_load_from_offline()):
                if((i < len(offline_data.applied_operations)) and (offline_data.applied_operations[i] == type(operator))):
                    continue
            x = operator.apply(x)
        return x
        
    def __get_after_offline_operators(self):
        '''It returns a list of operators which are not already applied in the oofline data.'''
        ops = self.__operators
        offline_data = self.subject.dataset.offline_data
        res = []
        for i,op in enumerate(ops):
            if((i < len(offline_data.applied_operations)) and (offline_data.applied_operations[i] == type(op))):
                continue
            res.append(op)
        return res

    def __compensate_shrinking(self, start, stop):
        operators = self.__get_after_offline_operators()
        new_start = start
        new_stop = stop
        augmented_start = 0
        augmented_stop = 0
        filters = [f for f in operators if isinstance(f, FilterBase) if f.corrector is not None]
        samp_left = [op.corrector.from_left for op in filters]
        samp_right = [op.corrector.from_right for op in filters]
        if(len(samp_right)>0):
            new_start -= sum(samp_left)
            new_stop += sum(samp_right)
            if(new_start < 0):
                augmented_start = -new_start
                new_start = 0
            if(new_stop > self.duration_samp):
                augmented_stop = new_stop-self.duration_samp
                new_stop = self.duration_samp
        return (new_start, new_stop,augmented_start, augmented_stop)

    @property
    def duration_str(self)->str:
        if(self.duration_sec is None):
            return "None"
        return Event._to_time_format(self.duration_sec)
    
    @property
    def unique_labels(self):
        if(self.annotations is None):
            return None
        lbl = ListExtension()
        non = [lbl.extend_append(ann.unique_labels,'add') for ann in self.annotations]
        return set(lbl)

    def __str__(self):
        return "<Recording {} (type: {}) includes {} annotations>".format(self.name, self.type, len(self.annotations))
    
    def summary(self):
        print(str(self))

    @property
    def number_of_annotations(self):
        return len(self.annotations)

    @property
    def number_of_events(self):
        return sum(ann.number_of_events for ann in self.annotations)

    @abstractproperty
    def number_of_channels(self):
        return None

    @property
    def fs_output(self):
        '''It returns the sampling frequency of the loaded data and can be affected by resampling operators (the last one).'''
        ope = [op for op in self.__operators if isinstance(op, Resampler)]
        if(len(ope)>0):
            return ope[-1].fs_new
        else:
            return self.fs

    @property
    def number_of_channels_output(self):
        '''It returns the number of channels of the loaded data and can be affected by montagmaker operators (the last one).'''
        res = self.number_of_channels
        for op in self.__operators:
            if(isinstance(op, Rereferencer) and op.remove_ref):
                res -= 1
            elif(isinstance(op, MontageMaker)):
                res = len(op.channel_orders)
        return res

    def add_background_label(self, label:str, start:float = 0, end:float = None):
        ''' 
        It adds events in all intervals (in the given start-end range) where no event was assign by the annotators.
        It can be very usefull in 2-class problems where only one label is annotated (e.g. seizures in seizure detection problems). 
        This functions will sort the events.
        It returns nothing.

        parameters:
        -----------
        label: the label of the background (e.g. non-seizure)
        start: the start of recording. If it sets to None, it will be set to the start of the first event.
        end: the end of recording. If it sets to None, it will be set to the end of the last event. If it sets to float('inf'), it will automatically set to the end of recordings.
        '''
        if(end == float('inf')):
            end = self.duration_sec
        self.annotations.add_background_label(label, start, end)

