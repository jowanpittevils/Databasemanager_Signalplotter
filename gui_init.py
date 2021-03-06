#%%
#%reload_ext autoreload
#%autoreload 2
#%%
import numpy as np
import math
import numbers
import matplotlib.pyplot as plt
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

    def openRecording(self, item):
    
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

        self.cplot(data, window, title,fs,sens,channel_names, callback, channel_first, verbose)


    def openTemporal(self):
        subjects = self.matching_subjects
        data = {}
        for  sub in ds.subjects:
            sum = 0
            for rec in sub.recordings:
                sum += rec.duration_sec
                data[sub.name] = sum
        print(data)
        values = list(data.values())
        names = list(data.keys())

        fig, ax = plt.subplots()
        ax.barh(names, values)

        plt.show()

        

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


    def cplot(self, x=None, window=30, title=None,fs=1,sens=None,channel_names=None, callback=None, channel_first:bool = True, verbose:bool = True):
        '''
        It plots continious signals by spliting into smaller segments and calling gplot.
        It may add zeros to the end of signals for the last segment. 
        - inputs:
            -- x:           The inout tensore. Its dimension should be as (K: Channel, T: Time-samples) if channel_first is True. Otherwise, as (T, K), for instance (3600s * 250 hz, 20 channels).
                            If it has only one dimension, it is assumed to be temporal samples of a single channel signal.
                            It is also possible to pass x1,x2,x3,x4,... for different channels. in this case x must be None.
            -- window:      optional, the length of signal in seconds to be shown in each window frame.        
            --other inputs are as gplot
        '''
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

        if(type(x) != list):
            x=[x]
        x = prepare_x(x, window, fs, channel_first)
        return self.gplot(x=x, y=None, title=title, fs=fs, sens=sens,channel_names=channel_names, callback=callback, channel_first=True, verbose=verbose)


    def gplot(self, x, y=None, title=None,fs=1,sens=None,channel_names=None, callback=None, channel_first:bool = True, verbose:bool = True):
        '''
        gplot (graphical UI-plot) is a function for visualizing tensors of multichannel timeseries such as speech, EEG, ECG, EMG, EOG. 
        - inputs:
            -- x:           the inout tensore. Its dimension should be as (S: Segments, K: Channel, T: Time-samples) (the same as the default dimension of Keras) if channel_first is True. Otherwise, as (S, T, K).
                            for instance (200 segments, 10s * 250 hz, 20 channels)
            -- y:           optional, the labels of segments. It must be a vector with size of S.
            -- title:       optional, the tile of the window.
            -- fs:          optional [default is None], the sampling frequensy. If fs is None the data will be plotted in samples, otherwise in seconds. 
                            if fs is -1, then the mean of signal on the Time mode will be plotted with a bar graph. 
            -- sens:        optional [default is None], normalizing factor. If it is None, the signals will be normalize automatically with the min and max of each channel in each segment.
            -- channel_names:optional [default is None], the name of channels to be plotted on the y-axis.
            -- callback:    optional [default is None], a function as func(x, sampleIndex) to be called when the user change the sample index by the GUI.
            -- channel_first: optional it defines if channel is before or after the time in the dimensions of the given x tensor.
            -- verbose: optional, if it is true, it logs the changes in the GUI; otherwise it is silent.
            * in order to plot tensors on top of each other (holding on) in the linePlot mode or barPlotMode, use x as List in List: [[x]] (see example 4)
            
        - output: list of selected indexes (as favorite)
        
        - examples: 'x=numpy.random.randn(15,fs*10,20)'
                gplot(x)
                gplot(x,title='title', sens=10)
                fav=gplot(x, y=y,title=title, fs=fs, channel_names=chn)
                
                * Bar graph, fs=-1
                gplot([x4,x4/2,x4*3], fs=-1)

                * Plot holded graphs '[[]]'
                gplot([[x,x/2,x*3]])
                gplot([[x,x/2,x*3]], fs=-1)

                * plot linked graphs '[]'
                gplot([x1,x2,x3], y=y,title=[title1, title2, title3], fs=[fs1,fs2,fs3], channel_names=[chn1,chn2,chn3])
                gplot([x1,x2,x3], y=y,title=[title1, None, title3], fs=fsAll, channel_names=[chn1,None,None])
                gplot([x1,x2,[x3 , x4]], y=y,title=[title1, None, title3], fs=[fs1,fs2,-1], channel_names=[chn1,None,None])
        '''

        self.countainer = plotter_countainer()
        if(type(x) != list):
            x=[x]
        N = len(x)
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

        N = len(x)
        for i in range(N):
            self.countainer.add(x[i],y,title[i],fs[i],sens[i],channel_names[i],callback[i], channel_first, verbose)



        return self.countainer.getFavorites()


root = 'C:\\db\\toyDB'
db = Database(root)
datasets = db.dataset_names
ds = db.load_dataset('ds1')
print(ds.subjects[0].recordings[0].duration_sec)
print(ds.subjects[0].recordings[0].duration_str)

print(type(ds.subjects[0].recordings[0].duration_sec))
print(type(ds.subjects[0].recordings[0].duration_str))




if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    w = gui_init()
    w.root = 'C:\\db\\toyDB'
    w.db = Database(w.root)
    w.datasets = w.db.dataset_names
    w.ds = w.db.load_dataset('all')
    w.show()
    sys.exit(app.exec_())