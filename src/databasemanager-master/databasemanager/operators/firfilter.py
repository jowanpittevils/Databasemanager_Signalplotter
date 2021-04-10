#==================================================#
# Authors: Amir H. Ansari <amirans65.ai@gmail.com> #
# License: BSD (3-clause)                          #
#==================================================#

from scipy.signal import firwin, filtfilt, lfilter
import numpy as np
from databasemanager.operators.filterbase import FilterBase
from databasemanager import numpyextensions as npx

class FIRFilter(FilterBase):
    '''
    Finite impulse response filter.
    cutoffs: bandpass cutoffs frequencies. low pass: [0, f], high pass: [f, fs/2], band-pass: [f1, f2], bond-stop: [0,f1,f2,fs/2]
    N: an ODD number defining the length of the filter coefficients. It has a big impact (almost linear) on the speed. 
    window: fir window type. see scipy.signal.get_window.
    approach= {'filter', 'filtfilt'} (case-insensitive), 'filter' is about 2 times faster than 'filtfilt'
        -- 'filter': only apply the convolution once, but the group/phase delay can be 
                compensated by filtercorrector (or append the filter by append_filter function). 
        -- 'filtfilt': applies left to right and one right to left to not have any delay. 
    e.g. if low freq is not important: (cutoffs=[0, 40], N = 21) (>25Hz are affected) 
    e.g. if low freq is not important: (cutoffs=[0, 40], N = 51) (>35Hz are affected) 
    e.g. if low freq is important to be removed: (cutoffs=[0.5, 40], N = 151) (>38Hz are affected) 
    e.g. if low freq is very important to be removed: (cutoffs=[0.5, 40], N = 255) (>38Hz are affected)  
    output_type: {'valid', 'same'} (case-insensitive) 
        -- same: return the output as the same size of the input. depending on the filter  approach it may have edge distortion. This distortion values are reachable by correction_samples
        -- valid: only returns the output that are valid by filtering. in this case the outputs size is smaller (x.shape - correction_samples) than the input size.
    '''
    
    #override
    def _filter_raw(self, x:np.ndarray):
        if(self.approach == 'filtfilt'):
            y = filtfilt(self.filter_coef, [1], x, self.axis)
        elif(self.approach == 'filter'):
            y = lfilter(self.filter_coef, [1], x, self.axis)
            #compensate the delay: it removes the begining of thefilter signal correspond to the delay ((N-1)/2) 
            # but to speed up, it does not remove the end 
            N0 = y.shape[self.axis]
            gp = self.correction_samples[1]
            N = N0 - gp
            suby = np.delete(y, slice(0,gp), self.axis)
            npx.put_in(y,suby,self.axis,range(0,N))
        else:
            raise TypeError('the given filtering approach is unknown!')
        return y
        
    #override
    @property
    def filter_length(self):
        return len(self.filter_coef)

    #override
    @property
    def correction_samples(self):
        N = self.filter_length
        if(self.approach == 'filtfilt'):
            return (0, 0)
        elif(self.approach == 'filter'):
            return (int((N-1)/2), int((N-1)/2))
        else:
            raise TypeError('the given filtering approach is unknown!')

    #override
    def _init_filter(self):
        if(self.fs is None or self.axis is None):
            raise BaseException('fs or channel_axis is not yet set!!')
        (new_cutoffs, islow_pass, _, _, isband_stop) = self.__get_filter_type(self.cutoffs, self.fs)
        low_stop = islow_pass or isband_stop
        self.filter_coef = firwin(fs=self.fs, numtaps=self.filter_N, cutoff=new_cutoffs, window=self.window, pass_zero=low_stop,)
        
    def __init__(self, cutoffs:list = [0.5,40], N:int = 255, window:str = 'hamming', approach='filter', output_type:str='valid'):
        super().__init__(output_type)
        if(N%2==0):
            raise ValueError('The given N must be an odd number.')
        self.cutoffs = cutoffs
        self.window = window.lower()
        self.filter_N = N
        self.approach = approach.lower()

    #override 
    def serialize_output_params(self):
        return f'{str(type(self))} >> {str(self.cutoffs)}, {self.filter_N}, {self.window}, {self.approach}, {self.output_type}'

    @staticmethod
    def __get_filter_type(cutoffs, fs):
        islow_pass = False
        ishigh_pass = False
        isband_pass = False
        isband_stop = False
        new_cutoffs = []
        if(len(cutoffs) == 2):
            if(cutoffs[0]==0):
                islow_pass = True
                new_cutoffs = cutoffs[1]
            elif(cutoffs[1]==fs/2):
                ishigh_pass = True
                new_cutoffs = cutoffs[0]
            else:
                isband_pass = True
                new_cutoffs = cutoffs
        elif(len(cutoffs) == 4):
            if(cutoffs[0] !=0 or cutoffs[-1]!=(fs/2)):
                raise ValueError("'cutoffs' list is not correct!")
            else:
                isband_stop = True
                new_cutoffs = cutoffs[1:3]
        else:
            raise ValueError("'cutoffs' list is not correct!")
        return (new_cutoffs, islow_pass, ishigh_pass, isband_pass, isband_stop)

    def filter_type_str(self):
        (new_cutoffs, islow_pass, ishigh_pass, isband_pass, isband_stop) = self.__get_filter_type(self.cutoffs, self.fs)
        if(islow_pass):
            _type = 'low-pass'
            _range = str(new_cutoffs)
        elif(ishigh_pass):
            _type = 'high-pass'
            _range = str(new_cutoffs)
        elif(isband_pass):
            _type = 'band-pass'
            _range = "({}-{})".format(str(new_cutoffs[0]),str(new_cutoffs[1]))
        elif(isband_stop):
            _type = 'band-stop'
            _range = "({}-{})".format(str(new_cutoffs[0]),str(new_cutoffs[1]))
        return (_type,_range)
        
    def __str__(self):
        (_type,_range) = self.filter_type_str()
        return "<FIR filter {} {} Hz>".format(_type, _range)


