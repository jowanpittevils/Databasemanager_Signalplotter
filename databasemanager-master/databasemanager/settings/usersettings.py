#==================================================#
# Authors: Amir H. Ansari <amirans65.ai@gmail.com> #
# License: BSD (3-clause)                          #
#==================================================#

import configparser
import ast
from abc import ABC
from collections import namedtuple
from databasemanager.settings._iusersettings import _iUserSettings

class UserSettings(ABC):
    # singleton pattern
    __global_settings = None
    @classmethod
    def global_settings(cls):
        if(cls.__global_settings is None):
            cls.__global_settings = _iUserSettings()
        return cls.__global_settings
    @classmethod
    def reload(cls):
        cls.global_settings().reload()

    def __init__(self):
        raise BaseException('This is a static class and should not be instantiated. Use UserSettings.global_settings() instead to have access to the singleton settings object.')
    
