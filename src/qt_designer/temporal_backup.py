from qt_designer.temporal_view import Ui_TemporalView
from PyQt5 import QtCore, QtGui, QtWidgets
from databasemanager import *
from cycler import cycler
from custom_plotter.plotter import agplot
from datetime import datetime

class temporal_ui(Ui_TemporalView):
    """
    Opens a temporal window of the given subjects from a certain database with a specified timescale.
    The temporal window shows the recordings and events of the subjects situated relative to each other in the specified timescale.
    
    Parameters:
    ----------
    Database:   from the class 'database' in the package 'databasemanager'
    subjects:   A list of strings of the names of the subjects to be shown in the temporal window. (Default is None which shows a temporal window 
                of all the subjects in the given database) 
    timescale:  A string which shows the recordings and events in that timescale situated from each other.
                inputs can be: 'day', 'week', 'month and 'year' (Default is 'year')

    e.g. temporal_browser(Database('C:\\db'), ['tr_ar_77', 'tr_ar_254', 'tr_ar_492'], 'day')
    """
    def __init__(self, database:Database=None, subjects=None, timescale = 'year'):
        self.temporalwindow = QtWidgets.QMainWindow()
        self.setupUi(self.temporalwindow)
        self.clicked_recording = None
        self.clicked_subject = None
        self.timescale = timescale
        if self.timescale == 'day':
            self.timescale_int = 86400
        if self.timescale == 'week':
            self.timescale_int = 604800
        if self.timescale == 'month':
            self.timescale_int = 2629744
        if self.timescale == 'year':
            self.timescale_int = 31536000
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
        self.partition_subjects()
        self.__updateValuesOfSlider()
        self.drawTemporal()
        self.Slider.valueChanged.connect(self.__onsldValueChanged)
        self.EventsCheckbox.toggled.connect(self.event_checked)
        self.EventsCheckbox.setChecked(True)
        self.TemporalPlot.canvas.mpl_connect('button_press_event', self.temporal_click)
        self.temporalwindow.show()

    def partition_subjects(self):
        self.partitioned_recs = []
        max_recs = 0
        for sub in self.subjects:
            sub_recs = []
            temp_recs = []
            for rec in sub.recordings:
                temp_recs.append(rec)
            while len(temp_recs) > 0:
                yearly_recs = []
                min_rec = temp_recs[0]
                min_start = datetime.timestamp(min_rec.start_of_recording)
                for rec in temp_recs:
                    start = datetime.timestamp(rec.start_of_recording)
                    if start < min_start:
                        min_rec = rec
                        min_start = start
                yearly_recs.append(min_rec)
                temp_recs.remove(min_rec)
                for rec in temp_recs:
                    start = datetime.timestamp(rec.start_of_recording)
                    if start < min_start + self.timescale_int:
                        yearly_recs.append(rec)
                        temp_recs.remove(rec)
                sub_recs.append(yearly_recs)
            self.partitioned_recs.append(sub_recs)
        for sub_recs in self.partitioned_recs:
            if len(sub_recs) > max_recs:
                max_recs = len(sub_recs)
        for sub_recs in self.partitioned_recs:
            if len(sub_recs) < max_recs:
                m = max_recs - len(sub_recs)
                for i in range(m):
                    sub_recs.append([])
                
    def __updateValuesOfSlider(self):
        maximum = len(self.partitioned_recs[0])
        self.Slider.setMinimum(0)
        self.Slider.setMaximum(maximum-1)
        self.sliderValue.setText("Timescale: " + self.timescale)

    def __onsldValueChanged(self):
        self.EventsCheckbox.setChecked(True)
        self.event_plots.clear()
        for i in range(len(self.subplots)):
            self.subplots[i].clear()

        #plotting the recordings
        custom_cycler = (cycler(color=['dodgerblue','mediumblue']))
        i = 0
        for sub_recs in self.partitioned_recs:
            self.subplots[i].set_prop_cycle(custom_cycler)
            for rec in sub_recs[self.Slider.value()]: 
                start = datetime.timestamp(rec.start_of_recording)
                stop = rec.duration_sec + start      
                self.subplots[i].plot([start, stop], [0, 0],linewidth=10) 
            i += 1

        #plotting the events
        custom_cycler = (cycler(color=['darkorange','gold']))
        i = 0
        k = 0
        for sub_recs in self.partitioned_recs:
            self.subplots[i].set_prop_cycle(custom_cycler)
            for rec in sub_recs[self.Slider.value()]:
                start = datetime.timestamp(rec.start_of_recording)
                for ann in rec.annotations:
                    for event in ann.events:
                        ev_start = event.start + start
                        ev_stop = event.stop + start
                        self.event_plots[k] = self.subplots[i].plot([ev_start, ev_stop], [0, 0],linewidth=15, alpha = 0.5)
                        k += 1
            i += 1

        #ax[idx].axis('off')   
        for i in range(len(self.subjects)):
            self.subplots[i].axes.set_ylim([-1,1])
            self.subplots[i].spines["top"].set_visible(False)
            self.subplots[i].spines["right"].set_visible(False)
            self.subplots[i].spines["bottom"].set_visible(False)
            self.subplots[i].spines["left"].set_visible(False)
            self.subplots[i].set_yticks([])
            self.subplots[i].set_xticks([])
            self.subplots[i].set_ylabel(self.subject_names[i],rotation='horizontal', ha='right',va="center")
            self.subplots[i].axhline(y=0, color="royalblue", alpha = 0.9,linestyle="--")
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
            verbose:bool = True
            agplot(self.clicked_recording, window, start, y, title,fs,sens,channel_names, callback, verbose, self)

    def temporal_click(self, event):
        if event.inaxes is not None:
            index = self.subject_names.index(event.inaxes.get_ylabel())
            self.clicked_subject = self.subjects[index]
            self.openRecording_temporal(event.xdata)

    def drawTemporal(self):
        k = 0
        for i in range(len(self.subjects)):
            self.subplots[i] = self.TemporalPlot.canvas.add(cols = 1)
        #plotting the recordings
        custom_cycler = (cycler(color=['dodgerblue','mediumblue']))
        i = 0
        for sub_recs in self.partitioned_recs:
            self.subplots[i].set_prop_cycle(custom_cycler)
            for rec in sub_recs[self.Slider.value()]:
                start = datetime.timestamp(rec.start_of_recording)
                stop = rec.duration_sec + start      
                self.subplots[i].plot([start, stop], [0, 0],linewidth=10) 
            i += 1
 
        #plotting the events
        custom_cycler = (cycler(color=['darkorange','gold']))
        i = 0
        for sub_recs in self.partitioned_recs:
            self.subplots[i].set_prop_cycle(custom_cycler)
            for rec in sub_recs[self.Slider.value()]:
                start = datetime.timestamp(rec.start_of_recording)
                for ann in rec.annotations:
                    for event in ann.events:
                        ev_start = event.start + start
                        ev_stop = event.stop + start
                        self.event_plots[k] = self.subplots[i].plot([ev_start, ev_stop], [0, 0],linewidth=15, alpha = 0.5)
                        k += 1
            i += 1 
        
        #ax[idx].axis('off')    
        for i in range(len(self.subjects)):
            self.subplots[i].axes.set_ylim([-1,1])
            self.subplots[i].spines["top"].set_visible(False)
            self.subplots[i].spines["right"].set_visible(False)
            self.subplots[i].spines["bottom"].set_visible(False)
            self.subplots[i].spines["left"].set_visible(False)
            self.subplots[i].set_yticks([])
            self.subplots[i].set_xticks([])
            self.subplots[i].set_ylabel(self.subject_names[i],rotation='horizontal', ha='right',va="center")
            self.subplots[i].axhline(y=0, color="royalblue", alpha = 0.9,linestyle="--")
    
    def event_checked(self, is_checked):
        if is_checked:
            for i in range(len(self.event_plots)):
                self.event_plots[i][0].set_visible(True)
        else:
            for i in range(len(self.event_plots)):
                self.event_plots[i][0].set_visible(False)
        self.TemporalPlot.canvas.draw_idle()