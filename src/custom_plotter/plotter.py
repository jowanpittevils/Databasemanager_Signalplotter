from databasemanager import *
from custom_plotter.plotter_ui import plotter_ui
from PyQt5 import QtWidgets, QtCore
import sys

class plotter_countainer():
    def __init__(self):
        self.plotterList = {}
        pass

    def add(self, recording, window, start=0, y=None, title=None,fs=1,sens=None,channel_names=None, callback=None, verbose=True):
        '''
        Adds a plotter_ui window that plots the recording data
        inputs as in agplot
        '''
        MainWindow = QtWidgets.QMainWindow()
        plotter = plotter_ui(MainWindow=MainWindow,  recording=recording, window=window, start=start, y=y, title=title, fs=fs, sens=sens, channelNames=channel_names, callback=callback, verbose=verbose)
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



def agplot(recording, window, start=0, y=None, title=None,fs=1,sens=None,channel_names=None, callback=None, verbose:bool = True, UIObject=None):
    '''
    agplot (adapted graphical UI-plot) is a function for visualizing tensors of multichannel timeseries such as speech, EEG, ECG, EMG, EOG. 
    It plots continious signals by sampling the data of the given recording.
    It may add zeros to the end of signals for the last window. 
    - inputs:
        -- recording:   the recording to be plotted
        -- window:      optional, the length of signal in seconds to be shown in each window frame.
                        for instance (200 segments, 10s * 250 hz, 20 channels)
        -- start: plots the recording at the start of the given event.
        -- y:           optional, the labels of segments. It must be a vector with size of S.
        -- title:       optional, the tile of the window.
        -- fs:          optional [default is None], the sampling frequensy. If fs is None the data will be plotted in samples, otherwise in seconds. 
                        if fs is -1, then the mean of signal on the Time mode will be plotted with a bar graph. 
        -- sens:        optional [default is None], normalizing factor. If it is None, the signals will be normalize automatically with the min and max of each channel in each segment.
        -- channel_names:optional [default is None], the name of channels to be plotted on the y-axis.
        -- callback:    optional [default is None], a function as func(x, sampleIndex) to be called when the user change the sample index by the GUI.
        -- verbose: optional, if it is true, it logs the changes in the GUI; otherwise it is silent.
        -- UIObject: when calling the agplot function from a different UI, give this UIObject to the function as a parameter. When calling the function without another UI running, this should be None
        
    - output: list of selected indexes (as favorite)
    
    TODO:
    - examples: 'x=numpy.random.randn(15,fs*10,20)'
            agplot(x)
            agplot(x,title='title', sens=10)
            fav=agplot(x, y=y,title=title, fs=fs, channel_names=chn)
            
            * Bar graph, fs=-1
            agplot([x4,x4/2,x4*3], fs=-1)

            * Plot holded graphs '[[]]'
            agplot([[x,x/2,x*3]])
            agplot([[x,x/2,x*3]], fs=-1)

            * plot linked graphs '[]'
            agplot([x1,x2,x3], y=y,title=[title1, title2, title3], fs=[fs1,fs2,fs3], channel_names=[chn1,chn2,chn3])
            agplot([x1,x2,x3], y=y,title=[title1, None, title3], fs=fsAll, channel_names=[chn1,None,None])
            agplot([x1,x2,[x3 , x4]], y=y,title=[title1, None, title3], fs=[fs1,fs2,-1], channel_names=[chn1,None,None])
    '''
    if(UIObject == None):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
        if hasattr(QtWidgets.QStyleFactory, "AA_UseHighDpiPixmaps"):
            QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps)
        app = QtWidgets.QApplication(sys.argv)
        recording_plotter_container = plotter_countainer()
        recording_plotter_container.add(recording, window, start, y,title,fs,sens,channel_names,callback, verbose)
        sys.exit(app.exec_())
        return recording_plotter_container.getFavorites
    else:
        UIObject.recording_plotter_container = plotter_countainer()
        UIObject.recording_plotter_container.add(recording, window, start, y,title,fs,sens,channel_names,callback, verbose)
        return UIObject.recording_plotter_container.getFavorites

