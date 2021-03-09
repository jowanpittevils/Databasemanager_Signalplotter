from PyQt5 import QtCore, QtGui, QtWidgets
from qt_designer.import_GUI import Ui_LoadWindow
from qt_designer.import_error import Ui_import_error
from PyQt5.uic import loadUi
from databasemanager import *
import sys
from qt_designer.dataset_selector import Ui_dataset 
from gui_init import *
from os import path
from gui_init import *

def database_browser(Database):
    app = QtWidgets.QApplication(sys.argv)
    ui = gui_init()
    ui.db = Database
    ui.load_database()
    ui.show()
    sys.exit(app.exec_())



