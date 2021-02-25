#==================================================#
# Authors: Amir H. Ansari <amirans65.ai@gmail.com> #
# License: BSD (3-clause)                          #
#==================================================#

import numpy as np
from databasemanager.classes.event import Event
from databasemanager.classes.copyable import Copyable
from databasemanager.classes.noneablelist import NoneableList
from databasemanager.labelaggregator import majority_voting

class EventList(Copyable, list):
    def __init__(self, liste:list = []):
        super().__init__(liste)
        if(liste is not None):
            if(len(liste)>0):
                assert(all([isinstance(item, Event) for item in liste]))
                
    @property
    def number_of_events(self):
        return len(self)

    @property
    def has_none_start(self):
        return any([event.start is None for event in self])

    @property
    def has_none_end(self):
        return any([event.end is None for event in self])

    @property
    def has_overlap(self):
        '''It is True if events have overlap together.'''
        if(self.has_none_start or self.has_none_end):
            return True
        sevent = self.sorted()
        starts = np.array([event.start for event in sevent])
        ends = np.array([event.end for event in sevent])
        assert(len(starts) == len(ends))
        for i in range(len(starts)-1):
            if(ends[i] > starts[i+1]):
                return True
        return False

    def sort(self):
        '''Sort the events based on the start time and return nothing'''
        super().sort(key=lambda event: event.start)
        
    def sorted(self):
        '''Sort the events based on the start time one a copy of the list and return it.'''
        res = self.copy_shallow()
        res.sort()
        return res
    

    @staticmethod
    def merge_eventlist(lists:list, duration_threshold_sec:float=1):
        ''' This function take a list of EventList and merge them together taking their annotations overlap into account. 
        This function does not perform any aggregation on the labels. Instead, the events in the returned list has a vectorized label
        merging the labels respectively. The labels can also be previously vectorized by this function.
        Hense, the length of label vector of the returning list equals the summation of lengths of the two label vectors. In case of missing label for some
        events, the label vector takes None for the corresponding annotator.
        It does not change the inputs.
        
        parameter:
        ---------
        
        lists: the list of eventlist to be merged
        duration_threshold_sec: the minimum accepted event duration. After the merging process, the events shorter than
                                this threshold will be deleted.

        return
        ------
        an EventList resulted from the merging process
        
        '''
        if(len(lists)==0):
            return None
        res = lists[0]
        for i in range(1, len(lists)):
            res = EventList.__merge_two_eventlist_time(res,lists[i])
        return res

    @staticmethod
    def __merge_two_eventlist_time(list1, list2, duration_threshold_sec:float=1):
        ''' This function take two EventList lists and merge them together taking their annotations overlap into account. 
        This function does not perform any aggregation on the labels. Instead, the events in the returned list has a vectorized label
        merging the labels of list1 and list2 respectively. The labels of list1 and list2 can also be previously vectorized by this function.
        Hense, the length of label vector of the returning list equals the summation of lengths of the two label vectors. In case of missing label for some
        events, the label vector takes None for the corresponding annotator.
        It does not change the inputs.
        
        parameter:
        ---------
        list1 / list2: the two event lists to be merged
        duration_threshold_sec: the minimum accepted event duration. After the merging process, the events shorter than
                                this threshold will be deleted.

        return
        ------
        an EventList resulted from the merging process
        
        '''
        if(list1.has_none_end or list2.has_none_end):
            raise ValueError("The events with 'None'-end are not supported in merging.")
        if(list1.has_none_start or list2.has_none_start):
            raise ValueError("The events with 'None'-start are not supported in merging.")
        if(list1.has_overlap or list2.has_overlap):
            raise ValueError("The events with intera overlap are not supported in merging.")
        merged = EventList.__merge_two_eventlist_label(list1, list2)
        merged.sort()
        res = EventList()
        while(True):
            if(len(merged)==0):
                break
            current_event = merged[0]
            if(len(merged)==1):
                res.append(current_event)
                break
            next_event = merged[1]
            if(current_event.has_overlap(next_event, False)):
                merged.remove(current_event)
                merged.remove(next_event)
                ls = EventList.__split_event(current_event, next_event)
                current_event = ls[0]
                next_event = ls[-1]
                merged = ls + merged

            res.append(current_event)
            merged.remove(current_event)

        res = EventList([r for r in res if r.duration>=duration_threshold_sec])
        return res

    @staticmethod
    def __split_event0(event1:Event, event2:Event):
        ''' It takes two events and check the overlap. In case of overlap it makes a third event indicating the overlap period. 
        It returns an EventList that has 2 (in case of no overlap) or 3 (in case of overlap) events. The label of the events must
        be previouslu vectorized to None-form (using the 'make_label_list' function). In case of overlap, first copies of event1/2
        are made, then the start/end are corrected, and next added to the returning list.
        It does not change the inputs.
        
        return
        ------
        EvenList object having 2/3 events
        '''
        event1 = event1.copy_shallow()
        event2 = event2.copy_shallow()
        res = EventList()
        if(event1.start > event2.start):
            (event1, event2) = (event2, event1)
        res.append(event1)
        d = event2.start - event1.end
        if(d<0): #has overlap
            newEvent = Event(event2.start, event1.end, EventList.__merge_labels(event1.label, event2.label), None,event1.annotation)
            event1.end = newEvent.start
            event2.start = newEvent.end
            res.append(newEvent)
        res.append(event2)
        return res

    @staticmethod
    def __split_event(event1:Event, event2:Event):
        ''' It takes two events and check the overlap. In case of overlap it makes a third event indicating the overlap period. 
        It returns an EventList that has 2 (in case of no overlap) or 3 (in case of overlap) events. 
        The label of the events must be previouslu vectorized to None-form (using the 'make_label_list' function). In case of overlap, first copies of event1/2
        are made, then the start/end are corrected, and next added to the returning list.
        It does not change the inputs.
        
        return
        ------
        EvenList object having 2/3 events
        '''
        utimes = list(set([event1.start, event1.end, event2.start, event2.end]))
        utimes.sort()
        res = EventList([])
        for i in range(0, len(utimes)-1):
            st = utimes[i]
            en = utimes[i+1]
            lbl1 = EventList._get_label_if_overlap(event1, st,en)
            lbl2 = EventList._get_label_if_overlap(event2, st,en)
            lbl = EventList.__merge_labels(lbl1, lbl2)
            res.append(Event(st, en,lbl,None, event1.annotation))
        return res
    
    @staticmethod
    def _get_label_if_overlap(event:Event, start:float, end:float):
        '''It returns the event label if it has overlap with the given range, otherwise None.'''
        if(event.has_overlap_range(start, end, False)):
            return event.label
        else:
            return None
          


    @staticmethod
    def __merge_labels(label1:list, label2:list):
        '''It merges two vectorized event labels. The None vecros should have no overlap.
           It does not change the inputs.
        '''
        if(label1 is None):
            return label2
        if(label2 is None):
            return label1
            
        N = len(label1)
        assert(N == len(label2))
        res = EventList()
        for i in range(N):
            res.append(EventList.__take_not_None(label1[i],label2[i]))
        return res

    @staticmethod
    def __take_not_None(val1, val2):
        '''It returns any one the values that is not None. If both are not 'None, it returns None.'''
        if(val1 is not None):
            return val1
        else:
            return val2



       
                
    @staticmethod
    def __merge_two_eventlist_label(list1, list2):        
        ''' It take two EventList lists and merge all events together without taking any overlap into account.
        If the labels of any of the input lists have not been vectorized, it will be done here.
        them together taking their annotationsoverlap into account. 
        The length of label vector of the returning list equals the summation of the lengths of two label vectors. In case of missing label for some
        events, the label vector takes None for the corresponding annotator.
        It does not change the inputs. The input lists must have at least one event.

        return
        ------
        an EventList resulted from the merging process. It has not been sorted
        
        '''
        assert(len(list1)>0)
        assert(len(list2)>0)
        list1 = list1.copy_shallow()
        list2 = list2.copy_shallow()
        if(isinstance(list1[0].label,str)):
            l1 = 1
        elif(isinstance(list1[0].label,list)):
            l1 = len(list1[0].label)
        else:
            l1 = 1
        if(isinstance(list2[0].label,str)):
            l2 = 1            
        elif(isinstance(list2[0].label,list)):
            l2 = len(list2[0].label)
        else:
            l2 = 1            
        L = l1+l2
        EventList.__vetorize_label(list1, L, [0,l1])
        EventList.__vetorize_label(list2, L, [l1,L])        
        merged = EventList(list1 + list2)
        return merged

    @staticmethod
    def __vetorize_label(eventlist, label_list_len:int, label_position):
        '''It converts the labels of the eventlist in to a vector while extra elements are None. It is applied directly on the egiven list. 
        Parameters:
        -----------
        eventlist: the list in which the labels should be vectorized
        label_list_len: the output length of the label vector
        label_position: a list (or int) with two numbers indicating the start and end (python end: n+1) index of the vector that correspons to this event.
                        If it is an int it is supposed to tbe [label_position, label_position + 1].
        
        It returns nothing.'''
        if(not isinstance(label_position,list)):
            label_position = NoneableList([label_position, label_position+1])
        for event in eventlist:
            nonelist = NoneableList([None]*label_list_len)
            if(not isinstance(event.label, list)):
                event.label = NoneableList([event.label])
            nonelist[label_position[0]:label_position[1]] = event.label
            event.label = nonelist
            
    
    def aggregate(
                self, 
                label_tied_order:list = None, 
                minimum_duration_threshold_sec:float = 1, 
                confidence_ratio:float = 0, 
                remove_Nones:bool = True,
                combine_equals:bool = True,
                ):
        '''
        This function aggregated all annotations into one using majority voting.

        parameters:
        -----------
        label_tied_order: is a list of label string defining the priority of labels if the aggregation is tied. If it is None, the tied annotations are broken randomly.
        minimum_duration_threshold_sec: the events smaller than this thresholds will be set to None after the aggregation.
        confidence_ratio: the events having less aggrement than this ratio will be set to None after the aggregation.
        remove_Nones: If it is true, the events that have None label after the aggregation, will be removed.
        combine_equals: if it is True, the consecutive labels that are exactly following each other in time domain (end1 == start2) and 
                            having equal labels will be merged together. In this case, their confidences must not be necessarily equal. The confidence of the merged event
                            is resulted from a weighted averaging of the confidences of the two events proportional to their durations.

        return:
        -------
        eventList
        '''
        event_list = majority_voting(self, label_tied_order)
        event_list.set_None_short_events(minimum_duration_threshold_sec)
        event_list.set_None_low_confident_events(confidence_ratio)
        if(combine_equals):
            event_list = event_list.combine_equals()
        if(remove_Nones):
            event_list = event_list.remove_Unknowns()
        return event_list

    def set_None_short_events(self, minimum_duration_threshold_sec:float):
        ''' This function sets the label of the events that are shorter than the given minimum_duration_threshold_sec to None and return nothing.'''
        for event in self:
            if event.duration < minimum_duration_threshold_sec:
                event.label = None
                event.label_confidence = None

    def set_None_low_confident_events(self, confidence_ratio:float):
        ''' This function sets the label of the events that have a confidence less than the given confidence_ratio to None and return nothing.'''
        for event in self:
            if (event.label_confidence is None) or (event.label_confidence < confidence_ratio):
                event.label = None
                event.label_confidence = None        

    def combine_equals(self, ignored_interval:float = 0):
        ''' 
        This function merges the consecutive labels that are exactly following each other in time domain (end1 == start2) 
        and having equal labels. Their confidences must not be necessarily equal. The confidence of the merged event
        is resulted from a weighted averaging of the confidences of the two events proportional to their durations.        
        It does not change the input list, all events will be deep-copied.

        parameters:
        ----------
        ignored_interval: that maximum interval (in seconds) between two equally labelled events that should be ignored to be merged.

        return:
        -------
        eventlist
        '''
        orig_list = self.copy_shallow()
        res = EventList([])
        if(len(orig_list)==0):
            return res
        for i in range(0,len(orig_list)-1):
            if(
                (orig_list[i].label == orig_list[i+1].label) and
                ((orig_list[i].end + ignored_interval) >= orig_list[i+1].start)
                ):
                    orig_list[i+1].start = orig_list[i].start
                    orig_list[i+1].label_confidence = self._get_averaged_confidence(orig_list[i],orig_list[i+1])
            else:
                res.append(orig_list[i])
        res.append(orig_list[-1])
        return res

    @staticmethod
    def _get_averaged_confidence(event1:Event, event2:Event)->float:
        if(event1.label_confidence is None):
            return event2.label_confidence
        if(event2.label_confidence is None):
            return event1.label_confidence

        if(event1.duration == 0 and event2.duration == 0):
            return (event1.label_confidence + event2.label_confidence)/2

        sm = (event1.duration*event1.label_confidence) + (event2.duration*event2.label_confidence)
        dv = (event1.duration + event2.duration)
        return sm / dv

            

    def remove_Unknowns(self, unknown_label:str=None):
        ''' 
        This function removes the events with None label and return the remaining.
        It does not change the input list, but it returns the same events in a new eventList list. So it does not deep-copy.
        '''
        if(unknown_label is not None):
            for event in self:
                if(event.label == unknown_label):
                    event.label = None

        return EventList([event for event in self if (event.label is not None)])
    
    def add_background_label(self, label:str, start:float = 0, end:float = None, annotation=None):
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
        annotation: the annotation object to which the background events belong
        '''
        if(len(self)==0):
            if(end is None):
                raise ValueError("The end is None and there is no event in the list to be set!")
            self.append(Event(start, end, label, None, annotation))
            return
        self.sort()
        if(start is None):
            if(self[0].start is None):
                raise ValueError("The start is None and the first event has a None start!")
            start = self[0].start
        if(end is None):
            if(self[-1].end is None):
                raise ValueError("The end is None and the last event has a None end!")
            end = self[-1].end
        extra = EventList()
        if(start < self[0].start):
            extra.append(Event(start, self[0].start, label, None, annotation))
        if(end > self[-1].end):
            extra.append(Event(self[-1].end, end, label, None, annotation))
        for i in range(0, len(self)-1):
            if(self[i].end < self[i+1].start):
                extra.append(Event(self[i].end, self[i+1].start, label, None, annotation))
        self.extend(extra)
        self.sort()

        

