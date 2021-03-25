#%%
#%reload_ext autoreload
#%autoreload 2
#%%
import numpy as np
import math
import numbers
import matplotlib.pyplot as plt
from PyQt5 import QtCore, QtGui, QtWidgets
from qt_designer.base_GUI import base_UI
from qt_designer.temporal_view import Ui_TemporalView
from PyQt5.uic import loadUi
from databasemanager import *
import sys
from qt_designer.dataset_selector import Ui_dataset 
from signalplotter.qt.plotter_ui import plotter_ui
from signalplotter.plotter import plotter_countainer
from datetime import datetime
from cycler import cycler
from plotter import cplot
from configparser import ConfigParser

class gui_init(QtWidgets.QMainWindow,base_UI):
    
    UserSettings.global_settings().loading_data_missing_channel_type = 'error'
    UserSettings.global_settings().loading_data_channels = ['fp1','fp2','t3','t4','o1','o2','c3','c4']


    config = None

 
    root = ''
    data_root = None
    ds_root = None
    db = Database(root)
    datasets = db.dataset_names
    dataset_name = ""
    selected_subject = []
    
    selected_recording = []
    selected_annotation = []

    selected_subject_recordings = []

    matching_subjects = []
    matching_recordings = []
    clicked_subject = None
    clicked_recording = None

    recording_plotter_container = None

    event_plots = {}

    
    def __init__(self):
        plt.ion()
        super(gui_init, self).__init__()
        self.myOtherWindow = QtWidgets.QMainWindow()
        self.temporalwindow = QtWidgets.QMainWindow()
        self.ui = base_UI()
        self.ui.setupUi(self)
        self.ui.Dataset_label.clicked.connect(self.get_dataset)
        self.ui.lineEdit.textChanged.connect(self.search_subject_list)
        self.ui.lineEdit_2.textChanged.connect(self.search_recording_list)
        self.ui.subject_list.currentItemChanged.connect(self.update_recording_list)
        self.ui.recordings_list.currentItemChanged.connect(self.update_annotation_list)
        self.ui.annotations_list.currentItemChanged.connect(self.update_event_list)
        self.ui.recordings_list.itemDoubleClicked.connect(self.openRecording)
        self.ui.pushButton_8.clicked.connect(self.openTemporal)
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


    def openRecording_temporal(self, timestamp):
        self.clicked_recording = None
        self.get_recording_names_temporal()
        for rec in self.clicked_subject.recordings:
            start = datetime.timestamp(rec.start_of_recording)
            stop = rec.duration_sec + start
            if((timestamp > start) and (timestamp < stop)):
                self.clicked_recording = rec
                break
        if(self.clicked_recording is not None):
        
            window = 10
            y=None
            title=None
            fs=int(self.clicked_recording.fs)
            sens=None
            channel_names=UserSettings.global_settings().loading_data_channels
            callback=None
            channel_first:bool = True
            verbose:bool = True


            lazy_plot:bool = True


            cplot(self, self.clicked_recording, lazy_plot, window, title,fs,sens,channel_names, callback, channel_first, verbose)
    

    def openRecording(self, item):
    
        self.get_recording_names()
        recording_name = item.text()
        index = self.selected_subject_recordings.index(recording_name)
        doubleclicked_recording = self.selected_subject.recordings[index]    
        window = 10
        y=None
        title=None
        fs=int(doubleclicked_recording.fs)
        sens=None
        channel_names=UserSettings.global_settings().loading_data_channels
        callback=None
        channel_first:bool = True
        verbose:bool = True


        lazy_plot:bool = True
    
        
        cplot(self,doubleclicked_recording, lazy_plot, window, title,fs,sens,channel_names, callback, channel_first, verbose)



    def drawTemporal(self):
        self.subplots = {}
        i = 0
        for  idx, sub in enumerate(self.ds.subjects):
            self.subplots[idx] = self.ui3.TemporalPlot.canvas.add(cols = 1)
            self.subplots[idx].axhline(y=0, color="royalblue", alpha = 0.9,linestyle="--")

            #plotting the recordings
            custom_cycler = (cycler(color=['dodgerblue','mediumblue']))
            self.subplots[idx].set_prop_cycle(custom_cycler)
            for rec in sub.recordings:
                start = datetime.timestamp(rec.start_of_recording)
                stop = rec.duration_sec + start

                self.subplots[idx].plot([start, stop], [0, 0],linewidth=10)

            #plotting the events
            custom_cycler = (cycler(color=['darkorange','gold']))
            self.subplots[idx].set_prop_cycle(custom_cycler)
            for rec in sub.recordings:
                start = datetime.timestamp(rec.start_of_recording)
                for ann in rec.annotations:
                    for event in ann.events:
                        if(event.label != 'bckg'):
                            ev_start = event.start + start
                            ev_stop = event.stop + start
                            self.event_plots[i] = self.subplots[idx].plot([ev_start, ev_stop], [0, 0],linewidth=15, alpha = 0.5)
                            i = i + 1
                            
                        
            #ax[idx].axis('off')
            self.subplots[idx].axes.set_ylim([-1,1])
            self.subplots[idx].spines["top"].set_visible(False)
            self.subplots[idx].spines["right"].set_visible(False)
            self.subplots[idx].spines["bottom"].set_visible(False)
            self.subplots[idx].spines["left"].set_visible(False)
            self.subplots[idx].set_yticks([])
            self.subplots[idx].set_xticks([])
            self.subplots[idx].set_ylabel(self.ds.subject_names[idx],rotation='horizontal', ha='right',va="center")
        

    def event_checked(self, is_checked):
        if is_checked:
            i = 0
            for  idx, sub in enumerate(self.ds.subjects):
                custom_cycler = (cycler(color=['darkorange','gold']))
                self.subplots[idx].set_prop_cycle(custom_cycler)
                for rec in sub.recordings:
                    start = datetime.timestamp(rec.start_of_recording)
                    for ann in rec.annotations:
                        for event in ann.events:
                            if(event.label != 'bckg'):
                                ev_start = event.start + start
                                ev_stop = event.stop + start
                                self.event_plots[i] = self.subplots[idx].plot([ev_start, ev_stop], [0, 0],linewidth=15, alpha = 0.5)
                                i = i + 1
        else:
            for i in range(len(self.event_plots)):
                self.event_plots[i].pop(0).remove()
        self.ui3.TemporalPlot.canvas.draw_idle()





    def openTemporal(self):
        def temporal_click(event):
            if event.inaxes is not None:
                index = self.ds.subject_names.index(event.inaxes.get_ylabel())
                self.clicked_subject = self.ds.subjects[index]
                self.openRecording_temporal(event.xdata)

        self.ui3 = Ui_TemporalView()
        self.ui3.setupUi(self.temporalwindow)
        self.ui3.EventsCheckbox.setChecked(True)
        self.drawTemporal()
        self.ui3.TemporalPlot.canvas.mpl_connect('button_press_event', temporal_click)
        self.ui3.EventsCheckbox.toggled.connect(self.event_checked)
        self.temporalwindow.show()
 
    
    def clear_GUI(self):
        self.ui.subject_list.clear()
        self.ui.recordings_list.clear()
        self.ui.annotations_list.clear()
        self.ui.events_list.clear()

    def get_recording_names_temporal(self):
        self.clicked_subject_recordings = []
        for r in self.clicked_subject.recordings:
            self.clicked_subject_recordings.append(r.name)

    def get_recording_names(self):
        self.selected_subject_recordings = []
        for r in self.selected_subject.recordings:
            self.selected_subject_recordings.append(r.name)


    def update_GUI(self):
        subject_names = self.ds.subject_names
        self.clear_GUI()
        self.ui.subject_list.addItems(self.matching_subjects)
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
        print(item)
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
    app = QtWidgets.QApplication(sys.argv)
    w = gui_init()
    w.config = ConfigParser()
    w.config.read('config.ini')
    if(w.config.get('database', 'root') is not None):
        w.root = w.config.get('database', 'root')
    w.db = Database(w.root)
    w.datasets = w.db.dataset_names
    if(w.config.get('database', 'dataset') is not None):
        w.doubleclick_dataset(w.config.get('database', 'dataset'))

    w.show()
    sys.exit(app.exec_())