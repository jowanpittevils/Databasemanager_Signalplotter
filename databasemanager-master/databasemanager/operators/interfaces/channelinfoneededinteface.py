#==================================================#
# Authors: Amir H. Ansari <amirans65.ai@gmail.com> #
# License: BSD (3-clause)                          #
#==================================================#

from abc import ABC, abstractmethod
from databasemanager.classes.channelinfolist import ChannelInfoList

class ChannelInfoNeededInterface(ABC):
    '''This interface class defines the operators in which their channel_info_list is needed to be set after the initialization. '''
    
    @abstractmethod
    def set_channel_info_list(self, channel_info_list:ChannelInfoList):
        raise BaseException('It is an interface function with no body!!')
