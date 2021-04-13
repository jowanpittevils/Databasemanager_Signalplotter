#==================================================#
# Authors: Amir H. Ansari <amirans65.ai@gmail.com> #
# License: BSD (3-clause)                          #
#==================================================#

from databasemanager.classes.path import Path
from databasemanager.classes.edfrecording import EDFRecording


class RecordingMaker(object):
    __typeMapper = {'.edf':EDFRecording}

    @staticmethod
    def make(path, subject_name, recording_file_name, recording_file_extension, annotation_list):
        '''
            Makes a recording class according to the recording file extension.
            
            parameters:
            -----------
            path: an object of Path class or absolute string indicating the database root
            subject_name: the name of the subject
            recerding_file_name: the stem name of the recording file name without extension
            recording_file_extension: the extension/suffix of the recording file including the dot
            annotation_list: a zip of annotation file name and annotation index
        '''
        
        if(not recording_file_extension.lower() in RecordingMaker.__typeMapper):
            raise BaseException('the recording extension is not supported. ({})'.format(recording_file_extension))
        RecorderClass = RecordingMaker.__typeMapper[recording_file_extension.lower()]
        return RecorderClass(
                            path, subject_name, 
                            recording_file_name, 
                            recording_file_extension, 
                            annotation_list
                            )