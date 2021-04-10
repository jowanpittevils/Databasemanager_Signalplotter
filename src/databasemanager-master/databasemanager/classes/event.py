#==================================================#
# Authors: Amir H. Ansari <amirans65.ai@gmail.com> #
# License: BSD (3-clause)                          #
#==================================================#

from databasemanager.classes.queryable import Queryable
from databasemanager.classes.eventextrainfo import EventExtraInfo
import math

class Event(Queryable):
    
    #override copyabledoubleside
    def reassign(self):
        pass

    ''' Start, End, and Durations are in seconds but can be a float including ms.'''
    _time_splitter = ':'
    def __init__(self, start, end, label, extrainfo, annotation, label_confidence=1):
        self.start = start
        self.end = end
        self.label = label
        self.label_confidence = label_confidence
        self.extrainfo = extrainfo
        self.annotation = annotation
        self.reassign()
        
    @property
    def stop(self):
        return self.end
        
    @property
    def duration(self):
        if(self.start is None):
            return -math.inf
        if(self.end is None):
            return math.inf
        return self.end - self.start

    @property
    def start_time(self):
        if(self.start is None):
            return 'None'
        return Event._to_time_format(self.start)
    @property
    def end_time(self):
        if(self.end is None):
            return 'None'
        return Event._to_time_format(self.end)
    @property
    def duration_time(self):
        if(self.start is None):
            return 'inf'
        if(self.end is None):
            return 'inf'
        return Event._to_time_format(self.duration)

    @staticmethod
    def _to_time_format(sec):
        if(sec is None):
            return 'None'
        if(sec is math.inf or sec is -math.inf):
            return str(sec)

        z = sec
        h = int(z//3600)
        z -= (h*3600)
        m =  int(z//60)
        z -= (m*60)
        s =  int(z//1)
        z -= s
        ss = str(h) + Event._time_splitter + str(m)+Event._time_splitter + str(s)
        if(z>0):
            ss += Event._time_splitter + str(z)[0:3] #3 digits of ms if exists
        return ss
    
    def __str__(self):
        conf_str = "({}%)".format(round(self.label_confidence*100)) if self.label_confidence is not None else ""
        return "<Event: {}{} from {} ({}) to {} ({}) (dur: {} ({}))>".format(
                                                                    str(self.label),
                                                                    conf_str,
                                                                    self.start_time,
                                                                    self.start,
                                                                    self.end_time,
                                                                    self.end,
                                                                    self.duration_time,
                                                                    self.duration,
                                                                    )
    def __repr__(self):
        return str(self)
    
    def summary(self):
        print(str(self))
        
    @staticmethod
    def make_event(event_tsv, annotation):
        max_column = 4
        min_column = 3

        if(len(event_tsv)==0):
            return None
        if(len(event_tsv)<min_column):
            print('??: '+str(event_tsv))

        if(len(event_tsv)>max_column):
            event_tsv = event_tsv[:(max_column-1)]+[','.join(event_tsv[(max_column-1):])]
        
        if(event_tsv[0].lower() == 'none'):
            start = None
        elif(Event.__is_number(event_tsv[0])):
            start = float(event_tsv[0])
        elif(Event.__is_time_format(event_tsv[0])):
            r = Event.__try_load_time_format(event_tsv[0])
            start = r[0]*3600 + r[1]*60 + r[2]
        else:
            raise BaseException('the start should be in seconds or in ''h:m:s'' format while it is {} (file: {})'.format(event_tsv[0], annotation.name))

        if(event_tsv[1].lower() == 'none'):
            end = None
        elif(Event.__is_number(event_tsv[1])):
            end = float(event_tsv[1])
        elif(Event.__is_time_format(event_tsv[1])):
            r = Event.__try_load_time_format(event_tsv[1])
            end = r[0]*3600 + r[1]*60 + r[2]
        else:
            raise BaseException('the end should be in seconds or in ''h:m:s'' format while it is {} (file: {})'.format(event_tsv[0], annotation.name))

        if(event_tsv[2].lower() == 'none' or event_tsv[2].lower() == ''):
            label = None
        else:
            label = event_tsv[2]
        commentTag = (event_tsv[3] if (len(event_tsv)>3) else "")
        extrainfo = EventExtraInfo(commentTag)
        return Event(start, end, label, extrainfo, annotation)
    
    @staticmethod
    def __is_number(s):
        try:
            s = float(s) # for int, long and float
            return True
        except ValueError:
            return False
    
    @staticmethod
    def __is_time_format(s):
        r = Event.__try_load_time_format(s)
        return (True if r is not None else False)
    
    @staticmethod
    def __try_load_time_format(s):
        ss = s.split(Event._time_splitter)        
        try:
            h = float(ss[0])
            m = float(ss[1])
            s = float(ss[2])
            return (h,m,s)
        except:
            return None

    def has_overlap(self, other_event, accept_end_end):
        '''
        It returns True if the event has overlap with the other.
        parameters:
        -----------
        other_event: to be compared with
        accept_end_end: to return true if end of one is exactly the start of the other
        '''
        return self.has_overlap_range(other_event.start, other_event.end, accept_end_end)

    def has_overlap_range(self, start, stop, accept_end_end):
        '''
        It returns True if the event has overlap with the range.
        parameters:
        -----------
        start: start time in seconds
        stop: end time in seconds
        accept_end_end: to return true if end of one is exactly the start of the other
        '''
        ma = max(self.start, start) 
        mi = min(self.end, stop)
        if(ma == mi):
            return accept_end_end
        return (ma < mi)
    
        
