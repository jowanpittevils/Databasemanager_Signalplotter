#==================================================#
# Authors: Amir H. Ansari <amirans65.ai@gmail.com> #
# License: BSD (3-clause)                          #
#==================================================#

from databasemanager.operators.operatorbase import OperatorBase
from databasemanager.operators.filterbase import FilterBase
from databasemanager.operators.filtercorrector import FilterCorrector
from databasemanager.classes.virtuallist import VirtualList

class OperatorList(VirtualList):
    def __init__(self, master_list):
        super().__init__()
        self.init_virtual_list(master_list, OperatorBase)

    def summary(self):
        for op in self:
            print(str(op))
