from PyQt5 import QtCore, QtGui, QtWidgets
from gui_init import gui_init
from os import path

import sys
import numpy as np
import math
import numbers
import matplotlib.pyplot as plt
from PyQt5.QtCore import QFile, QTextStream
from PyQt5.QtGui import QPalette, QIcon
from PyQt5.QtGui import QKeySequence, QPalette, QColor
from PyQt5.QtCore import Qt, QSize

def database_browser(Database):
    app = QtWidgets.QApplication(sys.argv)
    ui = gui_init()
    ui.db = Database
    ui.load_database()
    ui.show()
    app.exec_()

