#==================================================#
# Authors: Elisabeth Hereman #
# License: BSD (3-clause)                          #
#==================================================#

from databasemanager.operators.operatorbase import OperatorBase

class Scaler(OperatorBase):
    '''This operator scale the signals with contant scale. e.g. to convert unites (V to uV)'''
    def __init__(self, scale:float=1):
        super().__init__()
        self.scale=scale

    #override 
    def serialize_output_params(self):
        return f'{str(type(self))} >> {self.scale}'

    # override Operation.apply(x)
    def apply(self,x):
        return self.scale * x
    
    @property
    def correction_samples(self):
        return(0, 0) 

    def __str__(self):
        return "<Scaler, scale: {}>".format(self.scale)
