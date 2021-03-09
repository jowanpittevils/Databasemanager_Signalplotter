#%%
#%reload_ext autoreload
#%autoreload 2
#%%
from PyQt5 import QtCore, QtGui, QtWidgets
from qt_designer.import_GUI import Ui_LoadWindow
from qt_designer.import_error import Ui_import_error
from PyQt5.uic import loadUi
from databasemanager import *
import sys
from qt_designer.dataset_selector import Ui_dataset 
from gui_init import *
from os import path

 

class loadGUI_init(QtWidgets.QMainWindow,Ui_LoadWindow):

        

        def __init__(self):
                super(loadGUI_init, self).__init__()
                self.ui = Ui_LoadWindow()
                self.ui.setupUi(self)

                self.ui1 = gui_init()

                self.ui.browse1.clicked.connect(self.browsefolder1)
                self.ui.browse2.clicked.connect(self.browsefolder2)

                self.ui.dataset_list.itemClicked.connect(self.get_ds)

                self.ui.Load.clicked.connect(self.load_dataset)


        def browsefolder1(self):
                self.ui1.root = QtWidgets.QFileDialog.getExistingDirectory(self, "Select Database folder")        
                if path.exists(self.ui1.root + '/Data') == False:
                        self.import_error()   
                if path.exists(self.ui1.root + '/Datasets') == False:
                        self.ui1.data_root = self.ui1.root + '/Data'
                        self.ui.db_name.setText(self.ui1.root)
                        self.import_error() 
                else:
                        self.ui.db_name.setText(self.ui1.root)  
                        self.ui1.db = Database(self.ui1.root) 
                        self.ui1.datasets = self.ui1.db.dataset_names
                        self.ui.dataset_list.clear()
                        self.ui.dataset_list.addItems(self.ui1.datasets)
                               

        def browsefolder2(self):
                self.ui1.ds_root = QtWidgets.QFileDialog.getExistingDirectory(self,"select 'datasets' folder")
                self.ui.ds_name.setText(self.ui1.ds_root)
                self.ui1.db = Database(None, self.ui1.data_root, self.ui1.ds_root)
                self.ui1.datasets = self.ui1.db.dataset_names
                if len(self.ui1.datasets) == 0:
                        self.import_error()
                self.ui.dataset_list.clear()
                self.ui.dataset_list.addItems(self.ui1.datasets)


        def load_dataset(self): 
                self.ui1.ds = self.ui1.db.load_dataset(self.ui1.ds)
                self.ui1.matching_subjects = [subject for subject in self.ui1.ds.subject_names if self.ui1.ui.lineEdit.text() in subject]
                self.ui1.update_GUI()
                #self.ui1.label_11.setText(self.get_ds)
                self.ui1.show()

        def get_ds(self, item):
                self.ui1.ds = item.text()


        def import_error(self):
                self.myOtherWindow = QtWidgets.QMainWindow()
                self.ui2 = Ui_import_error()
                self.ui2.setupUi(self.myOtherWindow)
                if path.exists(self.ui1.root + '/Data') == False:
                        self.ui2.label.setText("No 'Data' folder found")
                        self.ui2.pushButton.clicked.connect(self.browsefolder1)
                else:
                        self.ui2.label.setText("No 'Datasets' folder found")
                        self.ui2.pushButton.clicked.connect(self.browsefolder2)            
                self.myOtherWindow.show()
                
 
 


app = QtWidgets.QApplication(sys.argv)
w = loadGUI_init()
w.show()
sys.exit(app.exec_())