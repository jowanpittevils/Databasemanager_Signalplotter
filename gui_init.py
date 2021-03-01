#%%
#%reload_ext autoreload
#%autoreload 2
#%%
from PyQt5 import QtCore, QtGui, QtWidgets
from base_GUI import Ui_MainWindow
from PyQt5.uic import loadUi
from databasemanager import *
import sys
from dataset_selector import Ui_dataset 



class gui_init(QtWidgets.QMainWindow,Ui_MainWindow):
    
    UserSettings.global_settings().loading_data_missing_channel_type = 'error'
    UserSettings.global_settings().loading_data_channels = ['fp1','fp2','t3','t4','o1','o2','c3','c4']
 
    root = 'C:\\db\\toyDB'
    db = Database(root)
    datasets = db.dataset_names
    ds = db.load_dataset('all')
    dataset_name = ""
    #subject = []
    #recording = []
    #annotation = []
    #event = []
    matching_subjects = []
    

    
    def __init__(self):
        super(gui_init, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.Dataset_label.clicked.connect(self.get_dataset)
        self.ui.lineEdit.textChanged.connect(self.update_subject_list)
        self.ui.subject_list.currentItemChanged.connect(self.update_recording_list)
        #self.ui.recordings_list.itemDoubleClicked.connect(self.update_annotation_list)
        #self.ui.annotations_list.itemDoubleClicked.connect(self.update_event_list)
    

    def clear_GUI(self):
        self.ui.subject_list.clear()
        self.ui.recordings_list.clear()
        self.ui.annotations_list.clear()
        self.ui.events_list.clear()

    def update_GUI(self):
        subject_names = self.ds.subject_names
        annotations = ['annotation1','annotation2', 'annotation3', 'annotation4']
        events = ['event1','event2']
        recordings = []
        subjects = self.ds.subjects
        for i in range(len(subjects)):
            for rec in subjects[i].recordings:
                recordings.append(rec.name)
        self.clear_GUI()
        self.ui.subject_list.addItems(self.matching_subjects)
        self.ui.recordings_list.addItems(recordings)
        self.ui.annotations_list.addItems(annotations)
        self.ui.events_list.addItems(events)
        self.ui.label_11.setText(self.dataset_name)
        self.ui.lineEdit.start(subject_names)

    def update_subject_list(self):
        self.matching_subjects = [s for s in self.ds.subject_names if self.ui.lineEdit.text() in s]
        self.update_GUI()


    def update_recording_list(self, item):
        if item is not None:
            sub = item.text()
            index = self.ds.subject_names.index(sub)
            recordings = []
            for i in range(len(self.ds.subjects[index])):
                recordings.append(self.ds.subjects[index].recordings[i].name)
            self.ui.recordings_list.clear()
            self.ui.recordings_list.addItems(recordings)


    # def update_annotation_list(self, item):
    #     recording = item.text()
    #     index = self.subject.recordings.index(recording)
    #     self.recording = self.subject.recordings[index]
    #     annotations = []
    #     self.ui.annotations_list.clear()
    #     for i in range
    #     self.ui.annotations_list.addItems()
    
    # def update_event_list(self,item):
    #     annotation = item.text()
    #     index = self.ds.subjects.recordings.annotations.index(annotation)
    #     self.ui.events_list.clear()
    #     self.ui.events_list.additems()
    
    def load_dataset(self):
        self.ds = self.db.load_dataset(self.dataset_name)
        self.matching_subjects = [subject for subject in self.ds.subject_names if self.ui.lineEdit.text() in subject]
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

        










app = QtWidgets.QApplication(sys.argv)
w = gui_init()
w.show()
sys.exit(app.exec_())