#==================================================#
# Authors: Amir H. Ansari <amirans65.ai@gmail.com> #
# License: BSD (3-clause)                          #
#==================================================#

import numpy as np
from databasemanager.operators.operatorbase import OperatorBase
from databasemanager.operators.interfaces.timeaxisneededinterface import TimeAxisNeededInterface

class Shrinker(OperatorBase, TimeAxisNeededInterface):
    #override from AxisNeededInterface.set_axis()
    def set_axis(self, axis):
        self.axis = axis

    #override OperatorBase.correction_samples()
    @property
    def correction_samples(self):
        return(0, 0)
               
    def __init__(self, from_left, from_right):
        '''from_left, from_right: The number of samples that should be removed from the left and right of the inputs.'''
        self.from_left = from_left
        self.from_right = from_right
        self.axis = None

    #override 
    def serialize_output_params(self):
        return f'{str(type(self))} >> {self.from_left}, {self.from_right}'

    # override Operation.apply(x)
    def apply(self, x):
        if(self.axis is None):
            raise BaseException("axis is not yet set!")
        L = x.shape[self.axis]
        stop = L - self.from_right
        return x.take(np.arange(self.from_left,stop),self.axis)

    def __str__(self):
        return "<Shrinker, removes ({}, {}) samples (left, right)>".format(self.from_left, self.from_right)
