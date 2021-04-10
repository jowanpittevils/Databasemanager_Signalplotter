from PyQt5 import QtCore, QtGui, QtWidgets
from databasemanager import *
from configparser import ConfigParser
from database_explorer.database_ui import database_ui
import sys

app = QtWidgets.QApplication(sys.argv)
w = database_ui()
w.show()
sys.exit(app.exec_())