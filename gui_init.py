#%%
#%reload_ext autoreload
#%autoreload 2
#%%
import numpy as np
import math
import numbers
#from signalplotter import cplot, gplot, iplot


from PyQt5 import QtCore, QtGui, QtWidgets

from PyQt5.QtWidgets import QMainWindow 

from qt_designer.base_GUI import base_UI
from PyQt5.uic import loadUi
from databasemanager import *
import sys
from qt_designer.dataset_selector import Ui_dataset 
from signalplotter.qt.plotter_ui import plotter_ui
from signalplotter.plotter import plotter_countainer


class gui_init(QMainWindow,base_UI):
    
    UserSettings.global_settings().loading_data_missing_channel_type = 'error'
    UserSettings.global_settings().loading_data_channels = ['fp1','fp2','t3','t4','o1','o2','c3','c4']
 
    root = ''
    data_root = None
    ds_root = None
    db = Database(root)
    datasets = db.dataset_names
    ds = db.load_dataset('all')
    dataset_name = ""
    selected_subject = []
    
    selected_recording = []
    selected_annotation = []

    selected_subject_recordings = []

    matching_subjects = []
    matching_recordings = []
    
    

    
    def __init__(self):
        super(gui_init, self).__init__()
        self.ui = base_UI()
        self.ui.setupUi(self)
        self.ui.Dataset_label.clicked.connect(self.get_dataset)
        self.ui.lineEdit.textChanged.connect(self.search_subject_list)
        self.ui.lineEdit_2.textChanged.connect(self.search_recording_list)
        self.ui.subject_list.currentItemChanged.connect(self.update_recording_list)
        self.ui.recordings_list.currentItemChanged.connect(self.update_annotation_list)
        self.ui.annotations_list.currentItemChanged.connect(self.update_event_list)
        self.ui.recordings_list.itemDoubleClicked.connect(self.openRecording)
        self.chns = ['fp1','fp2','t3','t4','o1','o2','c3','c4']
    
    def load_database(self):
        self.datasets = self.db.dataset_names
        self.ds = self.db.load_dataset('all')
        self.dataset_name = ""
        self.selected_subject = []   
        self.selected_recording = []
        self.selected_annotation = []
        self.selected_subject_recordings = []
        self.matching_subjects = []
        self.matching_recordings = []

    def openRecording(self, item):


        def prepare_x(x, window, fs, channel_first):
            if(type(x) == list):
                xx = []
                for i in range(len(x)):
                    xx.append(prepare_x(x[i], window, fs, channel_first))
                return xx

            assert(isinstance(x, np.ndarray))
            if(x.ndim == 1):
                x = np.expand_dims(x,1)
                channel_first = False
            assert(x.ndim == 2)
            if(not channel_first):
                x = x.transpose()
                channel_first = True

            window_sample = window * fs
            CH = x.shape[0]
            T = x.shape[1]
            Nceil = math.ceil(T/window_sample)
            z = np.zeros((CH, Nceil*window_sample - T))
            x = np.concatenate((x,z),1)
            T = x.shape[1]
            assert((T%window_sample)==0)
            xx = np.reshape(x, (CH, int(T/window_sample), window_sample))
            xx = xx.transpose((1,0,2))
            return xx
    
        self.get_recording_names()
        recording_name = item.text()
        index = self.selected_subject_recordings.index(recording_name)
        doubleclicked_recording = self.selected_subject.recordings[index]
        
        data = doubleclicked_recording.get_data()
        window = 10
        y=None
        title=None
        fs=250
        sens=None
        channel_names=None
        callback=None
        channel_first:bool = True
        verbose:bool = True
        segments = prepare_x(data, window, fs, channel_first)

        if(type(segments) != list):
            segments=[segments]
        N = len(segments)
        if(type(title) != list):
            title=[title] * N
        if(type(fs) != list):
            fs=[fs] * N
        if(type(sens) != list):
            sens=[sens] * N
        if(type(callback) != list):
            callback=[callback] * N
        if(channel_names is None):
            channel_names = [None] * N
        elif(type(channel_names[0]) != list):
            channel_names = [channel_names] * N

        self.plotter = plotter_countainer()

        N = len(segments)
        for i in range(N):
            self.plotter.add(segments[i],y,title[i],fs[i],sens[i],channel_names[i],callback[i], channel_first, verbose)
        appind = app.exec_()


    

    def clear_GUI(self):
        self.ui.subject_list.clear()
        self.ui.recordings_list.clear()
        self.ui.annotations_list.clear()
        self.ui.events_list.clear()

    def get_recording_names(self):
        self.selected_subject_recordings = []
        for r in self.selected_subject.recordings:
            self.selected_subject_recordings.append(r.name)


    def update_GUI(self):
        subject_names = self.ds.subject_names
        self.clear_GUI()
        self.ui.subject_list.addItems(self.matching_subjects)
        self.ui.recordings_list.addItems(self.matching_recordings)
        #self.ui.annotations_list.addItems(annotations)
        #self.ui.events_list.addItems(events)
        self.ui.label_11.setText(self.dataset_name)
        self.ui.lineEdit.start(subject_names)
        self.ui.lineEdit_2.start(self.matching_recordings)

    def search_subject_list(self):
        self.matching_subjects = [s for s in self.ds.subject_names if self.ui.lineEdit.text() in s]
        self.update_GUI()

    def search_recording_list(self):
        self.get_recording_names()
        self.matching_recordings = [r for r in self.selected_subject_recordings if self.ui.lineEdit_2.text() in r]
        self.update_GUI()


    def update_recording_list(self, item):
        if item is not None:
            subject = item.text()
            index = self.ds.subject_names.index(subject)
            self.selected_subject = self.ds.subjects[index]
            recordings = []
            for i in range(len(self.selected_subject.recordings)):
                if self.ui.lineEdit_2.text() in self.selected_subject.recordings[i].name:
                    recordings.append(self.selected_subject.recordings[i].name)
            self.ui.recordings_list.clear()
            self.ui.annotations_list.clear()
            self.ui.events_list.clear()
            self.ui.recordings_list.addItems(recordings)


    def update_annotation_list(self, item):
        if item is not None:
            recording = item.text()
            for i in range(len(self.selected_subject.recordings)):
                if recording == self.selected_subject.recordings[i].name:
                    self.selected_recording = self.selected_subject.recordings[i]
            annotations = []
            for annotation in self.selected_recording.annotations:
                annotations.append(annotation.name)
            self.ui.annotations_list.clear()
            self.ui.events_list.clear()
            self.ui.annotations_list.addItems(annotations)
    
    def update_event_list(self,item):
        if item is not None:

            annotation = item.text()
            for i in range(len(self.selected_recording.annotations)):
                if annotation == self.selected_recording.annotations[i].name:
                    self.selected_annotation = self.selected_recording.annotations[i]
            event_list = []
            for events in self.selected_annotation.events:
                event_list.append(events.label + " " + str(int(events.start)) + "-" + str(int(events.end)))
            self.ui.events_list.clear()
            self.ui.events_list.addItems(event_list)
    
    def load_dataset(self):
        self.ds = self.db.load_dataset(self.dataset_name)
        self.matching_subjects = [subject for subject in self.ds.subject_names if self.ui.lineEdit.text() in subject]
        self.selected_subject = self.ds.subjects[0]
        self.selected_recording = self.ds.subjects[0].recordings[0]
        self.get_recording_names()
        self.matching_recordings = [r for r in self.selected_subject_recordings if self.ui.lineEdit_2.text() in r]
        self.update_GUI()

    def doubleclick_dataset(self, item):
        self.dataset_name = item.text()
        self.myOtherWindow.hide()
        self.load_dataset()

    def get_dataset(self):
        self.myOtherWindow = QtWidgets.QMainWindow()
        self.ui2 = Ui_dataset()
        self.ui2.setupUi(self.myOtherWindow)
        self.ui2.listWidget.addItems(self.datasets)
        self.myOtherWindow.show()
        self.ui2.listWidget.itemDoubleClicked.connect(self.doubleclick_dataset)


        









if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    w = gui_init()
    w.root = 'C:\\db\\toyDB'
    w.db = Database(w.root)
    w.datasets = w.db.dataset_names
    w.ds = w.db.load_dataset('all')
    w.show()
    sys.exit(app.exec_())