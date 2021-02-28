from PyQt5 import QtCore, QtGui, QtWidgets
from base_GUI import Ui_MainWindow
from databasemanager import *
from dataset_selector import Ui_dataset


class GUI_wrapper(Ui_MainWindow):

    UserSettings.global_settings().loading_data_missing_channel_type = 'error'
    UserSettings.global_settings().loading_data_channels = ['fp1','fp2','t3','t4','o1','o2','c3','c4']
 
    root = 'C:\\db\\toyDB'
    db = Database(root)
    datasets = db.dataset_names
    ds = db.load_dataset('ds1')
    dataset_name = ""
    

    def clear_GUI(self):
        self.subject_list.clear()
        self.recordings_list.clear()
        self.annotations_list.clear()
        self.events_list.clear()

    def update_GUI(self):
        subject_names = self.ds.subject_names
        annotations = ['annotation1','annotation2', 'annotation3', 'annotation4']
        events = ['event1','event2']
        recordings = []
        subjects = self.ds.subjects
        for rec in subjects[1].recordings:
            recordings.append(rec.name)
        self.clear_GUI()
        self.subject_list.addItems(subject_names)
        self.recordings_list.addItems(recordings)
        self.annotations_list.addItems(annotations)
        self.events_list.addItems(events)
        self.label_11.setText(self.dataset_name)
        self.lineEdit.start(subject_names)

    def update_subject_list(self):
        print(self.lineEdit.text())
        print('updating...')

    def load_dataset(self):
        self.ds = self.db.load_dataset(self.dataset_name)
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

    


