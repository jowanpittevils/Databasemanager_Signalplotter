#%%
from databasemanager import *
from databasemanager.tsvreader import TSVReader
from databasemanager.classes.annotationlist import AnnotationList
from databasemanager.classes.eventlist import EventList


p1 = r'C:\Users\jowan\Documents\LEUVEN\Univ\postgraduaat\project work design\databasemanager-master\examples\Data\test1\testanot1.tsv'
p2 = r'C:\Users\jowan\Documents\LEUVEN\Univ\postgraduaat\project work design\databasemanager-master\examples\Data\test1\testanot2.tsv'
p3 = r'C:\Users\jowan\Documents\LEUVEN\Univ\postgraduaat\project work design\databasemanager-master\examples\Data\test1\testanot3.tsv'

(event_tsv_list, comments) = TSVReader.read_tsv(p1)
l1 = EventList([Event.make_event(event_tsv, None) for event_tsv in event_tsv_list])

(event_tsv_list, comments) = TSVReader.read_tsv(p2)
l2 = EventList([Event.make_event(event_tsv, None) for event_tsv in event_tsv_list])

(event_tsv_list, comments) = TSVReader.read_tsv(p3)
l3 = EventList([Event.make_event(event_tsv, None) for event_tsv in event_tsv_list])

ee = EventList.merge_eventlist([l1,l2,l3],5)


aa = ee.aggregate(
        minimum_duration_threshold_sec=1, 
        confidence_ratio=0.4, 
        remove_Nones=True,
        combine_equals=True
        )
aa


#aa2=  aa.remove_Unknowns(unknown_label='c2')
#aa2

#bb = aa.combine_equals(1)
#bb
# %%
ann1 = Annotation('', 'test1', r'C:\Users\jowan\Documents\LEUVEN\Univ\postgraduaat\project work design\databasemanager-master\examples\Data\test1\testanot1', 0)
ann2 = Annotation('', 'test1', r'C:\Users\jowan\Documents\LEUVEN\Univ\postgraduaat\project work design\databasemanager-master\examples\Data\test1\testanot2', 0)
ann3 = Annotation('', 'test1', r'C:\Users\jowan\Documents\LEUVEN\Univ\postgraduaat\project work design\databasemanager-master\examples\Data\test1\testanot3', 0)
al = AnnotationList([ann1,ann2,ann3])
aa = al.aggregate(
        minimum_duration_threshold_sec=1, 
        confidence_ratio=0.4, 
        remove_Nones=True,
        combine_equals=True
        )
aa.events
# %%
aa.add_background_label('hahaha',0)
aa.events

# %%
