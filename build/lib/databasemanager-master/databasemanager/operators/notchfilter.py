#==================================================#
# Authors: Amir H. Ansari <amirans65.ai@gmail.com> #
# License: BSD (3-clause)                          #
#==================================================#

import numpy as np
from scipy.signal import butter, filtfilt
from databasemanager.operators.filterbase import FilterBase

class NotchFilter(FilterBase):
    #override
    def _filter_raw(self, x:np.ndarray):
        y = filtfilt(self.filter_coef_b, self.filter_coef_a, x, self.axis)
        return y

    #override
    @property
    def correction_samples(self):
        N = self.filter_length[0]
        return (N, N)
        
    #override
    @property
    def filter_length(self):
        return [len(self.filter_coef_b), len(self.filter_coef_a)]

    #override
    def _init_filter(self):
        if(self.fs is None or self.axis is None):
            raise BaseException('fs or channel_axis is not yet set!!')
        dfs_2 = self.stop_band/2
        fstop = np.array([self.stop_fs - dfs_2, self.stop_fs + dfs_2])
        wn = fstop / (self.fs/2)
        (self.filter_coef_b, self.filter_coef_a) = butter(N=self.N, Wn=wn, btype='bandstop')
       
    def __init__(self, stop_fs:float = 50, stop_band:float = 1, N:int = 2, output_type:str='valid'):
        '''
        stop_fs: the center of the notch filter to be removed in Hz
        stop_band: the band width of the notch at -3db in Hz
        N: order of the filter. the length of b and a will be (2N+1)
        output_type: {'valid', 'same'} (case-insensitive) 
            -- same: return the output as the same size of the input. depending on the filter  approach it may have edge distortion. This distortion values are reachable by correction_samples
            -- valid: only returns the output that are valid by filtering. in this case the outputs size is smaller (x.shape - correction_samples) than the input size.
        '''
        super().__init__(output_type)
        self.stop_fs = stop_fs
        self.stop_band = stop_band
        self.N = N
        self.fs = None
        self.axis = None
        self.filter_coef_b = None
        self.filter_coef_a = None

    #override 
    def serialize_output_params(self):
        return f'{str(type(self))} >> {self.stop_fs}, {self.stop_band}, {self.N}, {self.output_type}'

        
    def __str__(self):
        return "<Notch filter at {} Hz (width: {} Hz)>".format(self.stop_fs, self.stop_band)


    


