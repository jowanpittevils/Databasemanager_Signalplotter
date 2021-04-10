#==================================================#
# Authors: Amir H. Ansari <amirans65.ai@gmail.com> #
# License: BSD (3-clause)                          #
#==================================================#

class ChannelInfo(object):
    def __init__(self, name=None, fs=None, order=None):
        self.name = name
        self.fs = fs
        self.order = order

    def __str__(self):
        return "channel: {}, fs: {}, ind: {})".format(
            self.name,
            self.fs,
            self.order,
        )        
    def __repr__(self):
        return str(self)

    


