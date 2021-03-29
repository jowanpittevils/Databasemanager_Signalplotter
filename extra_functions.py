from PyQt5 import QtCore, QtGui, QtWidgets
from database_ui import database_ui
from load_ui import load_ui
from os import path
from qt_designer.temporal_ui import temporal_ui
from databasemanager import *
from database_ui import database_ui


import sys
import numpy as np
import math
import numbers
import matplotlib.pyplot as plt
from PyQt5.QtCore import QFile, QTextStream
from PyQt5.QtGui import QPalette, QIcon
from PyQt5.QtGui import QKeySequence, QPalette, QColor
from PyQt5.QtCore import Qt, QSize


def load_browser():
    app = QtWidgets.QApplication(sys.argv)
    ui = load_ui()
    ui.show()
    app.exec_()



def database_browser(Database):
    app = QtWidgets.QApplication(sys.argv)
    ui = database_ui()
    ui.db = Database
    ui.load_database()
    ui.show()
    app.exec_()




# def temporal_browser(timescale, dataset, subjects=None):

#     ui3 = temporal_ui()
#     ui3.drawTemporal(subjects, subject_names)
#     ui3.TemporalPlot.canvas.mpl_connect('button_press_event', temporal_click)



