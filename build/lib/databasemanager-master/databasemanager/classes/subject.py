#==================================================#
# Authors: Amir H. Ansari <amirans65.ai@gmail.com> #
# License: BSD (3-clause)                          #
#==================================================#

from pathlib import Path as PathLibClass
from databasemanager.classes.path import Path
from databasemanager.classes.recordingmaker import RecordingMaker
from databasemanager.classes.MNEfetchableinterface import MNEFetchableInterface
from databasemanager.classes.queryable import Queryable
from databasemanager.classes.listextension import ListExtension
from databasemanager.operators.operatorbase import OperatorBase
from databasemanager.operators.resampler import Resampler
from databasemanager.operators.montagemaker import MontageMaker
from databasemanager.operators.rereferencer import Rereferencer

class Subject(MNEFetchableInterface, Queryable):
    
    # override MNEFetchableInterface.fetch_mne_list()
    def fetch_mne_list(self, set_annotations: bool = True):
        mne_list = []
        temp_none = [mne_list.extend(recording.fetch_mne_list(set_annotations)) for recording in self.recordings]
        return mne_list
    
    #override copyabledoubleside
    def reassign(self):
        if(self.recordings is not None):
            for rec in self.recordings:
                rec.subject = self
                rec.reassign()

    def __init__(self, path, name, annotation_warning=True):
        if(isinstance(path, Path)):
            self.path = path
        else:
            raise BaseException('Path must be an object of Path')
        
        self.name = name
        self.recordings = self.__load_recordings()
        self.annotation_warning = annotation_warning
        self.reassign()

    def add_operator(self, op:OperatorBase):
        '''
        It gets an operator and assigns it to all of its recordings.
        '''
        assert(isinstance(op, OperatorBase))
        for r in self.recordings:
            r.add_operator(op.copy())

    def __load_recordings(self):
        recording_files = self.path.get_recordings_details(self.name)
        recordings = []
        for i,r in enumerate(recording_files):
            rec_file_name = r[1]
            rec_file_extension = r[2]
            anns = self.path.get_annotations_details(self.name, rec_file_name)
            if(anns is None or len(anns)==0):
                print('Warning: {0} has no annotation.'.format(rec_file_name))
            else:
                annotation_list = zip([a[1] for a in anns],[a[2] for a in anns])
                rec = RecordingMaker.make(self.path, self.name, rec_file_name,rec_file_extension, annotation_list)
                if(rec.has_content):
                    recordings.append(rec)
        return recordings

    def __len__(self):
        if(self.recordings is None):
            return 0
        return len(self.recordings)

    @property
    def number_of_recordings(self):
        return len(self)

    @property
    def number_of_annotations(self):
        return sum(rec.number_of_annotations for rec in self.recordings)

    @property
    def number_of_events(self):
        return sum(rec.number_of_events for rec in self.recordings)

    @property
    def duration_sec(self)->float:
        dur_sec = [rec.duration_sec for rec in self.recordings]        
        return sum(dur_sec)

    @property
    def fs(self):
        if(self.number_of_recordings==0):
            return None
        if(self.number_of_recordings==1):
            return self.recordings[0].fs
        fs = ListExtension()
        for rec in self.recordings:
            fs.extend_append(rec.fs,'ignore')
        return fs.similar_in_list()

    @property
    def number_of_channels(self):
        if(self.number_of_recordings==0):
            return None
        if(self.number_of_recordings==1):
            return self.recordings[0].number_of_channels
        ch = ListExtension()
        for rec in self.recordings:
            ch.extend_append(rec.number_of_channels,'ignore')
        return ch.similar_in_list()

    @property
    def fs_output(self):
        '''It returns the sampling frequency of the loaded data and can be affected by resampling operators (the last one).'''
        fs_output = ListExtension([r.fs_output for r in self.recordings])
        return fs_output.similar_in_list()

    @property
    def number_of_channels_output(self):
        '''It returns the number of channels of the loaded data and can be affected by montagmaker operators (the last one).'''
        res = ListExtension([rec.number_of_channels_output for rec in self.recordings])
        return res.similar_in_list()


    @property
    def unique_labels(self):
        if(self.recordings is None):
            return None
        lbl = ListExtension()
        non = [lbl.extend_append(rec.unique_labels,'add') for rec in self.recordings]
        return set(lbl)
        
    def __str__(self):
        return "<Subject {0} with {1} recordings.>".format(self.name, len(self))
    
    def summary(self):
        print(str(self))

    