#==================================================#
# Authors: Amir H. Ansari <amirans65.ai@gmail.com> #
# License: BSD (3-clause)                          #
#==================================================#

import math
from databasemanager.classes.annotation import Annotation
from databasemanager.classes.eventlist import EventList
from databasemanager.classes.event import Event
from databasemanager.classes.copyable import Copyable

class AnnotationList(Copyable, list):
    def __init__(self, liste:list = []):
        super().__init__(liste)
        if(liste is not None):
            if(len(liste)>0):
                assert(all([isinstance(item, Annotation) for item in liste]))


    def merge_events(self, minimum_duration_threshold_sec=1):
        '''
        This function merged the events of all annotations together. Depending the overlaps of the events of different annotators, 
        the events might be split to smaller one. However, the labels will not be aggregated. The events of the resulted annotaion 
        include the labels of all annotators in a list. The order of the list is the same as the order of this AnnotationList object.
        The metadata of the resulted annotation is changed to minimum information. 
        The original annotations are kept unchanged.
        
        parameters:
        ----------
        minimum_duration_threshold_sec: the events smaller than this thresholds will be removed after the aggregation.      

        return
        ------
        annotation
        '''
        if(len(self)==0):
            return None

        res = self[0].copy_shallow()
        res.name = 'merged'
        res.annotator_index = [ann.annotator_index for ann in self]
        res.extrainfo = None
        res.events = EventList.merge_eventlist([ann.events for ann in self], minimum_duration_threshold_sec)
        return res
    
    def keep_only(self, annotation:Annotation = None, index=None):
        '''
        It keeps only one annotation and removes the others from the annotation list 
        by the given 'index' or (exclusive or) 'annotation'
        '''
        assert((annotation is None) ^ (index is None))
        if((annotation is not None) and isinstance(annotation, int)):
            index = annotation
        if(index is not None):
            annotation = self[index]
        self.clear()
        self.append(annotation)

    def aggregate(
                self, 
                label_tied_order:list = None, 
                minimum_duration_threshold_sec:float = 1, 
                confidence_ratio:float = 0, 
                remove_Nones:bool = True,
                combine_equals:bool = True,
                ):
        '''
        This function aggregated all annotations into one using majority voting (MV). 
        e.g. assume: 
                    - [a0] 00-10:a
                    -      10-20:b
                    - [a1] 00-08:a
                    -      08-20:b
                    - [a2] 00-07:a
                    -      07-20:b
                    Then: this function (MV) ->
                    [if combine equals: True]
                    -      00-10:a 
                    -      10-20:b 
                    [if combine equals: False]
                    -      00-07:a 
                    -      07-08:a 
                    -      08-10:b 
                    -      10-20:b 


        parameters:
        -----------
        label_tied_order: is a list of label string defining the priority of labels if the aggregation is tied. If it is None, the tied annotations are broken randomly.
        minimum_duration_threshold_sec: the events smaller than this thresholds will be set to None after the aggregation.
        confidence_ratio: the events having less aggrement than this ratio will be set to None after the aggregation.
        remove_Nones: If it is True, the events that have None label after the aggregation, will be removed.
        combine_equals: if it is True, the consecutive labels that are exactly following each other in time domain (end1 == start2) and 
                            having equal labels will be merged together. In this case, their confidences must not be necessarily equal. The confidence of the merged event
                            is resulted from a weighted averaging of the confidences of the two events proportional to their durations.

        return:
        -------
        annotation
        '''
        res = self.merge_events(0)
        res.events = res.events.aggregate(label_tied_order, minimum_duration_threshold_sec, confidence_ratio, remove_Nones, combine_equals)
        return res

    def add_background_label(self, label:str, start:float = 0, end:float = None):
        ''' 
        It adds events in all intervals (in the given start-end range) where no event was assign by the annotators.
        It can be very usefull in 2-class problems where only one label is annotated (e.g. seizures in seizure detection problems). 
        This functions will sort the events.
        It returns nothing.

        parameters:
        -----------
        label: the label of the background (e.g. non-seizure)
        start: the start of recording that should be logically 0 (unless in some special usecases). If it sets to None, it will be set to the start of the first event.
        end: the end of recording. If it sets to None, it will be set to the end of the last event.
        '''
        for ann in self:
            ann.events.add_background_label(label, start, end, ann)

        