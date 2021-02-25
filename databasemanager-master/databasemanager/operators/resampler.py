#==================================================#
# Authors: Amir H. Ansari <amirans65.ai@gmail.com> #
# License: BSD (3-clause)                          #
#==================================================#

import math
from scipy.signal import resample, resample_poly
from databasemanager.operators.operatorbase import OperatorBase
from databasemanager.operators.interfaces.timeaxisneededinterface import TimeAxisNeededInterface
from databasemanager.operators.interfaces.fsneededinterface import FsNeededInterface

class Resampler(OperatorBase, TimeAxisNeededInterface, FsNeededInterface):
    #override from FsNeededInterface.set_fs()
    def set_fs(self, fs):
        self.fs = fs
        self.__ratio = self.fs_new/fs
        self.__needed = (self.fs_new != fs)
        
    #override from TimeAxisNeededInterface.set_axis()
    def set_axis(self, axis):
        self.axis = axis

    #override OperatorBase.correction_samples()
    @property
    def correction_samples(self):
        return(0, 0)
               
    def __init__(self, fs_new, window='hamming', approach:str='poly'):
        '''
        approach: {'poly', 'fft'} (case-insensitive) in both case an FRI filter will be applied.
            -- poly: uses scipy.signal.resample_poly using polyphase filtering (this is a faster approach)
            -- fft: uses scipy.signal.resample using Fourier method            
        '''
        super().__init__()
        self.fs_new = fs_new
        self.window = window
        self.axis = None
        self.fs = None
        self.approach = approach.lower()
        self.__ratio = None
        self.__needed = None

    #override 
    def serialize_output_params(self):
        return f'{str(type(self))} >> {self.fs_new}, {self.window}, {self.approach}'

    # override Operation.apply(x)
    def apply(self, x):
        if(self.fs is None or self.axis is None):
            raise BaseException("fs or axis is not yet set!")
        if(not self.__needed):
            return x
        samp_old = x.shape[self.axis]
        samp_new = int(round(samp_old * self.__ratio))
        if(self.fs == self.fs_new):
            return x
        if(self.approach == 'fft'):
            xx = resample(x, samp_new, axis = self.axis, window=self.window)
        elif(self.approach == 'poly'):
            gcd = math.gcd(int(self.fs_new), int(self.fs))
            up = int(self.fs_new / gcd)
            down = int(self.fs / gcd)
            xx = resample_poly(x, up, down, axis = self.axis, window=self.window)
        else:
            raise ValueError('The given approach is not known!')
        return xx

    def __str__(self):
        return "<Resampler from 'any' to {} Hz>".format(self.fs_new)
