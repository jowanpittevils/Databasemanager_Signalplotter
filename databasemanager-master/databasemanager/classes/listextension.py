#==================================================#
# Authors: Amir H. Ansari <amirans65.ai@gmail.com> #
# License: BSD (3-clause)                          #
#==================================================#

from databasemanager.classes.noneablelist import NoneableList

class ListExtension(NoneableList):
    def __init__(self, liste=[]):
        super().__init__(liste)
        
    def similar_in_list(list, attribute_name=None, skip_Nones:bool = False):
        ''' if that attribute of all elements of the list has the same value, this value is returned. 
            Otherwise (+ if the length is zero) None is returned.
        '''
        if(list is None or len(list)==0):
            return None
        if(attribute_name is None):
            ref = list[0]
            sim = [item for item in list if item == ref or (skip_Nones and item is None)]
        else: 
            ref = list[0].__dict__[attribute_name]
            sim = [item for item in list if item.__dict__[attribute_name] == ref  or (skip_Nones and item.__dict__[attribute_name] is None)]
        if(len(sim) == len(list)):
            return ref
        else:
            return None

    def extend_append(self, value, if_None:str = 'add'):
        '''
        This function extends the list with the given value if it is a substance of list; otherwise append it.
        
        parameters:
        -----------
        value: to be added
        if_None: {'error', 'ignore', 'add'} defines the strategy when the given value is None.
        '''
        if(value is None):
            if(if_None.lower() == 'add'):
                self.append(None)
            elif(if_None.lower() == 'error'):
                raise ValueError("The added value cannot be None. If it can, set 'if_None'.")
            else:  # == 'ignore'
                pass
            return                
                
        if(isinstance(value, list)):
            self.extend(value)
        elif(isinstance(value, set)):
            self.extend(value)
        elif(isinstance(value, tuple)):
            self.extend(value)
        else:
            self.append(value)

        