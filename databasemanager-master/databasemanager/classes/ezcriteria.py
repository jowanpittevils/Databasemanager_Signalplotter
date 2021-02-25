#==================================================#
# Authors: Amir H. Ansari <amirans65.ai@gmail.com> #
# License: BSD (3-clause)                          #
#==================================================#

from databasemanager.classes.criteria import Criteria
from databasemanager.classes.event import Event
from databasemanager.classes.annotation import Annotation
from databasemanager.classes.recording import Recording
from databasemanager.classes.subject import Subject

'''
This includes  some predefined easy criteria
'''

def HasEvent():
    '''Criteria for the annotations that have at least one event.'''
    return Criteria(Annotation, lambda a: len(a.events)>0)
def HasAnnotation():
    '''Criteria for the recordings that have at least one annotation.'''
    return Criteria(Recording, lambda r: len(r.annotations)>0)
def HasRecording():
    '''Criteria for the subjects that have at least one recording.'''
    return Criteria(Subject, lambda s: len(s.recordings)>0)


def ALLEvents():
    return Criteria(Event)
def AllAnnotations():
    return Criteria(Annotation)
def AllRecordings():
    return Criteria(Recording)
def AllSubjects():
    return Criteria(Subject)
def All(target_type):
    return Criteria(target_type)

