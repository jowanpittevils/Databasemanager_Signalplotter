from qt_designer.temporal_view import Ui_TemporalView
from PyQt5 import QtCore, QtGui, QtWidgets
from databasemanager import *
from cycler import cycler
from custom_plotter.plotter import agplot
from datetime import datetime
import time
import numpy as np
import math
import pyqtgraph as pg
    

class temporal_ui(Ui_TemporalView):
    """
    Opens a temporal window of the given subjects from a certain database with a specified timescale.
    The temporal window shows the recordings and events of the subjects shown in each year.
    
    Parameters:
    ----------
    Database:   from the class 'database' in the package 'databasemanager'
    subjects:   A list of strings of the names of the subjects to be shown in the temporal window. (Default is None which shows a temporal window 
                of all the subjects in the given database) 

    e.g. temporal_browser(Database('C:\\db'), ['tr_ar_77', 'tr_ar_254', 'tr_ar_492'])
    """
    def __init__(self, database:Database=None, subjects=None):
        self.temporalwindow = QtWidgets.QMainWindow()
        self.setupUi(self.temporalwindow)
        self.clicked_recording = None
        self.clicked_subject = None
        self.event_plots = {}
        self.subplots = {}
        self.rec_plots = {}
        if database is not None:
            self.ds = database.load_dataset('all')
            if subjects is None:
                self.subjects = self.ds.subjects
                self.subject_names = self.ds.subject_names
            else:
                self.subjects = []
                self.subject_names = []
                for sub in subjects:
                    if self.ds.subject_names.count(sub) >0:
                         index = self.ds.subject_names.index(sub)
                         self.subjects.append(self.ds.subjects[index])
                         self.subject_names.append(self.ds.subject_names[index])
        else:
            self.subjects = subjects
            self.subject_names = [s.name for s in self.subjects]
        #self.partition_subjects()
        self.__updateValuesOfSlider()
        self.drawTemporal(self.subjects, self.subject_names)
        self.Slider.valueChanged.connect(self.__onsldValueChanged)
        self.EventsCheckbox.toggled.connect(self.event_checked)
        self.EventsCheckbox.setChecked(True)
        self.TemporalPlot.canvas.mpl_connect('button_press_event', self.temporal_click)
        self.temporalwindow.show()

    
    def partition_subjects(self):
        self.partitioned_recs = []
        i = 0
        for sub in self.subjects:
            sub_recs = []
            temp_recs = []
            for rec in sub.recordings:
                temp_recs.append(rec)
            while len(temp_recs) > 0:
                recs = []
                for rec in temp_recs:
                    min_rec = rec
                    min_stamp = datetime.timestamp(rec.start_of_recording)
                    break
                for rec in temp_recs:
                    start = datetime.timestamp(rec.start_of_recording)
                    if start < min_stamp:
                        min_rec = rec
                        min_stamp = start
                recs.append(min_rec)
                temp_recs.remove(min_rec)
                for rec in temp_recs:
                    start = datetime.timestamp(rec.start_of_recording)
                    if start < min_stamp + 31536000:
                        recs.append(rec)
                        temp_recs.remove(rec)
                sub_recs.append(recs)
            self.partitioned_recs.append(sub_recs)
        for sub_recs in self.partitioned_recs:
            if len(sub_recs) > i:
                i = len(sub_recs)
        for sub_recs in self.partitioned_recs:
            if len(sub_recs) < i:
                for k in range(i-len(sub_recs)-1):
                    sub_recs.append([])
        print(self.partitioned_recs)   

    def __updateValuesOfSlider(self):
        for sub in self.subjects:
            for rec in sub.recordings:
                self.min = datetime.timestamp(rec.start_of_recording)
                self.max = rec.duration_sec + self.min
                break
        for sub in self.subjects:
            for rec in sub.recordings: 
                start = datetime.timestamp(rec.start_of_recording)
                stop = rec.duration_sec + start
                if start < self.min:
                    self.min = start
                if stop > self.max:
                    self.max = stop
        self.min = datetime.fromtimestamp(self.min).year
        self.max = datetime.fromtimestamp(self.max).year
        self.Slider.setMinimum(self.min)
        self.Slider.setMaximum(self.max)
        self.sliderValue.setText('year:' + str(self.min))

    def __onsldValueChanged(self):
        self.sliderValue.setText('year:' + str(self.Slider.value()))
        self.EventsCheckbox.setChecked(True)
        self.event_plots.clear()
        for i in range(len(self.subplots)):
            self.subplots[i].clear()
        i = 0
        for  idx, sub in enumerate(self.subjects):
            #plotting the recordings
            custom_cycler = (cycler(color=['dodgerblue','mediumblue']))
            self.subplots[idx].set_prop_cycle(custom_cycler)
            for rec in sub.recordings:
                start = datetime.timestamp(rec.start_of_recording)
                stop = rec.duration_sec + start
                if self.Slider.value() == datetime.fromtimestamp(start).year:
                    self.subplots[idx].plot([start, stop], [0, 0],linewidth=10)
            #plotting the events
            custom_cycler = (cycler(color=['darkorange','gold']))
            self.subplots[idx].set_prop_cycle(custom_cycler)
            for rec in sub.recordings:
                start = datetime.timestamp(rec.start_of_recording)
                if self.Slider.value() == datetime.fromtimestamp(start).year:
                    for ann in rec.annotations:
                        for event in ann.events:
                            ev_start = event.start + start
                            ev_stop = event.stop + start
                            self.event_plots[i] = self.subplots[idx].plot([ev_start, ev_stop], [0, 0],linewidth=15, alpha = 0.5)
                            i += 1     
            #ax[idx].axis('off')
            self.subplots[idx].axes.set_ylim([-1,1])
            self.subplots[idx].spines["top"].set_visible(False)
            self.subplots[idx].spines["right"].set_visible(False)
            self.subplots[idx].spines["bottom"].set_visible(False)
            self.subplots[idx].spines["left"].set_visible(False)
            self.subplots[idx].set_yticks([])
            self.subplots[idx].set_xticks([])
            self.subplots[idx].set_ylabel(self.subject_names[idx],rotation='horizontal', ha='right',va="center")
            self.subplots[idx].axhline(y=0, color="royalblue", alpha = 0.9,linestyle="--")
        self.TemporalPlot.canvas.draw_idle()

    def openRecording_temporal(self, timestamp):
        self.clicked_recording = None
        for rec in self.clicked_subject.recordings:
            start = datetime.timestamp(rec.start_of_recording)
            stop = rec.duration_sec + start
            if((timestamp > start) and (timestamp < stop)):
                self.clicked_recording = rec
                break
        if(self.clicked_recording is not None):
            window = 20
            start = 0
            y=None
            title=None
            fs=int(self.clicked_recording.fs)
            sens=None
            channel_names=UserSettings.global_settings().loading_data_channels
            callback=None
            channel_first:bool = True
            verbose:bool = True
            agplot(self, self.clicked_recording, window, start, y, title,fs,sens,channel_names, callback, channel_first, verbose)

    def temporal_click(self, event):
        if event.inaxes is not None:
            index = self.subject_names.index(event.inaxes.get_ylabel())
            self.clicked_subject = self.subjects[index]
            self.openRecording_temporal(event.xdata)

    def drawTemporal(self, subjects, names):
        k = 0
        for idx, sub in enumerate(subjects):
            self.subplots[idx] = self.TemporalPlot.canvas.add(cols = 1)
            #plotting the recordings
            custom_cycler = (cycler(color=['dodgerblue','mediumblue']))
            self.subplots[idx].set_prop_cycle(custom_cycler)
            for rec in sub.recordings:
                start = datetime.timestamp(rec.start_of_recording)
                stop = rec.duration_sec + start
                if self.min == datetime.fromtimestamp(start).year:
                    self.subplots[idx].plot([start, stop], [0, 0],linewidth=10)      
            #plotting the events
            custom_cycler = (cycler(color=['darkorange','gold']))
            self.subplots[idx].set_prop_cycle(custom_cycler)
            for rec in sub.recordings:
                start = datetime.timestamp(rec.start_of_recording)
                if self.min == datetime.fromtimestamp(start).year:
                    for ann in rec.annotations:
                        for event in ann.events:
                            ev_start = event.start + start
                            ev_stop = event.stop + start
                            self.event_plots[k] = self.subplots[idx].plot([ev_start, ev_stop], [0, 0],linewidth=15, alpha = 0.5)
                            k += 1         
            #ax[idx].axis('off')
            self.subplots[idx].axes.set_ylim([-1,1])
            self.subplots[idx].spines["top"].set_visible(False)
            self.subplots[idx].spines["right"].set_visible(False)
            self.subplots[idx].spines["bottom"].set_visible(False)
            self.subplots[idx].spines["left"].set_visible(False)
            self.subplots[idx].set_yticks([])
            self.subplots[idx].set_xticks([])
            self.subplots[idx].set_ylabel(names[idx],rotation='horizontal', ha='right',va="center")
            self.subplots[idx].axhline(y=0, color="royalblue", alpha = 0.9,linestyle="--")
            
    def event_checked(self, is_checked):
        if is_checked:
            for i in range(len(self.event_plots)):
                self.event_plots[i][0].set_visible(True)
        else:
            for i in range(len(self.event_plots)):
                self.event_plots[i][0].set_visible(False)
        self.TemporalPlot.canvas.draw_idle()