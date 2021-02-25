#==================================================#
# Authors: Amir H. Ansari <amirans65.ai@gmail.com> #
# License: BSD (3-clause)                          #
#==================================================#

import configparser
import ast
from collections import namedtuple

class _iUserSettings(object):
    conf_file = 'config.ini'
    user_section = 'User'
    default_settings = {
                        'loading_data_frequency_type': 'similar',
                        'loading_data_channels': 'None',
                        'loading_data_missing_channel_type': 'None',
                        }
    default_settings_type = {
                        'loading_data_frequency_type': str,
                        'loading_data_channels': list,
                        'loading_data_missing_channel_type': str,
                        }
                        
    def __init__(self):
        self.reload()
        
    def reload(self):
        config = configparser.ConfigParser()
        config.read(self.conf_file)
        if(len(config.sections())==0):
                self.__SaveDefault()  
                config.read(self.conf_file)
        assert(len(config.sections())>0)
        self.__settings = self.__cast_types(config._sections[self.user_section])

        # assing the loaded settings dictionary to the fields of this current settings singleton object
        self.__dict__.update(self.__settings)

    @staticmethod
    def __replaceNone(val):
        if(val.lower() == 'none'):
            return None
        return val

    @classmethod
    def __cast_types(cls, settings):
        for k in settings:
            settings[k] = cls.__replaceNone(settings[k])
            if(settings[k] is not None):
                caster = cls.default_settings_type[k]
                if(caster in [list, dict, tuple, set]):
                    settings[k] = ast.literal_eval(settings[k])
                else:
                    settings[k] = caster(settings[k])
        return settings
                


    def __SaveDefault(self):
            config = configparser.ConfigParser()
            config[self.user_section] = self.default_settings
            with open(self.conf_file, 'w') as configfile:
                    config.write(configfile)  
    

    def __repr__(self):
        return str(self)
    def __str__(self):
        return str(self.__settings)

