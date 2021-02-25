#==================================================#
# Authors: Amir H. Ansari <amirans65.ai@gmail.com> #
# License: BSD (3-clause)                          #
#==================================================#

from abc import ABC
import pickle

class Saveable(ABC):
    def save_to_file(self, fname:str = 'dataset.ds', save_offline_data:bool = False):
        import sys
        from ..settings.usersettings import UserSettings
        if(not save_offline_data):
            temp_offline_data = self.offline_data
            self.offline_data = {}
        with open(fname, 'wb') as output:
            pickle.dump(self, output)

        if(not save_offline_data):
            self.offline_data = temp_offline_data

    @staticmethod
    def load_from_file( fname:str = 'dataset.ds'):
        with open(fname, 'rb') as data:
            return pickle.load(data)
            

        