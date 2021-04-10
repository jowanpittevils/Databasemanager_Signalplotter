#==================================================#
# Authors: Amir H. Ansari <amirans65.ai@gmail.com> #
# License: BSD (3-clause)                          #
#==================================================#

import copy
from databasemanager.classes.saveable import Saveable
from databasemanager.classes.copyable import Copyable
from databasemanager.classes.recording import RecordingBase

class OfflineData(Saveable, Copyable):
    '''
    The current version of this offile data only supports uniform operations. In other words, if different recordings have different operators it does not worlk. Will be fixed later.
    '''
    def __init__(self, data:dict=None, fs:float = None, applied_operations=None):
        if(data is None):
            self.data = {}
        else:
            self.data = data
        if(applied_operations is not None):
            self.applied_operations = [type(op) for op in applied_operations]
        else:
            self.applied_operations = []
        self.fs = fs

    def __len__(self):
        if(self.data is None):
            return 0
        return len(self.data)
    
    @staticmethod
    def _load_offline_one_recording(recording:RecordingBase):
        x = recording.get_data(start=0,stop=None,compensate_filter_shrinking=True,out_of_range='error')
        return {recording.name: x}

    #override
    def copy(self, new_name=None, copy_data_deeply:bool = True):
        if(copy_data_deeply):
            return copy.deepcopy(self)
        else:
            newdata = {}
            if(self.data):
                newdata = self.data.copy()
            newopp = []
            if(self.applied_operations):
                newopp = self.applied_operations.copy()
            res = OfflineData(newdata, self.fs, None)
            res.applied_operations = newopp
            return res

    def has_similar_operators_as(self, obj_compare):
        if((self.applied_operations is None) and (obj_compare.applied_operations is None)):
            return True
        if((self.applied_operations is None) or (obj_compare.applied_operations is None)):
            return False
        for i in range(len(obj_compare.applied_operations)):
            if(self.applied_operations[i] != obj_compare.applied_operations[i]):
                return False
        return True

    def __add__(self, other):
        return self.merge(other)
    def __sub__(self, other):
        return self.subtract(other)

    def merge(self, obj2):
        if(self is None and obj2 is None):
            return None
        if(self is None):
            return obj2.copy(copy_data_deeply=False)
        if(obj2 is None):
            return self.copy(copy_data_deeply=False)
        if(self.fs != obj2.fs):
            raise ValueError('Both objects must have the same fs.')
        if(not self.has_similar_operators_as(obj2)):
            raise ValueError('Both objects must have the same applied_operations lists.')
        res = self.copy(copy_data_deeply=False)
        for k,d in obj2.data.items():
            if(k in res.data):
                print('{} recording already exists in the offline data and is skipped.'.format(k))
            else:
                res.data[k] = d
        return res

    def subtract(self, obj2):
        if(self is None):
            return None
        if(obj2 is None):
            return self.copy(copy_data_deeply=False)
        if(not self.has_similar_operators_as(obj2)):
            raise ValueError('Both objects must have the same applied_operations lists.')
        if(self.fs != obj2.fs):
            raise ValueError('Both objects must have the same fs.')
        res = self.copy(copy_data_deeply=False)
        res.data = { k : v for k,v in res.data.items() if k not in obj2.data.keys()}
        res.applied_operations
        return res
        
    def subtract_recordings(self, recording_names):
        current_names = self.data.keys()
        intersection_names = [n for n in current_names if n not in recording_names]
        return self.intersection_recordings(intersection_names)

    def intersection_recordings(self, recording_names):
        if(recording_names is None):
            recording_names = []
        assert(isinstance(recording_names, list))
        res = self.copy(copy_data_deeply=False)
        res.data = { k : v for k,v in res.data.items() if k in recording_names}
        return res