#==================================================#
# Authors: Amir H. Ansari <amirans65.ai@gmail.com> #
# License: BSD (3-clause)                          #
#==================================================#

import random
from databasemanager.classes.event import Event
from databasemanager.classes.noneablelist import NoneableList

def _mode_list(lst:list):
    '''
    return the list of all most frequent values in the given list.
    return
    ------
    tuple (list of mode values, frequency)
    '''
    if(lst is None):
        return (None,None)
    if(len(lst)==0):
        return (None,None)
    s=set(lst)
    c=[lst.count(i) for i in s]
    z=list(zip(c,s))
    z=sorted(z, key=lambda x:-x[0])
    freq = z[0][0]
    mode_values = [x[1] for x in z if x[0]==freq]
    return (mode_values, freq)
   

def majority_voting(event_list, label_tied_order=None):
    '''It applies majority voting on the given event_list. 'label_tied_order' defined how to break the tie cases. 
       If 'label_tied_order' is None, it is done randomely.
       It does not change the input.
       return
       ------
       the resulted eventlist
       '''
    res = event_list.copy()
    for event in res:
        lbl = event.label
        if(isinstance(lbl,str)):
            lbl = [lbl]
        md = NoneableList(lbl).get_non_Nones()
        ln = len(md)
        (md,freq) = _mode_list(md)
        if(md is None):
            event.label = None
            event.label_confidence = None
            continue
        event.label_confidence = freq/ln
        if(len(md)==1):
            event.label = md[0]
        else:
            if(label_tied_order is None):
                event.label = random.choice(md)
            else:
                for lbl in label_tied_order:
                    if(lbl in md):
                        event.label = lbl
                        break
                event.label = random.choice(md)
    return res







    