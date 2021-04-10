#==================================================#
# Authors: Amir H. Ansari <amirans65.ai@gmail.com> #
# License: BSD (3-clause)                          #
#==================================================#

class Criteria(object):
    '''
    parameters:
    -----------
    * target_type: is a class type that should be searched in the object. 
    This class must be a subclass of Queryable. The input of the check_funtion function 
    is the founded objects from this type one by one.
    * check_funtion: is a function (or lambda). It must take one input (object from the defined target_class_type) 
                    If it is None, it means all targets (= lambda x: True) regardless of the given effect or exception_action.
    and return a boolean.
    * effect: {'include', 'exclude'} [default: 'include'] (case-insensitive), if defines to include or exclude the objects that satisfied the check_funtion.
    * exception_action {'error', 'include', 'exclude'} [default: 'error'] (case-insensitive), defining the action if the check_funtion raises an exception. 
        ** 'error': raises an exception
        ** 'include'/'exclude': the found object raising the exception will be included/excluded
    '''
    def __init__(
                self, 
                target_type,
                check_funtion=None, 
                effect='include', 
                exception_action='error'):
        self.target_type = target_type
        self.check_funtion = check_funtion
        self.effect = effect.lower()
        self.exception_action = exception_action.lower()
        if((not self.effect_is_include) and (not self.effect_is_exclude)):
            raise TypeError("'effect' should be 'include' or 'exclude'.")
        if((not self.exception_action_is_error) and (not self.exception_action_is_include) and (not self.exception_action_is_exclude)):
            raise TypeError("'exception_action' should be 'error', 'include', or 'exclude'.")
    
    @property
    def effect_is_include(self):
        return self.effect=='include'
    @property
    def effect_is_exclude(self):
        return self.effect=='exclude'
    @property
    def exception_action_is_error(self):
        return self.exception_action == 'error'
    @property
    def exception_action_is_include(self):
        return self.exception_action == 'include'
    @property
    def exception_action_is_exclude(self):
        return self.exception_action == 'exclude'
