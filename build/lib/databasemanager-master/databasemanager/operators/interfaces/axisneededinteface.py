#==================================================#
# Authors: Amir H. Ansari <amirans65.ai@gmail.com> #
# License: BSD (3-clause)                          #
#==================================================#

from abc import ABC, abstractmethod

class AxisNeededInterface(ABC):
    '''This inteface defines the classed in which an axis (mode) (e.g. channel axis or time axis) should be set after the initialization. '''
    
    @abstractmethod
    def set_axis(self, axis):
        raise BaseException('It is an interface function with no body!!')
        
    
    