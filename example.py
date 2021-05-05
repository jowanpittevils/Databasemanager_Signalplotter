from PyQt5 import QtWidgets
from databasemanager import *
from database_explorer_plotter.database_ui import database_ui
import sys

app = QtWidgets.QApplication(sys.argv)
w = database_ui()
w.show()
sys.exit(app.exec_())
