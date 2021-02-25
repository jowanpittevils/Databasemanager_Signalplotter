#==================================================#
# Authors: Amir H. Ansari <amirans65.ai@gmail.com> #
# License: BSD (3-clause)                          #
#==================================================#

from databasemanager.classes.channelinfo import ChannelInfo

class EDFChannelInfo(ChannelInfo):
    def __init__(self, name, fs=None, order=None, infile_name=None, infile_fs=None, infile_order=None):
        super().__init__(name, fs, order)
        self.infile_name = infile_name
        self.infile_fs = infile_fs
        self.infile_order = infile_order

    def __str__(self):
        return "channel: {}, fs: {}, order: {}, infile_name: {}, infile_fs: {}, infile_order: {})".format(
            self.name,
            self.fs,
            self.order,
            self.infile_name,
            self.infile_fs,
            self.infile_order,
        )
    def __repr__(self):
        return str(self)     