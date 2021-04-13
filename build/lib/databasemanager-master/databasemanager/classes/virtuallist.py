#==================================================#
# Authors: Amir H. Ansari <amirans65.ai@gmail.com> #
# License: BSD (3-clause)                          #
#==================================================#
 
import collections
from databasemanager.classes.copyable import Copyable

class VirtualList(collections.MutableSequence):
    '''
    This class behaves exactly like a list while it has no real content. It just calls from its children.
    All children should have the same len. For returning functions this class only uses the first object (len, get, ...)
    But for setting (isert, append, ...) it puts to a;;.
    '''
    def init_virtual_list(self, master_list, object_type):
        if(not isinstance(master_list, collections.MutableSequence)):
            TypeError('This instance should be a subclass from collections.MutableSequence (list, VirtualList).')
        self.master_list = master_list
        self.oktypes = object_type
        assert(issubclass(object_type, Copyable))
        self.list = []
        
    def check(self, v):
        if not isinstance(v, self.oktypes):
            raise TypeError(v)

    def __len__(self): 
        if(len(self.master_list)==0):
            return 0
        return len(self.master_list[0])

    def __getitem__(self, i): 
        if(len(self.master_list)==0):
            return None
        if(i<0):
            i += len(self)
        return self.master_list[0][i]

    def __delitem__(self, i): 
        for item in self.master_list:
            del item[i]

    def __setitem__(self, i, v):
        self.check(v)
        for item in self.master_list:
            item[i] = v.copy()

    def insert(self, i, v):
        self.check(v)
        for item in self.master_list:
            item.insert(i, v.copy())

    def __str__(self):
        if(len(self) == 0):
            return '[]'
        return str(self.master_list[0])

