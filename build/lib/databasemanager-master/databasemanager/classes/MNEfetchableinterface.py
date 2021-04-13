#==================================================#
# Authors: Amir H. Ansari <amirans65.ai@gmail.com> #
# License: BSD (3-clause)                          #
#==================================================#

from abc import ABC

class MNEFetchableInterface(ABC):
    def fetch_mne_list(self, asignAnnotation: bool = True):
        pass

    