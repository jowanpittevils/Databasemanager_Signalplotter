#==================================================#
# Authors: Amir H. Ansari <amirans65.ai@gmail.com> #
# License: BSD (3-clause)                          #
#==================================================#

from abc import ABC, abstractmethod, abstractproperty
from databasemanager.classes.copyable import Copyable

class OperatorBase(Copyable, ABC):

    @abstractproperty
    def apply(self, x):
        '''
        This main function that should be overrode by the subclasses to perform the operation.
        '''
        pass

    @abstractproperty
    def correction_samples(self):
        '''
        defined the number of extra samples needed in start and end of signal to correct bourder distortion effect.
        It must be a tuple with two elements. e.g. (100,0). For filtfilt approaches, they should be the same. In FIR filters it should be w/2 where w is the fir filter length.
        '''
        pass

    def serialize(self):
        '''
        This function is for serializing the operator to a string. This will be used to check the equality of two similar operators (e.g. Resampler(10) == Resampler(10))
        By default it makes a string version of internal dictionary.
        '''
        return f'{str(type(self))} >> {str(self.__dict__)}'
        

    def __eq__(self, other):
        return self.serialize().lower() == other.serialize().lower()

    def equals(self, other, general_effect:bool=False):
        '''
        This function check the equality of two operators.
        If general_effect is False, it compares all details of the two operations (with serialise()))
        If it is True, it only checks the general effect of the operators. For instance two Resampler(fs=30) are equal even if there input fs are different.
        '''
        if(general_effect):
            return self.serialize_output_params().lower() == other.serialize_output_params().lower()
        else:
            return self.serialize().lower() == other.serialize().lower()

    @abstractmethod
    def serialize_output_params(self):
        '''
        It serialises the parameters which define the outputs of the operators.
        For instance in Resampler(fs=30), the input fs (e.g. 250Hz) will not be serialized.
        '''
        pass
