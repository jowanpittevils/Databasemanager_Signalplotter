#==================================================#
# Authors: Amir H. Ansari <amirans65.ai@gmail.com> #
# License: BSD (3-clause)                          #
#==================================================#
import copy

class NoneableList(list):
    def get_non_Nones(self):
        '''It returns the items that are not None'''
        return [i for i in self if i is not None]

    def deepcopy(self):
        return copy.deepcopy(self)
