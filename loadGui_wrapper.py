#%%
#%reload_ext autoreload
#%autoreload 2
#%%
from PyQt5 import QtCore, QtGui, QtWidgets
from import_GUI import Ui_MainWindow
from PyQt5.uic import loadUi
from databasemanager import *
import sys
from dataset_selector import Ui_dataset 
from GUI_wrapper import GUI_wrapper

 

class loadGUI_wrapper(QtWidgets.QMainWindow,Ui_MainWindow):

        

        def __init__(self):
                super(loadGUI_wrapper, self).__init__()
                self.ui = Ui_MainWindow()
                self.ui.setupUi(self)

                self.ui.browse1.clicked.connect(self.browsefolder1)
                self.ui.browse2.clicked.connect(self.browsefolder2)

                self.ui.dataset_list.itemClicked.connect(self.get_ds)

                #self.ui.Load.clicked.connect(self.load_dataset)


        def browsefolder1(self):
                folder = QtWidgets.QFileDialog.getExistingDirectory(self, "Select Directory")
                self.ui.db_name.setText(folder)  
                db = Database(folder)
                datasets = db.dataset_names
                self.ui.dataset_list.clear()
                self.ui.dataset_list.addItems(datasets)
                               

        def browsefolder2(self):
                folder = QtWidgets.QFileDialog.getExistingDirectory(self,"Select Directory")
                self.ui.ds_name.setText(folder)
                db = Database(folder)
                datasets = db.dataset_names
                self.ui.dataset_list.clear()
                self.ui.dataset_list.addItems(datasets)


        def load_dataset(self):
                print(self.get_ds)
                ds = self.ui.dataset_list
                
                
                # self.ds = self.db.load_dataset(self.dataset_name)
                
        def get_ds(self, item):
                print(item.text())


app = QtWidgets.QApplication(sys.argv)
w = loadGUI_wrapper()
w.show()
sys.exit(app.exec_())