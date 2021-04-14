from PyQt5 import QtCore, QtGui, QtWidgets
from  database_explorer_plotter.database_ui import database_ui
from load_ui import load_ui
from os import path
from qt_designer.temporal_new import temporal_ui
from databasemanager import *
from custom_plotter.plotter import cplot

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
    """
    Opens the load explorer which enables the user to browse through files to select a database and the corresponding datasets in case none are provided in the database.  
    After loading the database with datasets, the user is able to click on one of the datasets which leads to the second window, the database explorer.
    """
    app = QtWidgets.QApplication(sys.argv)
    ui = load_ui()
    ui.show()
    app.exec_()


def database_browser(Database):
    """
    Opens the database explorer which enables the user to orderly navigate through the database, showing all information (subjects, recordings, annotations and events). 
    The database explorer does the following:
    -   opens a temporal view of the dataset which optionally shows events and annotations
    -   Change datasets
    -   Open a recording in a new window using matplotlib by double-clicking it
    -   Open an event in a new window by double-clicking it
    -   Search for specific subjects, recordings or events
    -   Have a summary button that displays the most important information regarding the currently selected dataset (sampling frequency, channels,...
    
    Parameters:
    ----------
    Database:  from the class 'database' in the package 'databasemanager'.
    e.g.
    1) db = Database('c:\\sleep')
    2) db = Database(Path('c:\\sleep')) # Path: from databasemanager.classes.path import Path
    2) db = Database(root = 'c:\\sleep')
    3) db = Database(root = None, data_path = 'c:\\sleep\\Data', datasets_path = 'c:\\sleep\\Datasets')
    """
    app = QtWidgets.QApplication(sys.argv)
    ui = database_ui()
    ui.db = Database
    ui.load_database()
    ui.show()
    app.exec_()


def temporal_browser(Database, subjects=None, timescale = 'year'):
    """
    Opens a temporal window of the given subjects from a certain database with a specified timescale.
    The temporal window shows the recordings and events of the subjects situated relative to each other in the specified timescale.
    
    Parameters:
    ----------
    Database:   see above.
    subjects:   A list of strings of the names of the subjects to be shown in the temporal window. (Default is None which shows a temporal window 
                of all the subjects in the given database) 
    timescale:  A string which shows the recordings and events in that timescale situated from each other. 
                inputs can be: 'day', 'week', 'month and 'year' (Default is 'year')

    e.g. temporal_browser(Database('C:\\db'), ['tr_ar_77', 'tr_ar_254', 'tr_ar_492'], 'day')
    """
    app = QtWidgets.QApplication(sys.argv)
    ui3 = temporal_ui(Database, subjects, timescale)
    app.exec_()


def plot_browser(recording, window=30, start_event=None, title=None,fs=1,sens=None,channel_names=None, callback=None, channel_first:bool = True, verbose:bool = True):
    """
    Opens a recording in the plot explorer for visualizing tensors of multichannel timeseries such as speech, EEG, ECG, EMG, EOG. 
    It plots continious signals by sampling the data of the given recording.
    
    Parameters:
    ----------
        -- recording:   the recording to be plotted
        -- window:      optional, the length of signal in seconds to be shown in each window frame.
                        for instance (200 segments, 10s * 250 hz, 20 channels)
        -- start_event: plots the recording at the start of the given event.
        -- y:           optional, the labels of segments. It must be a vector with size of S.
        -- title:       optional, the tile of the window.
        -- fs:          optional [default is None], the sampling frequensy. If fs is None the data will be plotted in samples, otherwise in seconds. 
                        if fs is -1, then the mean of signal on the Time mode will be plotted with a bar graph. 
        -- sens:        optional [default is None], normalizing factor. If it is None, the signals will be normalize automatically with the min and max of each channel in each segment.
        -- channel_names:optional [default is None], the name of channels to be plotted on the y-axis.
        -- callback:    optional [default is None], a function as func(x, sampleIndex) to be called when the user change the sample index by the GUI.
        -- channel_first: optional it defines if channel is before or after the time in the dimensions of the given x tensor.
        -- verbose: optional, if it is true, it logs the changes in the GUI; otherwise it is silent.
        
    - output: list of selected indexes (as favorite)
    """
    cplot(window, start_event, title, fs, sens, channel_names, callback, channel_first, verbose)



root = 'C:\\db\\toyDB'
db = Database(root)


temporal_browser(db, ['tr_ar_77', 'tr_ar_254', 'tr_ar_492'], 'day')

