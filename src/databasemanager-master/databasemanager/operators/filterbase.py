#==================================================#
# Authors: Amir H. Ansari <amirans65.ai@gmail.com> #
# License: BSD (3-clause)                          #
#==================================================#

import numpy as np
from abc import ABC, abstractmethod, abstractproperty
from databasemanager.operators.operatorbase import OperatorBase
from databasemanager.operators.interfaces.fsneededinterface import FsNeededInterface
from databasemanager.operators.interfaces.timeaxisneededinterface import TimeAxisNeededInterface
from databasemanager.operators.filtercorrector import FilterCorrector

class FilterBase(OperatorBase, FsNeededInterface, TimeAxisNeededInterface, ABC):

    #override from FsNeededInterface.set_fs()
    def set_fs(self, fs):
        self.fs = fs
        if(self.axis is not None):
            self.set_filter()
        
    #override from TimeAxisNeededInterface.set_axis()
    def set_axis(self, axis):
        self.axis = axis
        if(self.fs is not None):
            self.set_filter()
               
    def __init__(self, output_type:str='valid'):
        '''
            output_type: {'valid', 'same'} (case-insensitive) 
                -- same: return the output as the same size of the input. depending on the filter  approach it may have edge distortion. This distortion values are reachable by correction_samples
                -- valid: only returns the output that are valid by filtering. in this case the outputs size is smaller (x.shape - correction_samples) than the input size.
        '''
        self.output_type  = output_type.lower()
        self.corrector = None
        self.axis = None
        self.fs = None

    # override Operation.apply(x)
    def apply(self, x):
        return self.filter(x)

    def filter(self, x:np.ndarray):
        y = self._filter_raw(x)
        if(self.corrector is not None):
            y = self.corrector.apply(y)
        return y

    def set_filter(self):
        self._init_filter()
        if(self.output_type == 'valid'):
            self.corrector = FilterCorrector(self)
            self.corrector.set_axis(self.axis)

    @abstractmethod
    def _filter_raw(self, x:np.ndarray):
        pass
    
    @abstractmethod
    def _init_filter(self):
        pass

    @abstractproperty
    def filter_length(self):
        pass
        