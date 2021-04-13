from PyQt5 import QtCore, QtGui, QtWidgets
from database_ui import database_ui
from load_ui import load_ui
from os import path
from qt_designer.temporal_new import temporal_ui
from databasemanager import *
from database_ui import database_ui
from datetime import datetime

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


def temporal_browser(Database, subjects=None, timescale = 'year'):
    app = QtWidgets.QApplication(sys.argv)
    ui3 = temporal_ui(Database, subjects, timescale)
    app.exec_()

root = 'C:\\db\\toyDB'
db = Database(root)


temporal_browser(db, ['tr_ar_77', 'tr_ar_254', 'tr_ar_492'], 'day')

