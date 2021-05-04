from PyQt5 import QtWidgets, QtCore
from databasemanager import *
from database_explorer_plotter.database_ui import database_ui
import sys

QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
if hasattr(QtWidgets.QStyleFactory, "AA_UseHighDpiPixmaps"):
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps)
app = QtWidgets.QApplication(sys.argv)
w = database_ui()
w.show()
sys.exit(app.exec_()) 