#==================================================#
# Authors: Amir H. Ansari <amirans65.ai@gmail.com> #
# License: BSD (3-clause)                          #
#==================================================#

from databasemanager import numpyextensions as npx
from databasemanager.operators.montagemaker import MontageMaker
from databasemanager.operators.interfaces.channelinfoneededinteface import ChannelInfoNeededInterface
from databasemanager.classes.channelinfolist import ChannelInfoList

class Rereferencer(MontageMaker):

    #override
    def set_channel_info_list(self, channel_info_list:ChannelInfoList):
        mapper = []
        if(isinstance(self.ref_channel, int)):
            self.ref_channel = channel_info_list[self.ref_channel]
        for ch in channel_info_list:
            mapper.append((ch, self.ref_channel))
        self.remove_ref_index = channel_info_list.find(self.ref_channel, 'error').order
        self.montage = mapper
        super().set_channel_info_list(channel_info_list)

    #override OperatorBase.correction_samples()
    @property
    def correction_samples(self):
        return(0, 0)

    def __init__(self, ref_channel, remove_ref:bool = True):
        '''
        ref_channel: can be channel name, order, or channelInfo object
        remove_ref: if it is true, the referenced channel, which are all zeros after rereferencing, will be removed after apply function.
        '''        
        self.ref_channel = ref_channel
        self.remove_ref = remove_ref
        self.remove_ref_index = None
        self.axis = None

    #override 
    def serialize_output_params(self):
        return f'{str(type(self))} >> {self.ref_channel}, {self.remove_ref}'


    # override Operation.apply(x)
    def apply(self, x):
        if(self.remove_ref_index is None or self.axis is None):
            raise BaseException("axis or channel_info_list is not yet set!")      
        x = super().apply(x)
        if(self.remove_ref):
            x = npx.exclude_in(x, self.axis, self.remove_ref_index)
        return x

    def __str__(self):
        return "<Rereferencer, new ref: {}>".format(self.ref_channel)
