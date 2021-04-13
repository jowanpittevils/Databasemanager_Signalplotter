#%%
#%reload_ext autoreload
#%autoreload 2
#%%
from PyQt5 import QtCore, QtGui, QtWidgets
from qt_designer.import_GUI import Ui_LoadWindow
from PyQt5.uic import loadUi
from databasemanager import *
import sys
from qt_designer.dataset_selector import Ui_dataset 
from database_explorer_plotter.database_ui import *
from os import path

 

class load_ui(QtWidgets.QMainWindow,Ui_LoadWindow):

        def __init__(self):
                super(load_ui, self).__init__()
                self.ui = Ui_LoadWindow()
                self.ui.setupUi(self)
                self.__AssignCallbacks()
                self.show()

        def __AssignCallbacks(self):
                self.ui1 = database_ui()
                self.ui.browse1.clicked.connect(self.browsefolder1)
                self.ui.browse2.clicked.connect(self.browsefolder2)
                self.ui.dataset_list.itemClicked.connect(self.get_ds)
                self.ui.load.clicked.connect(self.load_dataset)
                self.ui.load.clicked.connect(self.close)

        def browsefolder1(self):
                self.ui1.root = QtWidgets.QFileDialog.getExistingDirectory(self, "Select Database folder")        
                if path.exists(self.ui1.root + '/Data') == False:
                        self.import_error() 
                else:
                        self.ui.db_name.setText(self.ui1.root)
                        self.ui1.config.set('database', 'root', self.ui1.root)
                        with open('config.ini', 'w') as f:
                                self.ui1.config.write(f)
                        self.ui1.data_root = self.ui1.root + '/Data'
                        if path.exists(self.ui1.root + '/Datasets') == False:
                                self.import_error()
                        else:
                                self.ui.ds_name.setText(self.ui1.root + '/Datasets')
                                self.ui1.db = Database(self.ui1.root) 
                                self.ui1.datasets = self.ui1.db.dataset_names
                                self.ui.dataset_list.clear()
                                self.ui.dataset_list.addItems(self.ui1.datasets)
                                
        def browsefolder2(self):
                if self.ui1.root == '':
                        self.import_error()
                else:
                        self.ui1.ds_root = QtWidgets.QFileDialog.getExistingDirectory(self,"select 'datasets' folder")
                        self.ui1.db = Database(None, self.ui1.data_root, self.ui1.ds_root)
                        self.ui1.datasets = self.ui1.db.dataset_names
                        if len(self.ui1.datasets) == 0:
                                self.import_error()
                        else:
                                self.ui.ds_name.setText(self.ui1.ds_root)
                                self.ui.dataset_list.clear()
                                self.ui.dataset_list.addItems(self.ui1.datasets)

        def load_dataset(self): 
                self.ui1.ds = self.ui1.db.load_dataset(self.ui1.ds)
                self.ui1.dataset_name = self.ui1.ds.name
                self.ui1.matching_subjects = [subject for subject in self.ui1.ds.subject_names if self.ui1.ui.lineEdit.text() in subject]
                self.ui1.update_GUI()
                self.ui1.show()

        def get_ds(self, item):
                self.ui1.ds = item.text()
                self.ui1.config.set('database','dataset', item.text())
                with open('config.ini', 'w') as f:
                        self.ui1.config.write(f)

        def import_error(self):
                self.msg = QtWidgets.QMessageBox()
                self.msg.setWindowTitle("Error")
                self.msg.setIcon(QtWidgets.QMessageBox.Warning)
                self.browse = self.msg.addButton("Browse", QtWidgets.QMessageBox.YesRole)
                self.msg.addButton(QtWidgets.QPushButton("Cancel"), QtWidgets.QMessageBox.NoRole)

                if path.exists(self.ui1.root + '/Data') == False:
                        if path.exists(self.ui1.root) == False:
                                self.msg.setText("Select database folder first")
                                self.browse.clicked.connect(self.browsefolder1)
                                x = self.msg.exec_()

                        else:
                                self.msg.setText("No 'Data' folder found")
                                self.browse.clicked.connect(self.browsefolder1)
                                self.ui.db_name.clear()
                                self.ui.ds_name.clear()
                                self.ui.dataset_list.clear()
                                x = self.msg.exec_()

                else:
                        self.msg.setText("No 'Datasets' folder found")
                        self.browse.clicked.connect(self.browsefolder2)
                        self.ui.ds_name.clear()
                        self.ui.dataset_list.clear()
                        x = self.msg.exec_()
                     


if __name__ == "__main__":
        app = QtWidgets.QApplication(sys.argv)
        w = load_ui()
        sys.exit(app.exec_())