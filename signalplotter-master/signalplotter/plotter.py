#%%
import sys
import numpy as np
import math
import numbers
import matplotlib.pyplot as plt
from PyQt5 import QtWidgets
from PyQt5.QtCore import QFile, QTextStream
from PyQt5.QtGui import QPalette, QIcon
from PyQt5.QtGui import QKeySequence, QPalette, QColor
from PyQt5.QtCore import Qt, QSize

from .qt.plotter_ui import plotter_ui

#%% ezplot

def iplot(x, fs=None, channel_names=None, auto_normalize:bool=True, channel_first:bool = True, call_show:bool = True, plot_args = None):
    '''
    iplot (inline-plot) is a function for inline visualization of a segment of a multichannel timeseries such as speech, EEG, ECG, EMG, EOG. 
    - inputs:
        -- x: the inout matrix. Its dimension should be as (K: Channel, T: Time-samples) if channel_first is True or (T, K) if channel_first is False.
        -- fs: [optional] sampling frequency. If it is None, the x-axis will be in samples, otherwise in seconds.
        -- channel_names: [optional] the name of channels to be shown on the vertical axis. If it is None, Channel inxdex (from 0) will be shown.
        -- auto_normalize: [optional] to normalize each signal between [0,1].
        -- channel_first: [optional] it defines if channel is before or after the time in the dimensions of the given x tensor.
        -- call_show: if it is True, it calls plt.show() at the end of the function; otherwise not. Can be usefull for adding title, or doing some changes in the plot after the function.
        -- plot_args: the arguments for matplotlib.pyplot.plot function. It should be one in of the following types: 
                        -- a dictionary e.g. {'color': (1,0,0), 'marker':'*'}
                        -- a function that returns such a dictionary. This function should get 3 inputs (isignal, ich, x) where:
                                -- ich is the channel index (e.g. for alternativly coloring)
                                -- ix, if the givenx is a list [x0,x1,...] to be plotted on top of each other, ix defines the signal index, otherwise it is 0.
                                -- x the plotting signal after normalizing (e.g. for highlighting high power signals)
                        example:
                        def getargs(ich,ix,x):
                            if(ich %2 == 0):
                                return {'color': (1,0,0), 'marker':'*'}
                            return {'color': (0,0,1), 'marker':'o'}
    '''   
    assert((plot_args is None) or isinstance(plot_args, dict) or callable(plot_args))
    if(not channel_first):
        x = np.transpose(x)
    if(type(x) is not list):
        x = [x]

    # normalizing
    if(auto_normalize):
        m = min([v.min() for v in x])
        M = max([v.max() for v in x])
        x = [(v-m)/(M-m) for v in x]

    T = x[0].shape[1]
    CH = x[0].shape[0]
    
    t = np.arange(T)
    if(fs is not None):
        t = t / fs
        
    
    # biasing and plotting
    for ix,xx in enumerate(x):
        for ch in range(CH):
            xch = xx[ch, :]
            a = xch + (CH-ch-1) - 0.5
            if(plot_args is None):
                plt.plot(t, a)
            else:
                if(callable(plot_args)):
                    args = plot_args(ch, ix, xch)
                else:
                    args = plot_args
                plt.plot(t, a, **args)
    
    if(fs is not None):
        plt.xlabel("Time (s)")
    else:
        plt.xlabel("Samples")
        
    if(channel_names is not None):
        plt.yticks(range(CH), channel_names[::-1])
    
    if(call_show):
        plt.show()

def iiplot(x, auto_normalize:bool=True, channel_first:bool = True, transpose_image:bool = False, plot_args = None):
    '''
    iiplot (inline-image-plot) is a function for inline visualization of tensors of images, e.g. output of deep neural networks. 
    - inputs:
        -- x: the inout matrix. Its dimension should be as (K: Channel, W: with, H: height) if channel_first is True or (W, H, K) if channel_first is False.
        -- auto_normalize: [optional] to normalize each image between [0,1] per channel.
        -- channel_first: [optional] it defines if channel is the first dimension or the last.
        -- transpose_image: [optional] if true the images per channel are tranposed (H, W).
        -- plot_args: the arguments for matplotlib.pyplot.plot function. It should be one in of the following types: 
                        -- a dictionary e.g. {'color': (1,0,0), 'marker':'*'}
                        -- a function that returns such a dictionary. This function should get 3 inputs (isignal, ich, x) where:
                                -- ich is the channel index (e.g. for alternativly coloring)
                                -- x the plotting image (e.g. for highlighting high power signals)
                        example:
                        def getargs(ich,ix,x):
                            if(ich %2 == 0):
                                return {'color': (1,0,0), 'marker':'*'}
                            return {'color': (0,0,1), 'marker':'o'}
    '''   
    assert((plot_args is None) or isinstance(plot_args, dict) or callable(plot_args))
    if(not channel_first):
        x = np.transpose(x, (2,0,1)) # move the channel dim to the first

    CH = x.shape[0]
    W = x.shape[1]
    H = x.shape[2]
    
    # biasing and plotting
    for ch in range(CH):
        xch = x[ch,]
    # normalizing
        if(auto_normalize):
            m = xch.min()
            M = xch.max()
            xch = (xch-m)/(M-m)
        if(transpose_image):
            xch = np.transpose(xch)
        if(plot_args is None):
            args = {}
        elif(callable(plot_args)):
            args = plot_args(ch, xch)
        else:
            args = plot_args
        plt.imshow(xch, **args)
        plt.title(f'{ch})')
        plt.show()

#%% gplot
def cplot(x=None, window=30, title=None,fs=1,sens=None,channel_names=None, callback=None, channel_first:bool = True, verbose:bool = True):
    '''
    It plots continious signals by spliting into smaller segments and calling gplot.
    It may add zeros to the end of signals for the last segment. 
    - inputs:
        -- x:           The inout tensore. Its dimension should be as (K: Channel, T: Time-samples) if channel_first is True. Otherwise, as (T, K), for instance (3600s * 250 hz, 20 channels).
                        If it has only one dimension, it is assumed to be temporal samples of a single channel signal.
                        It is also possible to pass x1,x2,x3,x4,... for different channels. in this case x must be None.
        -- window:      optional, the length of signal in seconds to be shown in each window frame.        
        --other inputs are as gplot
    '''
    def prepare_x(x, window, fs, channel_first):
        if(type(x) == list):
            xx = []
            for i in range(len(x)):
                xx.append(prepare_x(x[i], window, fs, channel_first))
            return xx

        assert(isinstance(x, np.ndarray))
        if(x.ndim == 1):
            x = np.expand_dims(x,1)
            channel_first = False
        assert(x.ndim == 2)
        if(not channel_first):
            x = x.transpose()
            channel_first = True
        window_sample = window * fs
        CH = x.shape[0]
        T = x.shape[1]
        Nceil = math.ceil(T/window_sample)
        z = np.zeros((CH, Nceil*window_sample - T))
        x = np.concatenate((x,z),1)
        T = x.shape[1]
        assert((T%window_sample)==0)
        xx = np.reshape(x, (CH, int(T/window_sample), window_sample))
        xx = xx.transpose((1,0,2))
        return xx

    if(type(x) != list):
        x=[x]
    x = prepare_x(x, window, fs, channel_first)
    return gplot(x=x, y=None, title=title, fs=fs, sens=sens,channel_names=channel_names, callback=callback, channel_first=True, verbose=verbose)


def gplot(x, y=None, title=None,fs=1,sens=None,channel_names=None, callback=None, channel_first:bool = True, verbose:bool = True):
    '''
    gplot (graphical UI-plot) is a function for visualizing tensors of multichannel timeseries such as speech, EEG, ECG, EMG, EOG. 
    - inputs:
        -- x:           the inout tensore. Its dimension should be as (S: Segments, K: Channel, T: Time-samples) (the same as the default dimension of Keras) if channel_first is True. Otherwise, as (S, T, K).
                        for instance (200 segments, 10s * 250 hz, 20 channels)
        -- y:           optional, the labels of segments. It must be a vector with size of S.
        -- title:       optional, the tile of the window.
        -- fs:          optional [default is None], the sampling frequensy. If fs is None the data will be plotted in samples, otherwise in seconds. 
                        if fs is -1, then the mean of signal on the Time mode will be plotted with a bar graph. 
        -- sens:        optional [default is None], normalizing factor. If it is None, the signals will be normalize automatically with the min and max of each channel in each segment.
        -- channel_names:optional [default is None], the name of channels to be plotted on the y-axis.
        -- callback:    optional [default is None], a function as func(x, sampleIndex) to be called when the user change the sample index by the GUI.
        -- channel_first: optional it defines if channel is before or after the time in the dimensions of the given x tensor.
        -- verbose: optional, if it is true, it logs the changes in the GUI; otherwise it is silent.
        * in order to plot tensors on top of each other (holding on) in the linePlot mode or barPlotMode, use x as List in List: [[x]] (see example 4)
        
    - output: list of selected indexes (as favorite)
    
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

    app = QtWidgets.QApplication(sys.argv)

    __ApplyStyle(app)
    __ApplyIcon(app)

    countainer = plotter_countainer()
    if(type(x) != list):
        x=[x]
    N = len(x)
    if(type(title) != list):
        title=[title] * N
    if(type(fs) != list):
        fs=[fs] * N
    if(type(sens) != list):
        sens=[sens] * N
    if(type(callback) != list):
        callback=[callback] * N
    if(channel_names is None):
        channel_names = [None] * N
    elif(type(channel_names[0]) != list):
        channel_names = [channel_names] * N

    N = len(x)
    for i in range(N):
        countainer.add(x[i],y,title[i],fs[i],sens[i],channel_names[i],callback[i], channel_first, verbose)

    appind = app.exec_()
    
    #sys.exit(appind)


    return countainer.getFavorites()

#%%    
class plotter_countainer():
    def __init__(self):
        self.plotterList = {}
        pass

    def add(self, x, recording, lazy_plot:bool, window, y=None, title=None,fs=1,sens=None,channel_names=None, callback=None, channel_first=True, verbose=True):
        MainWindow = QtWidgets.QMainWindow()
        plotter = plotter_ui(MainWindow=MainWindow, x=x, recording=recording, lazy_plot=lazy_plot, window=window, y=y, title=title, fs=fs, sens=sens, channelNames=channel_names, callback=callback, channelFirst=channel_first, verbose=verbose)
        MainWindow.show()

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
#%%
def __ApplyStyle(app):
# Force the style to be the same on all OSs:
    app.setStyle("Fusion")

    # Now use a palette to switch to dark colors:
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(53, 53, 53))
    palette.setColor(QPalette.WindowText, Qt.white)
    palette.setColor(QPalette.Base, QColor(25, 25, 25))
    palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    palette.setColor(QPalette.ToolTipBase, Qt.white)
    palette.setColor(QPalette.ToolTipText, Qt.white)
    palette.setColor(QPalette.Text, Qt.white)
    palette.setColor(QPalette.Button, QColor(53, 53, 53))
    palette.setColor(QPalette.ButtonText, Qt.white)
    palette.setColor(QPalette.BrightText, Qt.red)
    palette.setColor(QPalette.Link, QColor(42, 130, 218))
    palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    palette.setColor(QPalette.HighlightedText, Qt.black)
    app.setPalette(palette)

def __ApplyIcon(app):
    app_icon = QIcon()
    app_icon.addFile('s16.png', QSize(16,16))
#    app_icon.addFile('gui/icons/24x24.png', QSize(24,24))
#    app_icon.addFile('gui/icons/32x32.png', QSize(32,32))
#    app_icon.addFile('gui/icons/48x48.png', QSize(48,48))
#    app_icon.addFile('gui/icons/256x256.png', QSize(256,256))
    app.setWindowIcon(app_icon)