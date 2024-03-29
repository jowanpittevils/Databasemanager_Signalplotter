#%%
#%reload_ext autoreload
#%autoreload 2
#%%
import numpy as np
import math
import numbers
import matplotlib.pyplot as plt
from PyQt5 import QtCore, QtGui, QtWidgets
from qt_designer.base_GUI import Ui_DB_explorer
from qt_designer.temporal_ui import temporal_ui
from PyQt5.uic import loadUi
from databasemanager import *
import sys
from qt_designer.dataset_selector import Ui_dataset 
from datetime import datetime
from cycler import cycler
from custom_plotter.plotter import agplot
from configparser import ConfigParser
from os import path

class database_ui(QtWidgets.QMainWindow,Ui_DB_explorer):
    """
    This class is to orderly navigate through the database, showing all information (subjects, recordings, annotations and events). 
    The class does the following:
    -   opens a temporal view of the dataset which optionally shows events and annotations
    -   Change datasets
    -   Open a recording in a new window using matplotlib by double-clicking it
    -   Open an event in a new window by double-clicking it
    -   Search for specific subjects, recordings or events
    -   Have a summary button that displays the most important information regarding the currently selected dataset (sampling frequency, channels,...)
    """
    def __init__(self):
        plt.ion()
        super(database_ui, self).__init__()
        UserSettings.global_settings().loading_data_missing_channel_type = 'error'
        UserSettings.global_settings().loading_data_channels = ['fp1','fp2','t3','t4','o1','o2','c3','c4']
        self.root = ''
        self.data_root = ''
        self.ds_root = ''
        self.db = Database(self.root)
        self.datasets = self.db.dataset_names
        self.dataset_name = ""
        self.myOtherWindow = QtWidgets.QMainWindow()
        self.selected_subject = []
        self.selected_recording = []
        self.selected_annotation = []
        self.selected_subject_recordings = []
        self.matching_subjects = []
        self.matching_recordings = []
        self.event_plots = {}
        self.ui = Ui_DB_explorer()
        self.ui.setupUi(self)

        self.config = ConfigParser()
        self.config.read('config.ini')
        if(self.config.has_section('database')):
            self.root = self.config.get('database', 'root')
            if path.exists(self.root + '/Datasets'):
                self.db = Database(self.root)
            else:
                self.data_root = self.root + '/Data'
                self.ds_root = self.config.get('database', 'ds_root')
                self.db = Database(None, self.data_root, self.ds_root)
            self.datasets = self.db.dataset_names
            if self.config.get('database', 'dataset') != "":
                self.doubleclick_dataset(self.config.get('database', 'dataset'))
        else:
            self.config.add_section('database')
            self.config.set('database', 'root', self.root)
            self.config.set('database', 'ds_root', self.ds_root)
            self.config.set('database', 'dataset', self.dataset_name)
            with open('config.ini', 'w') as f:
                self.config.write(f)
        self.__AssignCallbacks()
    
    def __AssignCallbacks(self):
        self.chns = ['fp1','fp2','t3','t4','o1','o2','c3','c4']
        self.ui.Dataset_label.clicked.connect(self.get_dataset)
        self.ui.lineEdit.textChanged.connect(self.search_subject_list)
        self.ui.lineEdit_2.textChanged.connect(self.search_recording_list)
        self.ui.subject_list.currentItemChanged.connect(self.update_recording_list)
        self.ui.recordings_list.currentItemChanged.connect(self.update_annotation_list)
        self.ui.annotations_list.currentItemChanged.connect(self.update_event_list)
        self.ui.recordings_list.itemDoubleClicked.connect(self.openRecording)
        self.ui.events_list.itemDoubleClicked.connect(self.openEventRecording)
        self.ui.pushButton_8.clicked.connect(self.openTemporal)

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
        self.get_recording_names()
        recording_name = item.text()
        index = self.selected_subject_recordings.index(recording_name)
        doubleclicked_recording = self.selected_subject.recordings[index]    
        window = 20
        start=0
        y=None
        title=None
        fs=int(doubleclicked_recording.fs)
        sens=None
        channel_names= None   
        callback=None
        verbose:bool = True
        agplot(doubleclicked_recording, window, start, y, title, fs, sens, channel_names, callback, verbose, self)
    
    def openEventRecording(self,item):
        event = item.text()
        for key in self.event_list.keys():
            if event == key:
                doubleclicked_event = self.event_list[key]
        start = doubleclicked_event.start
        window = 60
        y=None
        title=None
        fs=int(self.selected_recording.fs)
        sens=None
        channel_names= None
        callback=None
        verbose:bool = True
        agplot(self.selected_recording, window, start, y, title, fs, sens, channel_names, callback, verbose, self)

    def openTemporal(self):
        self.ui3 = temporal_ui(None,self.ds.subjects)

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
        #self.ui.recordings_list.addItems(self.matching_recordings)
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
            self.event_list = {}
            for event in self.selected_annotation.events:
                self.event_list[event.label + " " + str(int(event.start)) + "-" + str(int(event.end)) + " s"] = event
            self.ui.events_list.clear()
            self.ui.events_list.addItems(self.event_list.keys())
    
    def load_dataset(self):
        self.ds = self.db.load_dataset(self.dataset_name)
        self.matching_subjects = [subject for subject in self.ds.subject_names if self.ui.lineEdit.text() in subject]
        self.selected_subject = self.ds.subjects[0]
        self.selected_recording = self.ds.subjects[0].recordings[0]
        self.get_recording_names()
        self.matching_recordings = [r for r in self.selected_subject_recordings if self.ui.lineEdit_2.text() in r]
        self.update_GUI()

    def doubleclick_dataset(self, item):
        if not (isinstance(item, str)):
            self.dataset_name = item.text()
        else:
             self.dataset_name = item
        self.config.set('database', 'dataset', self.dataset_name)
        with open('config.ini', 'w') as f:
            self.config.write(f)
        self.myOtherWindow.hide()
        self.load_dataset()

    def get_dataset(self):
        self.ui2 = Ui_dataset()
        self.ui2.setupUi(self.myOtherWindow)
        self.ui2.listWidget.addItems(self.datasets)
        self.myOtherWindow.show()
        self.ui2.listWidget.itemDoubleClicked.connect(self.doubleclick_dataset)




if __name__ == "__main__":
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    if hasattr(QtWidgets.QStyleFactory, "AA_UseHighDpiPixmaps"):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps)
    app = QtWidgets.QApplication(sys.argv)
    w = database_ui()
    w.show()
    sys.exit(app.exec_())