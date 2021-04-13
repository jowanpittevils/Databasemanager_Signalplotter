#==================================================#
# Authors: Amir H. Ansari <amirans65.ai@gmail.com> #
# License: BSD (3-clause)                          #
#==================================================#

from databasemanager.classes.listextension import ListExtension
from databasemanager.classes.channelinfo import ChannelInfo

class ChannelInfoList(ListExtension):
    def __init__(self, liste):
        super().__init__(liste)

    @property
    def fs_common(self):
        '''returns the fs if is equal in all channels; otherwise, None.'''
        return self.similar_in_list('fs')

    def find(self, channel, cannot_find='error'):
        '''
        Find a channel in the list and return it.
        'channel' can be string of the channel name or object of ChannelInfo
        cannot_find: {'error', 'none'} (case-insensitive) defines to raise an exception or return None of the target in not found.
        '''
        res = None
        if(isinstance(channel, ChannelInfo)):
            if(channel in self):
                res = self[self.index(channel)]
        elif(isinstance(channel, str)):
             ch = [ch for ch in self if ch.name == channel]
             if(len(ch)>1):
                raise ValueError('There are more than one channel in the list ({})!'.format(channel))
             elif(len(ch)==1):
                res = ch[0]
        if(res is None):
            cannot_find = cannot_find.lower()
            if(cannot_find == 'error'):
                raise ValueError('the given channel ({}) is not found!'.format(channel))
            elif(cannot_find is None or cannot_find == 'None'):
                return None
            else:
                raise ValueError("the given 'cannot_find' ({}) parameter is not true!".format(cannot_find))
        return res



