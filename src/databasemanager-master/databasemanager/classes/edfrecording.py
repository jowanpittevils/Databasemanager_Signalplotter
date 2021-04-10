#==================================================#
# Authors: Amir H. Ansari <amirans65.ai@gmail.com> #
# License: BSD (3-clause)                          #
#==================================================#

from databasemanager.classes.recording import Recording
from databasemanager.classes.MNEfetchableinterface import MNEFetchableInterface
from databasemanager.classes.annotation import Annotation
from databasemanager.settings.usersettings import UserSettings
from databasemanager.MNEextensions.rawlist import RawList
from databasemanager.EDF.ezEDF import edf


class EDFRecording(Recording):

    # override MNEFetchableInterface.fetch_mne_list()
    def fetch_mne_list(self, set_annotations: bool = True, aggregated_annotation:Annotation = None):
        '''
        It return a list of mne raw. 

        parameters:
        -----------
        set_annotations: if it is True, it sets the mne annotations before returning. 
        aggregated_annotation: if set_annotations is True and the recording has multiple annotation, this parameter is obligatory. Otherwise, it can be None.
        '''
        mne_raw = self.__edf.mne_raw.copy()
        if(set_annotations and len(self.annotations)>0):
            if(aggregated_annotation is None):
                if(len(self.annotations)>1):
                    raise ValueError("When the recording has multiple annotations, the given 'aggregated_annotation' cannot be None!")
                else:
                    aggregated_annotation = self.annotations[0]
            mne_ann = aggregated_annotation.get_mne_annotations()
            mne_raw.set_annotations(mne_ann)
        mne_list = RawList([mne_raw])
        return mne_list

    # override RecordingBase.duration()
    @property
    def duration_samp(self):
        return self.__edf.mne_raw.n_times

    # override RecordingBase.start_of_recording()
    @property
    def start_of_recording(self):
        return self.__edf.start_of_recording

    # override RecordingBase.__get_raw_data()
    def get_unprocessed_data(self, start, stop):
        '''Load and return data, start and stop are in samples.'''
        return self.__edf.mne_raw.get_data(
                                            self.reordering_indeces,
                                            start,
                                            stop
                                            )

    # override RecordingBase.number_of_channels()
    @property
    def number_of_channels(self):
        return len(self.__edf.channels_info)

    def __init__(self, path, subject_name, file_name,file_extension, annotation_list):
        super().__init__(path, subject_name, file_name,file_extension, annotation_list)
        self.type = "EDF"

        self.settings = UserSettings.global_settings()
        loading_data_channels = self.settings.loading_data_channels
        loading_data_frequency_type = self.settings.loading_data_frequency_type
        loading_data_missing_channel_type = self.settings.loading_data_missing_channel_type
        
        self.__edf = edf(
            path.get_recording_fullpath(subject_name, file_name + file_extension),
            channels = loading_data_channels,
            fs_type=loading_data_frequency_type,
            missing_channel=loading_data_missing_channel_type)
        self.has_content = self.__edf.has_content
        #to be used in get_data
        chs = self.channels
        self.reordering_indeces = [self.__edf.mne_raw.ch_names.index(ch) for ch in chs]

        
    @property
    def channel_info_list(self):
        return self.__edf.channels_info

        
    @property
    def channels(self):
        return [ch.name for ch in self.channel_info_list]

    @property
    def fs(self):
        fs = self.__edf.fs
        return fs if fs is not None else tuple(self.__edf.channelFs)

