#==================================================#
# Authors: Amir H. Ansari <amirans65.ai@gmail.com> #
# License: BSD (3-clause)                          #
#==================================================#

import glob
from prettytable import PrettyTable
from databasemanager.classes.path import Path
from databasemanager.classes.dataset import Dataset
from databasemanager.settings.usersettings import UserSettings

class Database(object):
    '''
    This class is for organizing the whole the database. Its main function is 'load_dataset' that returns an object of a dataset.
    
    parameters:
    -------------
    root: 
    -   a string to the database folder (relative or absolute path)
    -   or an object of Path class.

    another alternative, when the location of Data and Datasets are different, is:
    root = None (obligatory)
    data_path = ...
    datasets_path = ...

    e.g.
    1) db = Database('c:\\sleep')
    2) db = Database(Path('c:\\sleep')) # Path: from databasemanager.classes.path import Path
    2) db = Database(root = 'c:\\sleep')
    3) db = Database(root = None, data_path = 'c:\\sleep\\Data', datasets_path = 'c:\\sleep\\Datasets')


    '''
    def __init__(self, root: str, data_path: str=None, datasets_path: str=None):
        if(isinstance(root, str)):
            assert((data_path is None) and (datasets_path is None))
            self.path = Path(root)
        elif(isinstance(root, Path)):
            assert((data_path is None) and (datasets_path is None))
            self.path = root
        elif(root is None):
            assert(isinstance(data_path, str) and isinstance(datasets_path, str))
            self.path = Path(root=None, data_path=data_path, datasets_path=datasets_path)
        else:
            raise TypeError(f'root must be a string or a Path object while it is "{type(root)}"!')

    @property        
    def dataset_names(self):
        return self.path.datasets_list_names
    
    def load_dataset(self, dataset_name:str = 'all', channel_names:list = None, verbose:bool = True) -> Dataset:
        '''
        This function loads a dataset by its name and returns a dataset object.
        name: the name of the dataset
        verbose: to show extra information while loading
        channel_names: the name of the channels to be loaded. It then internally sets UserSettings.global_settings().loading_data_channels
        '''
        if(channel_names is not None):
            UserSettings.global_settings().loading_data_channels = channel_names
        return Dataset.load_dataset(self.path, dataset_name, verbose=verbose)
    
    def __len__(self):
        return len(self.dataset_names)
            
    def __str__(self):
        return "<Database object includs {} datasets.".format(len(self))

    def __repr__(self):
        st  = ("="*30 + " Database " + "="*30 + "\n")
        st += ("\n").join(["dataset: "+d for d in self.dataset_names])+ "\n"
        st += ("="*30 + "="*10 + "="*30) + "\n"
        return st
    
    def summary(self):
        print("="*30 + " Database " + "="*30)
        print('#datasets: ' + str(len(self.dataset_names)))
        t = PrettyTable(['Dataset names'])
        non = [t.add_row([dsname]) for dsname in self.dataset_names]
        print(t)
        print("="*30 + "="*10 + "="*30 + "\n"+ "\n")
        
        