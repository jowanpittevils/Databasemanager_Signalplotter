from custom_plotter.plotter_ui import plotter_ui
import matplotlib.pyplot as plt
import numpy as np
import math
import numbers
from databasemanager import *
import os, psutil
from PyQt5 import QtWidgets


class plotter_countainer():
    def __init__(self):
        self.plotterList = {}
        pass

    def add(self, recording, window, start_event=None, y=None, title=None,fs=1,sens=None,channel_names=None, callback=None, channel_first=True, verbose=True):
        MainWindow = QtWidgets.QMainWindow()
        plotter = plotter_ui(MainWindow=MainWindow,  recording=recording, window=window, start_event=start_event, y=y, title=title, fs=fs, sens=sens, channelNames=channel_names, callback=callback, channelFirst=channel_first, verbose=verbose)
        MainWindow.showMaximized()

        self.plotterList.update( {plotter.ID: plotter})
        plotter.IndexChanged.connect(self.__updateALL)
        
    def __updateALL(self, senderID, currentIndex):
        for k,pl in self.plotterList.items():
            if(k == senderID):
                continue
            else:
                pl.UpdateSampleIndex(currentIndex, rePlot=True, triggeredSignals = False)
    
    def getFavorites(self):
        favoriteList = {}
        for k,pl in self.plotterList.items():
            favoriteList.update({k: pl.FavoriteList})
            if(len(self.plotterList)==1):
                return pl.FavoriteList
        return favoriteList


def cplot(self, recording, window=30, start_event=None, title=None,fs=1,sens=None,channel_names=None, callback=None, channel_first:bool = True, verbose:bool = True):
    '''
    It plots continious signals by sampling the data of the given recording and calling gplot.
    It may add zeros to the end of signals for the last window. 
    - inputs:
        -- recording:   the recording to be plotted
        -- window:      optional, the length of signal in seconds to be shown in each window frame.
        -- start_event: plots the recording at the start of the given event.        
        --other inputs are as gplot
    '''
    return gplot(self, recording=recording, window = window, start_event=start_event, y=None, title=title, fs=fs, sens=sens,channel_names=channel_names, callback=callback, channel_first=True, verbose=verbose)


def gplot(self, recording, window, start_event=None, y=None, title=None,fs=1,sens=None,channel_names=None, callback=None, channel_first:bool = True, verbose:bool = True):
    '''
    gplot (graphical UI-plot) is a function for visualizing tensors of multichannel timeseries such as speech, EEG, ECG, EMG, EOG. 
    - inputs:
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
    
    TODO:
    - examples: 'x=numpy.random.randn(15,fs*10,20)'
            gplot(x)
            gplot(x,title='title', sens=10)
            fav=gplot(x, y=y,title=title, fs=fs, channel_names=chn)
            
            * Bar graph, fs=-1
            gplot([x4,x4/2,x4*3], fs=-1)

            * Plot holded graphs '[[]]'
            gplot([[x,x/2,x*3]])
            gplot([[x,x/2,x*3]], fs=-1)

            * plot linked graphs '[]'
            gplot([x1,x2,x3], y=y,title=[title1, title2, title3], fs=[fs1,fs2,fs3], channel_names=[chn1,chn2,chn3])
            gplot([x1,x2,x3], y=y,title=[title1, None, title3], fs=fsAll, channel_names=[chn1,None,None])
            gplot([x1,x2,[x3 , x4]], y=y,title=[title1, None, title3], fs=[fs1,fs2,-1], channel_names=[chn1,None,None])
    '''

    self.recording_plotter_container = plotter_countainer()
    self.recording_plotter_container.add(recording, window, start_event, y,title,fs,sens,channel_names,callback, channel_first, verbose)
    
    process = psutil.Process(os.getpid())
    print('memory used:')
    print(process.memory_info().rss)  

    return self.recording_plotter_container.getFavorites()