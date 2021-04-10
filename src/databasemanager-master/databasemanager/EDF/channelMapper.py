#==================================================#
# Authors: Amir H. Ansari <amirans65.ai@gmail.com> #
# License: BSD (3-clause)                          #
#==================================================#

import configparser
import ast

#%%
class mapper(object):
        conf_file = 'edf.ini'
        electrode_names_section = 'electrodenames'
        default_channel_names = {
                        'fp1':['eeg fp1','fp1', 'fp1-ref', 'eeg fp1-ref'],                                
                        'fp2' : ['eeg fp2','fp2', 'fp2-ref', 'eeg fp2-ref'],
                        'f3':['eeg f3','f3', 'f3-ref', 'eeg f3-ref'],                                
                        'f4' : ['eeg f4','f4', 'f4-ref', 'eeg f4-ref'],
                        'p3':['eeg p3','p3', 'p3-ref', 'eeg p3-ref'],                                
                        'p4' : ['eeg p4','p4', 'p4-ref', 'eeg p4-ref'],
                        'c3' : ['eeg c3','c3','c3-ref', 'eeg c3-ref'],
                        'c4' : ['eeg c4','c4','c4-ref', 'eeg c4-ref'],
                        't1' : ['eeg t1','t1','t1-ref', 'eeg t1-ref'],
                        't2' : ['eeg t2','t2','t2-ref', 'eeg t2-ref'],
                        't3' : ['eeg t3','t3','t3-ref', 'eeg t3-ref'],
                        't4' : ['eeg t4','t4','t4-ref', 'eeg t4-ref'],
                        't5' : ['eeg t5','t5','t5-ref', 'eeg t5-ref'],
                        't6' : ['eeg t6','t6','t6-ref', 'eeg t6-ref'],
                        'o1' : ['eeg o1','o1','o1-ref', 'eeg o1-ref'],
                        'o2' : ['eeg o2','o2','o2-ref', 'eeg o2-ref'],
                        'a1' : ['eeg a1','a1','a1-ref', 'eeg a1-ref'],
                        'a2' : ['eeg a2','a2','a2-ref', 'eeg a2-ref'],
                        'f7':['eeg f7','f7', 'f7-ref', 'eeg f7-ref'],                                
                        'f8':['eeg f8','f8', 'f8-ref', 'eeg f8-ref'],                                
                        'fz' : ['eeg fz','fz','fz-ref', 'eeg fz-ref'],
                        'cz' : ['eeg cz','cz','cz-ref', 'eeg cz-ref'],
                        'pz' : ['eeg pz','pz','pz-ref', 'eeg pz-ref'],
                        'ecg' : ['ecg','ii'],
                        'emg' : ['emg chin','emg emg chin'],
                        'resp' : ['thorax','resp thorax'],
                        'sao2' : ['sao2','sao2 sao2','spo','sao2 spo','sao2 spo.'],
                        'eogl' : ['loc','eog loc'],
                        'eogr' : ['roc','eog roc'],
                        'pulse' : ['sao2 pulse']
                }
                
        electrode_type_section = 'electrodetypes'
        default_channel_type = {
                        'eeg': ['fp1',
                                'fp2',
                                'f3',
                                'f4',
                                'p3',
                                'p4',
                                'c3',
                                'c4',
                                't1',
                                't2',
                                't3',
                                't4',
                                't5',
                                't6',
                                'o1',
                                'o2',
                                'f7',
                                'f8',
                                'fz',
                                'cz',
                                'pz',
                                ],
                        'ecg': ['ecg'],
                        'resp': ['ecg'],
                }

        
        def __init__(self):
                config = configparser.ConfigParser()
                config.read(mapper.conf_file)
                if(len(config.sections())==0):
                        self.__SaveDefault()  
                        config.read(mapper.conf_file)
                assert(len(config.sections())>0)
                self.channel_dict = self.__translate_dict_config(config._sections[mapper.electrode_names_section])
                self.type_dict = self.__translate_dict_config(config._sections[mapper.electrode_type_section])
                
        def get_standard_channels(self):
                return list(self.channel_dict.keys())

        def __translate_dict_config(self, configSection):
                res = dict()
                for k,v in configSection.items():
                        vv = ast.literal_eval(v)
                        res.update({k:vv})
                return res


        def __SaveDefault(self):
                config = configparser.ConfigParser()
                config[mapper.electrode_names_section] = mapper.default_channel_names
                config[mapper.electrode_type_section] = mapper.default_channel_type
                with open(mapper.conf_file, 'w') as configfile:
                        config.write(configfile)                

        def is_standard_key(self, key):
                key = key.lower()
                return key in self.channel_dict.keys()
        
        def find_matched_standard_key(self, channel_name):
                channel_name = channel_name.lower()
                for ks,vs in self.channel_dict.items():
                        if(len([k for k in vs if k == channel_name])>0):
                                return ks
                return None
                                
        def get_channels_by_type(self, _type):
                if(_type is None):
                        return None
                if(isinstance(_type,list)):
                        return None
                _type = _type.lower()
                if(_type in self.type_dict.keys()):
                        return self.type_dict[_type]
                return None



# %%
