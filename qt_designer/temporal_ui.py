from qt_designer.temporal_view import Ui_TemporalView
from PyQt5 import QtCore, QtGui, QtWidgets
from databasemanager import *
from cycler import cycler
from datetime import datetime


class temporal_ui(Ui_TemporalView):
    def __init__(self):
        self.temporalwindow = QtWidgets.QMainWindow()
        self.setupUi(self.temporalwindow)
        self.Slider.setMaximum(100)
        self.Slider.setMinimum(0)
        self.subjects = []
        self.Slider.valueChanged.connect(self.__onsldValueChanged)
        self.EventsCheckbox.toggled.connect(self.event_checked)
        self.EventsCheckbox.setChecked(True)
        self.temporalwindow.show()
        self.event_plots = {}

    def __onsldValueChanged(self):
        self.UpdateSampleIndex(self.Slider.value())
    
    def UpdateSampleIndex(self, SampleIndex):
        pass

    def drawTemporal(self, subjects, names):
        self.subjects = subjects
        self.subplots = {}
        i = 0
        for  idx, sub in enumerate(subjects):
            self.subplots[idx] = self.TemporalPlot.canvas.add(cols = 1)
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
            self.subplots[idx].set_ylabel(names[idx],rotation='horizontal', ha='right',va="center")


    def event_checked(self, is_checked):
        if is_checked:
            i = 0
            for  idx, sub in enumerate(self.subjects):
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
        self.TemporalPlot.canvas.draw_idle()