#==================================================#
# Authors: Amir H. Ansari <amirans65.ai@gmail.com> #
# License: BSD (3-clause)                          #
#==================================================#

import collections
from databasemanager.operators.interfaces.channelaxisneededinterface import ChannelAxisNeededInterface
from databasemanager.operators.interfaces.timeaxisneededinterface import TimeAxisNeededInterface
from databasemanager.operators.interfaces.channelinfoneededinteface import ChannelInfoNeededInterface
from databasemanager.operators.interfaces.fsneededinterface import FsNeededInterface

class RecordingOperatorList(collections.MutableSequence):
    def __init__(self, recording):
        self._inner_list = []
        self.recording = recording

    def __len__(self):
        return len(self._inner_list)

    def __delitem__(self, index):
        del self._inner_list[index]

    def insert(self, index, value):
        self.set_recording_params(value)
        self._inner_list.insert(index, value)

    def __setitem__(self, index, value):
        self.set_recording_params(value)
        self._inner_list[index] = value

    def __getitem__(self, index):
        return self._inner_list[index]
    
    def append(self, value):
        self._inner_list.append(value)

    def set_recording_params(self, item):
        if(isinstance(item, ChannelInfoNeededInterface)):
            item.set_channel_info_list(self.recording.channel_info_list)
        if(isinstance(item, TimeAxisNeededInterface)):
            item.set_axis(self.recording.time_axis)
        if(isinstance(item, ChannelAxisNeededInterface)):
            item.set_axis(self.recording.channel_axis)
        if(isinstance(item, FsNeededInterface)):
            item.set_fs(self.recording.fs_output)
        
