#==================================================#
# Authors: Amir H. Ansari <amirans65.ai@gmail.com> #
# License: BSD (3-clause)                          #
#==================================================#

import mne
class RawList(list):
    def __init__(self, liste):
        super().__init__(liste)
        if(liste is not None):
            if(len(liste)>0):
                assert(all([isinstance(item, mne.io.BaseRaw) for item in liste]))
        


