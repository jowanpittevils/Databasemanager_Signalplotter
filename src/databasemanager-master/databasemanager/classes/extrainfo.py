#==================================================#
# Authors: Amir H. Ansari <amirans65.ai@gmail.com> #
# License: BSD (3-clause)                          #
#==================================================#

import re
from databasemanager.classes.queryable import Queryable

class ExtraInfo(Queryable):
    _info_separators = [',','\n']
    _dict_separator = ':'
    _hashtag = '#'

    #override copyabledoubleside
    def reassign(self):
        pass
    
    def __init__(self, info_text:str):
        self.comments=[]
        self.info_text = info_text.strip()
        re_spliter = '|'.join(self._info_separators)
        strlist = re.split(re_spliter,info_text)
        dict_info = {}
        for s in strlist:
            s = s.strip()
            if(len(s)==0):
                continue
            if(s[0] is self._hashtag):
                s = s[1:]
            ss = s.split(self._dict_separator)
            if(len(ss)==1):
                s = s.strip()
                self.comments.append(s)
            else:
                if(len(ss)>2): # take the first as the key and join the rest
                    ss[1] =  self._dict_separator.join(ss[1:])
                    ss=ss[0:2]
                if(self.__check_new_key(ss[0])):
                    ss[0] = ss[0].strip()
                    ss[1] = ss[1].strip()
                    dict_info.update({ss[0]:ss[1]})
                else:
                    raise BaseException('Bad format! The used key is researved in python. Please change it in the extra info: ({})'.format(ss[0]))
        self.__dict__.update(dict_info)

    def __check_new_key(self, key):
        return key not in self.__dict__.keys()

    def keys(self):
        ls = list(self.__dict__.keys())
        ls.remove('comments')
        ls.remove('info_text')
        return ls

    def __getitem__(self, key):
        if(key in self.__dict__.keys()):
            return self.__dict__[key]
        else:
            return None
    def __setitem__(self, key, value):
        self.__dict__.update({key: value})

    def __str__(self):
        return "<Extrainfo: {}>".format(list(self.__dict__.keys()))

        
