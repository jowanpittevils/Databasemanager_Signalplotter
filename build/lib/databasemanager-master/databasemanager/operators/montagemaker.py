#==================================================#
# Authors: Amir H. Ansari <amirans65.ai@gmail.com> #
# License: BSD (3-clause)                          #
#==================================================#

import numpy as np
from databasemanager import numpyextensions as npx
from databasemanager.operators.operatorbase import OperatorBase
from databasemanager.operators.interfaces.channelinfoneededinteface import ChannelInfoNeededInterface
from databasemanager.operators.interfaces.channelaxisneededinterface import ChannelAxisNeededInterface
from databasemanager.classes.channelinfolist import ChannelInfoList
from databasemanager.classes.channelinfo import ChannelInfo
from databasemanager.settings.usersettings import UserSettings

class MontageMaker(OperatorBase, ChannelInfoNeededInterface, ChannelAxisNeededInterface):
    '''
    This operator converts the output channels to bipolar, monopolar, or a mixture.
    montage: list of tuples of channel names, channel orders, or channelInfo (their combinations are accepted)
            In case that the loading_data_missing_channel_type sets to 'skip' in the settings and the recordings 
            has some missing channels, the missing channels should not be counted in the channel order. In this case using channel name can be a better option.
            the channel names should be the standard names.
            for the mixture the tuple should have one item (ch,), or None as the second channel (ch, None). But (None, ch) is not accepted.
    e.g. bipolar: [('c4','c3'),('fp1','c3')] 
    e.g. bipolar: [(1,3),(2,3)], [(1,2),('c3',5)]
    e.g. monopolar: [('c4',),('fp1',)] 
    e.g. mixture: [('cz',),('c3','c4')] or [('cz', None),('c3','c4')]
    '''
    def __init__(self, montage:list):
        assert(isinstance(montage, list))
        self.montage = montage
        self.channel_orders = None
        for r in self.montage:
            assert(isinstance(r,tuple) or isinstance(r,list))
            assert(len(r)==2 or len(r)==1)


    #override 
    def serialize_output_params(self):
        return f'{str(type(self))} >> {str(self.montage)}'

    #override OperatorBase.correction_samples()
    @property
    def correction_samples(self):
        return (0,0)

    #override
    def set_channel_info_list(self, channel_info_list:ChannelInfoList):
        mcd =  UserSettings.global_settings().loading_data_missing_channel_type
        chil = channel_info_list.deepcopy()
        if((mcd is None) or (mcd == 'skip')):
            chil.sort(key = lambda e:e.order)
            for i,c in enumerate(chil):
                c.order = i

        assert(isinstance(chil, ChannelInfoList))
        channel_orders = []
        for r in self.montage:
            order1 = self.__get_channel_order(r[0], chil)
            if((len(r)==2) and (r[1] is not None)):
                order2 = self.__get_channel_order(r[1], chil)
            else: #monopolar
                order2 = -1
            channel_orders.append((order1, order2))            
        self.channel_orders = channel_orders
        self.max_order = max([val for row in channel_orders for val in row]) # to assert faster

    #override
    def set_axis(self, axis):
        self.axis = axis


    @staticmethod
    def __get_channel_order(channel, channel_info_list):
        '''return the channel order if the channel is the channel name (str), an object of channelInfo, or an int or channel order. If cannot find, raises an exception.'''
        if(isinstance(channel,str)):
            return channel_info_list.find(channel,'error').order
        elif(isinstance(channel,ChannelInfo)):
            return channel_info_list.find(channel.name,'error').order
        elif(isinstance(channel,int)):
            return channel
        else:
            raise ValueError('The given channel is neither str nor channelInfo')
        

    # override Operation.apply(x)
    def apply(self, x:np.ndarray):
        if(self.channel_orders is None):
            raise BaseException("channel_info_list is not yet set!")        
        assert(self.max_order < x.shape[self.axis])
        yshape = list(x.shape)
        yshape[self.axis] = len(self.channel_orders)
        y = np.empty(tuple(yshape))
        for i,r in enumerate(self.channel_orders):
            xx0 = np.take(x, r[0], self.axis)
            if(r[1] > -1):
                xx1 = np.take(x, r[1], self.axis)
            else: #monopolar
                xx1 = 0 
            xx = xx0 - xx1
            npx.put_in(y, xx, self.axis, i)
        return y

    @property
    def channels_str(self):
        return ["-".join(mont) for mont in self.montage]
        
    def __str__(self):
        st = ", ".join(self.channels_str)
        return "<MontageMaker: {}>".format(st)

