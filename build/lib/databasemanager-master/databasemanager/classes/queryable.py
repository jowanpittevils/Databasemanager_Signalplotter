#==================================================#
# Authors: Amir H. Ansari <amirans65.ai@gmail.com> #
# License: BSD (3-clause)                          #
#==================================================#

from abc import ABC, abstractmethod
from databasemanager.classes.copyable import Copyable
from databasemanager.classes.criteria import Criteria
import numpy as np

class Queryable(Copyable, ABC):
 
    @abstractmethod
    def reassign(self):
        pass


    def purify(self, criteria:Criteria):
        ''' This function purifies (filters) the object according to the given criteria and return nothing.
        parameters:
        -----------
        criteria: an object from Criteria to define the purifying actions 

        return
        ------
        None
        '''
        assert(isinstance(criteria, Criteria))
        target_list = self.__find_target(criteria.target_type)
        if(len(target_list)==0):
            raise BaseException('The target_class_type cannot be found in the properties of this class!')
        for countainer_root,found_element in target_list:
            criteria_satisfied = self.__apply_filter(criteria, found_element)
            if(criteria.effect_is_include ^ criteria_satisfied): # include XOR critera 
                found = False
                for i,countainer_list in enumerate(countainer_root[-2::-1]): #end to first excluding the last object which is the found one
                    ind = len(countainer_root)-1-i #index of the next object in countainer_root
                    if(isinstance(countainer_list, list)):
                        countainer_list.remove(countainer_root[ind])
                        found = True
                        break
                if(not found):
                    raise BaseException("Cannot find any list having such an object!")

    def where(self, criteria: Criteria):
        ''' this function apply the filter on a copy of the original object according to the given criteria and return it. the original object is kept unchanged.
        parameters:
        -----------
        criteria: an object from Criteria to define the purifying actions 

        return
        ------
        New filtered object
        '''
        assert(isinstance(criteria, Criteria))
        ds_filtered = self.copy()
        ds_filtered.purify(criteria)
        return ds_filtered

    def take(self, criteria: Criteria):
        ''' this function makes a query on the object properties recursively by the given criteria and return all affected objects.
        parameters:
        -----------
        criteria: an object from Criteria to define the purifying actions

        return
        ------
        list of object from creteria.target_type
        '''
        assert(isinstance(criteria, Criteria))
        target_list = self.__find_target(criteria.target_type)
        if(len(target_list)==0):
            raise BaseException('The target_class_type cannot be found in the properties of this class!')

        res = []
        for _,found_element in target_list:
            criteria_satisfied = self.__apply_filter(criteria, found_element)
            if(not (criteria.effect_is_include ^ criteria_satisfied)): # XNOR critera 
                res.append(found_element)
        return res

    def count(self, criteria: Criteria):
        ''' this function runs the given do_funtion in a for-loop on the results of the queried object. It returns a list of do-function results if it does not return None for all. Otherwise, it returns None.
        parameters:
        -----------
        criteria: an object from Criteria to do the query

        return
        ------
        integer indicating the number of items that could passed the criteria
        '''
        assert(isinstance(criteria, Criteria))
        object_list = self.take(criteria)
        return len(object_list)        

    def foreach(self, criteria: Criteria, do_funtion=None, do_exception_action='error', do_exception_default_value=None):
        ''' this function runs the given do_funtion in a for-loop on the results of the queried object. It returns a list of do-function results if it does not return None for all. Otherwise, it returns None.
        parameters:
        -----------
        criteria: an object from Criteria to do the query
        do_funtion: the fucntion that should be apply on the results of the query. It can return something or None
        do_exception_action: {'error','use_default_value','use_exception_object'} [default: 'error'] (case-insensitive) 
            * 'error': will raise an exception (ValueError type) is do_funtion raises an exception
            * 'use_default_value': will put the given 'do_exception_default_value' value in the final list
            * 'use_exception_object': will put the raised exception object in the final list and does not raise an exception
        do_exception_default_value: [default is None] if do_exception_action is set to 'use_default_value', this value will be put in the returing list 

        return
        ------
        None or list depending on the output of do_funtion
        '''
        assert(isinstance(criteria, Criteria))
        object_list = self.take(criteria)
        res = []
        for obj in object_list:
            try:
                res.append(do_funtion(obj))
            except Exception as err:
                if(do_exception_action == 'use_default_value'):
                    res.append(do_exception_default_value)
                elif(do_exception_action == 'use_exception_object'):
                    res.append(err)
                raise err
        if(all(item is None for item in res)):
            res = None
        return res

    def __apply_filter(self, criteria, check_function_input):
        try:
            if(criteria.check_funtion is None):
                return True
            res = criteria.check_funtion(check_function_input)
            if(isinstance(res, np.bool) or isinstance(res, np.bool_)):
                res = bool(res)
            if(not isinstance(res, bool)):
                raise TypeError('The criteria_funtion must return a boolean result. it is ({}).'.format(type(res)))
            return res
        except:
            if(criteria.exception_action_is_include):
                return criteria.effect_is_include
            elif(criteria.exception_action_is_exclude):
                return criteria.effect_is_exclude
            else:
                raise 
            

    def __find_target(self, target_class_type, root = None): #-> (countainer_list, found_element)
        if(root is None):
            root = []
        if(self in root):# to avoid recursion loop subject->recording->subject
            return None
        root = root + [self]
        
        #finding the target in properties
        target_list = self.__find_specific_type_properties(target_class_type, root)
        for i in range(len(target_list)): #founded targetclass at the end of the root list
            target_list[i] = (target_list[i][0]+[target_list[i][1]], target_list[i][1])
        
        #finding the target recursively in the deeper properties
        if(len(target_list)==0):
            Queryable_list = self.__find_specific_type_properties(Queryable, root)
            for rootList,prop in Queryable_list:
                rec_targets = prop.__find_target(target_class_type, rootList)
                if(rec_targets is not None): # to avoid recursion loop subject->recording->subject
                    found = [le[1] for le in target_list]
                    for elem in rec_targets:
                        if(elem[1] not in found):
                            target_list.append(elem)
                    #target_list.extend(rec_targets)
        return target_list

    def __find_specific_type_properties(self, _type, root):
        res = []
        for _,v in self.__dict__.items():
            if(isinstance(v, _type)):
                res.append((root,v))
            if(isinstance(v, list)):
                for vv in v:
                    if(isinstance(vv, _type)):
                        res.append((root+[v],vv))
        return res

    
