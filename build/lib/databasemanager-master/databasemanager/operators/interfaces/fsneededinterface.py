#==================================================#
# Authors: Amir H. Ansari <amirans65.ai@gmail.com> #
# License: BSD (3-clause)                          #
#==================================================#

from abc import ABC, abstractmethod

class FsNeededInterface(ABC):
    '''This interface class defines the operators in which their sampeling frequecny (fs) is needed to be set after the initialization. '''
    def __intit__(self):
        pass
    
    @abstractmethod
    def set_fs(self, fs:int):        
        raise BaseException('It is an interface function with no body!!')

        