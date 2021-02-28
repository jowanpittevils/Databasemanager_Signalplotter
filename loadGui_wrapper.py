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

 

class loadGUI_wrapper(QtWidgets.QMainWindow,Ui_MainWindow):

        

        def __init__(self):
                super(loadGUI_wrapper, self).__init__()
                self.ui = Ui_MainWindow()
                self.ui.setupUi(self)

                self.ui.browse1.clicked.connect(self.browsefolder1)
                self.ui.browse2.clicked.connect(self.browsefolder2)

                self.ui.Load.clicked.connect(self.load_dataset)


        def update_GUI(self):
                db = Database(str(self.ui.ds_name))
                datasets = db.dataset_names
                self.ui.dataset_list.addItems(datasets)


        def browsefolder1(self):
                folder = QtWidgets.QFileDialog.getExistingDirectory(self, "Select Directory")
                self.ui.db_name.setText(folder)  
                db = str(folder)
                print(db) 
                self.update_GUI()               

        def browsefolder2(self):
                folder = QtWidgets.QFileDialog.getExistingDirectory(self,"Select Directory")
                self.ui.ds_name.setText(folder)
                self.update_GUI()

        def load_dataset(self):
                self.update_GUI()
                self.ds = self.db.load_dataset(self.dataset_name)
                

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
w = loadGUI_wrapper()
w.show()
sys.exit(app.exec_())