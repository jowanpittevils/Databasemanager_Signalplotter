#==================================================#
# Authors: Amir H. Ansari <amirans65.ai@gmail.com> #
# License: BSD (3-clause)                          #
#==================================================#

from abc import ABC
import copy

class Copyable(ABC):
    def copy(self, new_name=None):
        res = copy.deepcopy(self)
        if(new_name is not None):
            res.name = new_name
        return res

    def copy_shallow(self):
        return copy.copy(self)        