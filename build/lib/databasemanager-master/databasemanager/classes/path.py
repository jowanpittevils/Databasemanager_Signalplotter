#==================================================#
# Authors: Amir H. Ansari <amirans65.ai@gmail.com> #
# License: BSD (3-clause)                          #
#==================================================#

import glob
import collections
from os import walk
from os.path import join
from pathlib import Path as PathLibClass


class Path():
    '''
        This class organizes all path and folders of the database.
        There are two ways for making a Path object:
        -- set the root, in which there is a 'Data' and a 'Datasets' folder.
        -- set data_folder and datasets_folder.
        for each case, the other(s) must be None.

        parameters:
        -----------
        root: the path of the root folder
        data_path: the path of the data folder (if root is not set)
        datasets_path: the path of the datasets folder (if root is not set)


        General rules of the database structure:
        subjects folder Name: [string]number. must ends with number. e.g. a123, 123
        recording file Name: subjectName+letter where letter ranges between 'a' to 'z'. It must starts with the subjectname and ends with a single letter 
            (maximum 28 rec is possible now). In case of a single recording, the letter can be dropped. e.g. a123c.edf, 123a.edf, 123.edf. 
        annotation file Name: recordingName+number where the number is a single digit starting from 1. must starts with the corresponding recording file name and ends with number. 
            In case of a single annotation, the file name can be exactly as the recording file name (the extensions are different).
            e.g. a123.tsv, a123c.tsv, 123a_2.tsv
    '''
    DATAFOLDER = 'Data'
    DATASETSFOLDER = 'Datasets'
    DATASETFILEEXTENSION = '.tsv'
    ANNOTATIONFILEEXTENSION = '.tsv'
    EXTRAFOLDER = 'Extra'
    RECORDINGSUFFIX = '_r'
    ANNOTATIONSUFFIX = '_a'
    
    @classmethod
    def _get_path(cls, path, has_session_folder:bool = False):
        if(isinstance(path, cls)):
            return path
        elif(isinstance(path, str)):
            return Path(path, has_session_folder=has_session_folder)
        else:
            raise BaseException('Path must be a string or an object of '+str(cls))

    @classmethod
    def get_defaulte_data_folder_fullpath(cls, root):
        '''returns the full path of the 'Data' folder based on the 'root' attribute.'''
        return join(root, cls.DATAFOLDER)
    
    @classmethod
    def get_defaulte_datasets_folder_fullpath(cls, root):
        '''returns the full path of the 'Datasets' folder based on the 'root' attribute.'''
        return join(root, cls.DATASETSFOLDER)
    
    @classmethod
    def get_defaulte_extra_folder_fullpath(cls, root):
        '''returns the full path of the 'Extra' folder based on the 'root' attribute.'''
        return join(root, cls.EXTRAFOLDER)

    def __init__(self, root, data_path=None, datasets_path=None):
        if(root is not None):
            assert((data_path is None ) and (datasets_path is None))
            self.root = root
            self.__data_path = self.get_defaulte_data_folder_fullpath(root)
            self.__datasets_path = self.get_defaulte_datasets_folder_fullpath(root)
        else:
            assert((data_path is not None ) and (datasets_path is not None))
            self.__data_path = data_path
            self.__datasets_path = datasets_path
            self.root = None
        
    
    @property
    def datafolder_fullpath(self):
        '''returns the full path of the 'Data' folder.'''
        return self.__data_path
    
    @property
    def datasetsfolder_fullpath(self):
        '''returns the full path of the 'Datasets' folder.'''
        return self.__datasets_path
    
    @property
    def extrafolder_fullpath(self):
        '''returns the full path of the 'Extra' folder if the root has been set.'''
        if(self.root is None):
            return None
        return self.get_extrafolder_fullpath(self.root)

    @property
    def datasets_list_fullpath(self):
        '''returns a list of all fullpath corresponding the existing datasets.'''
        folderS = join(self.datasetsfolder_fullpath, "*" + Path.DATASETFILEEXTENSION)
        files = [f for f in glob.glob(folderS, recursive=False)]
        return files  
    
    @property
    def datasets_list_names(self):
        '''returns a list of all existing dataset names.'''
        names = [PathLibClass(f).stem for f in self.datasets_list_fullpath]
        return names      
    
    def get_dataset_fullpath(self, name):
        '''returns the full path of a dataset based on the given dataset name.'''
        return join(self.datasetsfolder_fullpath, name + self.DATASETFILEEXTENSION)
    
    def get_subject_fullpath(self, name):
        '''returns the full path of the subject data folder based on the subject name.'''
        return join(self.datafolder_fullpath, name)

    def get_annotation_fullpath(self, subject_name, annotation_name):
        '''returns the full path of an annotation file.'''
        p = self.get_subject_fullpath(subject_name)
        return join(p, annotation_name + self.ANNOTATIONFILEEXTENSION)
    
    def get_recording_fullpath(self, subject_name,recording_name_with_extension):
        '''returns the full path of an recording file.'''
        p = self.get_subject_fullpath(subject_name)
        return join(p,recording_name_with_extension)

    def get_all_subject_names(self): 
        '''returns a list of all folders (subject names) in the 'Data' folder.'''
        return self.get_all_folder_names(self.datafolder_fullpath)
    
    @staticmethod
    def get_all_folder_names(dir):
        res = []
        for (_, dirs, _) in walk(dir, topdown=False):
            for name in dirs:
                res.append(name)
        return res


    def get_recordings_details(self, subject_name):
        ''' returns a sorted list of tuples as (fullpath,recname,extension,recordingSuffix) 
            e.g. ('c:\\data\\a1\\a1.edf', 'a1_r1','.edf',1)
            the output is sorted by the recording suffix '_rx'.
            parameters:
            -----------
            subjectName: the name of the target subject
        '''

        filepath = self.get_subject_fullpath(subject_name)

        folderS = join(filepath, "*")
        full = [(f,PathLibClass(f).stem, PathLibClass(f).suffix) 
                for f in glob.glob(folderS, recursive=False) 
                if PathLibClass(f).suffix.lower() != self.ANNOTATIONFILEEXTENSION.lower()]
        
        compnames = []
        for f in full:
            fullpath = f[0]
            recname = f[1]
            extension = f[2]
            ind0 = recname.rfind(self.RECORDINGSUFFIX)
            if(ind0 == -1):
                raise ValueError("All recording files must end with '_r' following the recording index, e.g. 'sub1_r5.edf'. Error on: " + recname)
            ind = ind0 + len(self.RECORDINGSUFFIX)
            suffix = int(recname[ind:])
            compnames.append((fullpath, recname, extension, suffix))
        

        compnames.sort(key = lambda comp: comp[3])
        return compnames
        
    def get_annotations_details(self, subject_name, recording_name):
        ''' returns a sorted list of tuples as (fullpath,annotationname,annotationsuffix) where a is the fullpath, b is the real file name, and c is the annotator suffix. 
            Note that if the annotation does not end with a number it is supposed to end with '1' as the first annotation file.
            e.g. ('c:\\amir1.tsv', 'amir1a.tsv', 'amir1a2.tsv')
            It is sorted by the annotation number of the sorting file names.
            parameters:
            -----------
            subjectName: the name of the target subject
            recordingName: the name of the real recording file name
        '''
        recs = self.get_recordings_details(subject_name)
        rec = [c for c in recs if c[1].lower() == recording_name.lower()]
        assert(len(rec)==1)
        rec = rec[0]
        f = self.get_subject_fullpath(subject_name)
        folderS = join(f, "*")
        full = [(f,PathLibClass(f).stem) 
                for f in glob.glob(folderS, recursive=False) 
                if PathLibClass(f).suffix.lower() == self.ANNOTATIONFILEEXTENSION.lower()]
        
        compnames = []
        for f in full:
            fullpath = f[0]
            annotname = f[1]
            ind0 = annotname.rfind(self.ANNOTATIONSUFFIX)
            if(ind0 == -1):
                raise ValueError("All annotation files must end with '_a' following the annotation index, e.g. 'sub1_r5_a1.edf'. Error on: " + annotname)
            recnameofannot = annotname[:ind0]
            if(recnameofannot != recording_name):
                continue
            
            ind = ind0 + len(self.ANNOTATIONSUFFIX)
            suff = int(annotname[ind:])
            compnames.append((fullpath, annotname, suff))
        compnames.sort(key = lambda comp: comp[2])
        return compnames

        
        
    