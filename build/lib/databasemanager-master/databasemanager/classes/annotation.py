#==================================================#
# Authors: Amir H. Ansari <amirans65.ai@gmail.com> #
# License: BSD (3-clause)                          #
#==================================================#

import mne
import random
import numpy as np
from databasemanager.tsvreader import TSVReader
from databasemanager.classes.path import Path
from databasemanager.classes.event import Event
from databasemanager.classes.annotationextrainfo import AnnotationExtraInfo
from databasemanager.classes.noneablelist import NoneableList
from databasemanager.classes.queryable import Queryable
from databasemanager.classes.eventlist import EventList
from databasemanager.classes.listextension import ListExtension

class Annotation(Queryable):
    
    #override copyabledoubleside
    def reassign(self):
        if(self.events is not None):
            for event in self.events:
                event.annotation = self
                event.reassign()       

    def __init__(self, path, subject_name, file_name, annotator_index):
        if(isinstance(path, Path)):
            self.path = path
        elif(isinstance(path, str)):
            self.path = Path(path)
        else:
            raise BaseException('Path must be a string or an object of Path ({}).'.format(self.name))
        self.name = file_name
        self.annotator_index = annotator_index
        self.subject_name = subject_name
        (event_tsv_list, comments) = TSVReader.read_tsv(self.path.get_annotation_fullpath(subject_name,file_name))
        self.events = EventList([Event.make_event(event_tsv, self) for event_tsv in event_tsv_list])
        self.extrainfo = AnnotationExtraInfo(",".join(comments))
        self.reassign()
        
    def __len__(self):
        if(self.events is None):
            return 0
        return len(self.events)

    @property
    def number_of_events(self):
        return len(self)

    @property
    def has_none_start(self):
        return self.events.has_none_start

    @property
    def has_none_end(self):
        return self.events.has_none_end

    @property
    def has_overlap(self):
        return self.events.has_overlap

    @property
    def unique_labels(self):
        lbls =  ListExtension([event.label for event in self.events])
        return set(lbls)

    def sort_events(self):
        '''Sort the events based on the start time and return nothing'''
        self.events.sort()
        
    def __str__(self):
        return "<Annotation {0} includes {1} events.>".format(self.name, len(self))
    
    def Summary(self):
        print(str(self))

    def remove_Unknowns(self, unknown_label:str=None):
        ''' 
        This function removes the events with None label and return the remaining.
        It does not change the input list, but it returns the same events in a new eventList list. So it does not deep-copy.
        '''
        self.events.remove_Unknowns(unknown_label)

    def add_background_label(self, label:str, start:float = 0, end:float = None):
        ''' 
        It adds events in all intervals (in the given start-end range) where no event was assign by the annotators.
        It can be very usefull in 2-class problems where only one label is annotated (e.g. seizures in seizure detection problems). 
        This functions will sort the events.
        It returns nothing.

        parameters:
        -----------
        label: the label of the background (e.g. non-seizure)
        start: the start of annotation that should be logically 0 (unless in some special usecases). If it sets to None, it will be set to the start of the first event.
        end: the end of annotation. If it sets to None, it will be set to the end of the last event.
        '''
        self.events.add_background_label(label, start, end, self)

    def get_mne_annotations(self):
        ''' returns an mne annotation object.'''
        start = [event.start for event in self.events]
        duration = [event.duration for event in self.events]
        label = [event.label for event in self.events]

        mne_ann = mne.Annotations(start, duration, label)
        return mne_ann
    def add_stop_point(self, point, not_in_range = 'error'):
        '''
        This function gets a point in seconds (from the start), if at that point an event starts or ends, it does nothing.
        Otherwise, it breaks the event including this point into two events with the same label. 
        If the point is not in the range, it does nothing
        e.g. exist: (1-10: QS) -> break at 7 -> (1-7: QS) and (7-10: QS)
        point: the stopping point in seconds
        not_in_range = {'error', 'nothing'} (case-insensitive) defines to raise an exception or do nothing if there is no event including the given stop-point.
        '''
        not_in_range = not_in_range.lower()
        exist = [event for event in self.events if event.start == point or event.end == point]
        if(len(exist)>0):
            return
        events = [event for event in self.events if event.start < point and point < event.end]
        if(len(events)==0):
            if(not_in_range == 'error'):
                raise ValueError('There is no event in the annotation file including the given stop-point. ann: '+self.name)
            else:
                return
        if(self.has_none_end or self.has_none_start):
            raise ValueError('This function does not support unknown start/stop events ({}).'.format(self.name))
        if(len(events)>1):
            raise ValueError('There are more than one event including the given stop-point. This is not supported in this function ({}).'.format(self.name))
        event = events[0]
        ind = self.events.index(event)
        ev2 = Event(point, event.end, event.label, event.extrainfo, event.label_confidence, self)
        event.end = point
        self.events.insert(ind+1, ev2)

    def get_label(self, start, stop, border_case='last'):
        ''' 
        returns all possible labels between the start (in seconds) and stop (in seconds) range.
        start: start time in seconds
        stop: stop time in seconds
        border_case: {'first', 'last', 'random', 'error', 'longest', 'all'} (case-insensitive) defines the strategy if the range has overlap with multiple events:
            -- 'first': return the label at the begining of the range 
            -- 'last': return the label at the end of the range 
            -- 'random': return a random label 
            -- 'error': raise a value error
            -- 'longest': return the longest event. if equal return the last.
            -- 'details_on_borders': only if the range is on the border (has more than 1 label), returns a list of new events describing the labels in the requested range.
                            These start and end of these events are related to the given start (so between 0 and (stop-start)).
                            If it is not on the border it returns a single string.
            -- 'details_all': similar to details_on_borders while it returns also [event(0,stop-start,lbl)] for the ranges that are not on any border.
                                Normaly it is not time-efficent as most of ranges are usually not on borders.
            -- 'all': return a list of all labels
        return the label string or list of strings
        '''
        border_case = border_case.lower()
        assert(border_case in ('first','last','random','error','longest','details_on_borders','details_all','all'))
        lst = []
        for event in self.events:
            if(max(event.start,start) < min(event.end, stop)):
                if(event.label is not None):
                    lst.append(event)
        return self._merge_events_by_border_case(lst, border_case, start, stop)

    def _add_gaps(self, lst, start, stop):
        # make a unique list of all start and stops in the list
        points = list(set([l.start for l in lst] + [l.end for l in lst]))
        assert(None not in points)
        #exclude the points out of the given start-end
        points = [p for p in points if (p >= start and p <= stop)]
        # add start and stop to the points
        points  = list(set(points + [start, stop]))
        points = sorted(points)
        gaps=[]
        for ip in range(1,len(points)):
            ll = [l for l in lst if l.has_overlap_range(points[ip-1], points[ip], False)]
            if(len(ll) == 0): #gap
                gaps.append(Event(points[ip-1], points[ip], None, None, self)) 
        if(len(gaps)>0):
            lst = lst + gaps
            lst.sort(key= lambda e: e.start)
        return lst

    def _merge_events_by_border_case(self, lst, border_case, start, stop):
        '''It takes a list of event and merge them into one event corresponding the given borde_case.'''
        dur = stop - start
        lst = [l for l in lst if (min(l.end, stop) - max(l.start, start)) > 0]
        lst = self._add_gaps(lst, start, stop)
        if(lst is None or len(lst)==0):
            return None
        if(len(lst)==1):
            if(border_case == 'details_all'):
                return [Event(lst[0].start, lst[0].end, lst[0].label, self, lst[0].label_confidence)]
            return lst[0].label
        border_case = border_case.lower()
        if(border_case == 'first'): 
            return lst[0].label
        elif(border_case == 'last'): 
            return lst[-1].label
        elif(border_case == 'random'): 
            return random.choice(lst).label
        elif(border_case == 'error'): 
            raise ValueError('There are more than one label for the given range! ({}).'.format(self.name))
        elif(border_case == 'longest'): #events must be sorted in the annotation file
            if(len(lst)==1):
                return lst[0].label
            durs = [(min(e.end, stop) - max(e.start, start)) for e in lst]
            #durs = [e.duration for e in lst]
            #durs[0] = lst[0].end - max(lst[0].start, start)
            #durs[-1] = min(lst[-1].end, stop) - lst[-1].start
            durs = np.array(durs)
            i = np.argmax(durs)
            return lst[i].label
        elif(border_case == 'details_on_borders' or border_case == 'details_all'):
            res = []
            for i in range (len(lst)):
                e = lst[i]
                st = max(0, e.start - start)
                en = min(dur, e.end - start)
                res.append(Event(st,en,e.label,e.extrainfo, self ,e.label_confidence))
            return res
        else:
            return [l.label for l in lst] #all 

        
    def merge_similar_adjacent_event(self, only_if_extra_infos_are_the_same:bool = False):
        '''
        This function merges the events in which they are consequetive (end of one is exactly the start of the other)
        and merge them together. It first sorts the events.
        parameters:
        ----------
        only_if_extra_infos_are_similar: if it is true, only the events that are adjacent and have exactly the same extra_info (4th column in the annotation file) will be merged (None is equal to None).
        
        Return:
        It returns the deleted events (mainly for debug)
        '''
        L = len(self.events)
        if(L<2):
            return []
        self.sort_events()
        ev_last = self.events[0]
        ev_last.must_be_deleted = False
        for i in range(1,L):
            ev1 = self.events[i]
            ev1.must_be_deleted = False
            if(ev_last.label == ev1.label):
                if(ev_last.end == ev1.start):
                    if((not only_if_extra_infos_are_the_same) or
                            (ev_last.extrainfo.info_text == ev1.extrainfo.info_text)):
                        ev_last.end = ev1.end
                        ev1.must_be_deleted = True
            if(not ev1.must_be_deleted):
                ev_last = ev1
        deleted_events = [e for e in self.events if (hasattr(e,'must_be_deleted') and e.must_be_deleted)]
        self.events = EventList([e for e in self.events if (not hasattr(e,'must_be_deleted') or (not e.must_be_deleted))])
        return deleted_events







  