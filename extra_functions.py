from PyQt5 import QtCore, QtGui, QtWidgets
from gui_init import *
from os import path

def database_browser(Database):
    app = QtWidgets.QApplication(sys.argv)
    ui = gui_init()
    ui.db = Database
    ui.load_database()
    ui.show()
    app.exec_()



