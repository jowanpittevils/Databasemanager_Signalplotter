from custom_plotter.plotter_uiDesign import Ui_MainWindow
import pyqtgraph as pg
import numpy as np
from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5 import QtWidgets, QtGui
from databasemanager import *
import math
import datetime
import time


class plotter_ui(QObject, Ui_MainWindow):
    __lastID = 0
    @classmethod
    def __getNewID(cls):
        cls.__lastID += 1
        return cls.__lastID
    
    IndexChanged = pyqtSignal(int, int)
    def __init__(self, MainWindow, recording, window, start=0, y=None, title=None,fs=1, sens=None, channelNames=None, callback=None, verbose=True):
        super().__init__()
        self.recording = recording
        self.annotations = self.recording.annotations
        self.window = window
        self.start = start
        self.scale_factor = 1
        self.colors_ev = {}
        self.event_colors = ['#4363d8', '#800000', '#3cb44b', '#ffe119', '#f58231', '#911eb4', '#46f0f0', '#f032e6', '#bcf60c', '#fabebe', '#008080', '#e6beff', '#9a6324', '#fffac8', '#aaffc3', '#808000', '#e6194b', '#ffd8b1', '#000075', '#808080', '#ffffff', '#000000']
        self.verbose = verbose
        self.norm = plotter_ui.struct()
        self.ID = plotter_ui.__getNewID()
        self.y = y
        self.FavoriteList=set()
        self.setupUi(MainWindow)
        self.MainWindow = MainWindow
        self.window_scale = 1
        self.callback = callback
        self.sens = sens
        self.__UpdateTitleText(recording.name)
        self.axis.showGrid(True,True)
        self.ChannelNames = channelNames
        self.UpdateSampleIndex(0)
        self.__AssignCallbacks()
        self.detachedWindows=[]
        self.assign_colors()
        self.axis.setBackgroundBrush(QtGui.QBrush(QtGui.QColor(0, 0, 0, 255))) # set background color here
        self.norm.totalMaxX = 0.01
        self.norm.totalMinX = -0.01
        self.T = int(self.recording.fs) * self.window
        self.CH = recording.number_of_channels
        N = math.ceil(recording.duration_samp/self.T)
        self.__UpdateFs(fs)
        self.__UpdateTotalNumberOfSamples()

        self.vb = self.axis.getViewBox()
        self.vb.setMouseEnabled(x=False, y=False)
        plotSample = int(self.start*self.fs-10*self.fs)
        if plotSample < 0 :
            self.UpdateSampleIndex(0,True)

        else:
            self.UpdateSampleIndex(plotSample,True)

    def assign_colors(self):
        #gives each event a different color in the plotter window
        i = 0
        for ann in self.annotations:
            for event in ann.events:
                t = i%len(self.event_colors)
                self.colors_ev[event] = pg.intColor(i, alpha = 255)
                i = i+1

    def __CheckAnnotationOverlap(self, SampleIndex):
        #needed to know which events are currently overlapping the window
        overlapping_events = []
        start = SampleIndex
        end = SampleIndex+self.T
        for ann in self.annotations:
            for event in ann.events:

                ev_start = event.start*self.fs
                ev_stop = event.stop*self.fs
                if((start <= ev_stop) and (end >= ev_start)):
                    overlapping_events.append(event)
        return overlapping_events
            
    def __UpdateTitleText(self, title):
        self.title = title
        wintitle =  str(self.ID) + '-Signal plotter'
        if(title is not None):
            wintitle += ' - ' + title
        self.MainWindow.setWindowTitle(wintitle)
        
    def __increase_amplitude(self):
        self.scale_factor = self.scale_factor*0.8
        self.Plot()

    def __decrease_amplitude(self):
        self.scale_factor = self.scale_factor/0.8
        self.Plot()
    
    def __UpdateFs(self, fs):
        self.fs = fs
        if(fs is not None):
            if(fs != -1):
                self.axis.setLabel('bottom', 'hh:mm:ss')
            self.T_sec = self.T/fs
        else:
            self.axis.setLabel('bottom', 'Sample')
            
    def __UpdateChannelNames(self, channelNames, overlapping_events, areChannelsVertical):
        ttick=list()  
        for i,t in enumerate(channelNames[::-1]):
            ttick.append((i,  t))
        for i,event in enumerate(overlapping_events):
            ttick.append((self.CH-0.1-i/8, event.label))
        left_ax=self.axis.getAxis('left') 
        left_ax.setTicks([ttick])
    
    def UpdateSampleIndex(self, sampleIndex, rePlot=False, callerObject=None, triggeredSignals = True):
        self.SampleIndex = sampleIndex
        if(callerObject != self.nmrSampleIndex):
            self.nmrSampleIndex.blockSignals(True)
            self.nmrSampleIndex.setValue(sampleIndex)
            self.nmrSampleIndex.blockSignals(False)
        if(callerObject != self.sldSampleIndex):
            self.sldSampleIndex.blockSignals(True)
            self.sldSampleIndex.setValue(sampleIndex)
            self.sldSampleIndex.blockSignals(False)
        if(rePlot):
            self.Plot()
        if(triggeredSignals):
            self.IndexChanged.emit(self.ID, self.SampleIndex)
        self.chbFavorite.blockSignals(True)
        self.chbFavorite.setChecked((self.SampleIndex in self.FavoriteList))
        self.chbFavorite.blockSignals(False)
        print(self.FavoriteList)
        
    def __UpdateTotalNumberOfSamples(self):
        self.lblTotalSamples.setText("/ " + str(self.recording.duration_samp - math.floor(self.T/2)))
        self.sldSampleIndex.setMaximum(self.recording.duration_samp - math.floor(self.T))
        self.nmrSampleIndex.setMaximum(self.recording.duration_samp - math.floor(self.T))
        self.sldSampleIndex.setMinimum(0)
        self.nmrSampleIndex.setMinimum(0)
        
    def __AddBias(self, x0):
        x = x0
        for xi in x:
            for ch in range(self.CH):
                xi[ch,:] += (self.CH-ch-1) - 0.5
        return x
        
    def __iNormalize(self, x0, sens = None):
        if(sens is None):
            M = self.scale_factor*max([v.max() for v in x0]) #Scale factor for changing amplitude
            m = self.scale_factor*min([v.min() for v in x0])
        else:
            M = sens
            m = -sens
        x = [(v-m)/(M-m) for v in x0]
        return x
        
    def Clear(self):
        self.axis.clear()
        
    def Plot(self, sampleIndex = None):
        if(sampleIndex is not None):
            self.UpdateSampleIndex(sampleIndex)
        overlapping_events = self.__CheckAnnotationOverlap(self.SampleIndex)
        self.PlotLine(overlapping_events, self.recording,self.window, self.SampleIndex)
        self.__UpdateChannelNames(self.ChannelNames,overlapping_events, True)
        self.vb.autoRange(padding = 0)
            
    def PlotLine(self, overlapping_events, recording,window, sampleIndex):
        if(self.window_scale >= 1):
            window_scale = int(self.window_scale)
        else:
            window_scale = 1
        if(sampleIndex < self.recording.duration_samp - self.T):
            start=sampleIndex
            stop=sampleIndex+self.T
            xx = [recording._get_data_in_sample(start=start, stop=stop)]
            xx = [xx[0][0:,0::window_scale]]
        else:
            xx = np.zeros(shape=(1,self.CH,self.T))
            data = np.array([recording.get_data(start=sampleIndex/self.fs)])
            xx[:,:data.shape[1],:data.shape[2]] = data
            xx = [xx[0][0:,0::window_scale]]
        xx = self.__iNormalize(xx, self.sens)
        xx = self.__AddBias(xx)
        t = np.arange(sampleIndex, sampleIndex+self.T)
        ticks = list()
        if(self.fs is not None):
            t = t / self.fs
            if(self.T > 9):
                for i in range(0,self.T,math.floor(self.T/10)):
                    ticks.append((t[i],time.strftime('%H:%M:%S', time.gmtime(t[i]))))
        stringaxis = self.axis.getAxis('bottom')
        stringaxis.setTicks([ticks])
        t = t[0::window_scale]
        tEvent = {}
        ToPlot = {}
        starts = {}
        stops = {}
        for i, event in enumerate(overlapping_events):
            tEvent[event] = t
            starts[event] = max(sampleIndex/self.fs, event.start)
            stops[event] = min((sampleIndex+self.T)/self.fs, event.stop)
            tEvent[event] = [item for item in tEvent[event] if (item >= starts[event] and item <= stops[event])]
            ToPlot[event] = [self.CH-i/8-0.1 for item in tEvent[event] if (item >= starts[event] and item <= stops[event])]
        self.Clear()
        for i, xxi in enumerate(xx):
            for ch in range(self.CH):
                    self.axis.plot(t,xxi[ch,:], pen=self.GetPen(i))
        for i, event in enumerate(overlapping_events):
                self.axis.plot(tEvent[event],ToPlot[event], pen=pg.mkPen(self.colors_ev[event],width=8))
        self.vb.setLimits(yMin=-1, yMax=self.CH, xMin = sampleIndex/self.fs, xMax=t[-1])
        self.__UpdateTitle()

    def GetColorString(self, colorIndex=0):
        strL = ('#4363d8', '#800000', '#3cb44b', '#ffe119', '#f58231', '#911eb4', '#46f0f0', '#f032e6', '#bcf60c', '#fabebe', '#008080', '#e6beff', '#9a6324', '#fffac8', '#aaffc3', '#808000', '#e6194b', '#ffd8b1', '#000075', '#808080', '#ffffff', '#000000')
        return str(strL[colorIndex])
    def GetPen(self, colorIndex=0):
        return pg.mkPen(self.GetColorString(colorIndex))
        
    def __UpdateTitle(self):
        if(self.title is not None):
            titlestr = self.title + ' '
        else:
            titlestr = ''
        if(self.y is not None):
            ystr = '(y[{0}]= {1})'.format(self.SampleIndex, self.y[self.SampleIndex])
        else:
            ystr = ''
        titlestr += ystr
        self.lblTitle.setText(titlestr)

        if(self.verbose):                
            printstr = 'Plotted (x({0},:,:))'.format(self.SampleIndex)
            if(self.y is not None):
                printstr += ' ' + ystr
            print(printstr)
    
    def __AssignCallbacks(self):
        self.btnFirst.clicked.connect(self.__onbtnFirstClicked)
        self.btnAmpUp.clicked.connect(self.__increase_amplitude)
        self.btnAmpDown.clicked.connect(self.__decrease_amplitude)
        self.btnWindowUp.clicked.connect(self.__onbtnWindowUp)
        self.btnWindowDown.clicked.connect(self.__onbtnWindowDown)
        self.btnPrevious.clicked.connect(self.__onbtnPreviousClicked)
        self.btnNext.clicked.connect(self.__onbtnNextClicked)
        self.btnPreviousSimilarY.clicked.connect(self.__onbtnPreviousSimilarYClicked)
        self.btnNextSimilarY.clicked.connect(self.__onbtnNextSimilarYClicked)
        self.btnLast.clicked.connect(self.__onbtnLastClicked)
        self.sldSampleIndex.valueChanged.connect(self.__onsldValueChanged)
        self.nmrSampleIndex.valueChanged.connect(self.__onnmrValueChanged)
        self.btnDuplicate.clicked.connect(self.__onbtnDuplicate)
        self.chbFavorite.stateChanged.connect(self.__onchbFavoriteStateChanged)

    def __onchbFavoriteStateChanged(self, state):
        if(self.chbFavorite.isChecked()):
            self.FavoriteList.add(self.SampleIndex)
        else:
            self.FavoriteList.discard(self.SampleIndex)
    def __onbtnFirstClicked(self):
        self.UpdateSampleIndex(0, True)
    def __onbtnPreviousClicked(self):
        if(self.SampleIndex>math.floor(self.T*0.3)):
            self.UpdateSampleIndex(self.SampleIndex - math.floor(self.T*0.3), True)
        else:
            self.UpdateSampleIndex(0, True)
    def __onbtnNextClicked(self):
        if(self.SampleIndex<(self.recording.duration_samp - 1.3*math.floor(self.T))):
            self.UpdateSampleIndex(self.SampleIndex + math.floor(self.T*0.3), True)
        else:
            self.UpdateSampleIndex(self.recording.duration_samp - math.floor(self.T), True)
    def __onbtnPreviousSimilarYClicked(self):
        if(self.SampleIndex>self.T):
            self.UpdateSampleIndex(self.SampleIndex-self.T,True)
        else:
            self.UpdateSampleIndex(0,True)
    def __onbtnNextSimilarYClicked(self):
        if(self.SampleIndex<(self.recording.duration_samp-self.T)):
            self.UpdateSampleIndex(self.SampleIndex+self.T,True)
    def __onbtnLastClicked(self):
        self.UpdateSampleIndex(self.recording.duration_samp-self.T, True)
    def __onsldSliderReleased(self):
        self.UpdateSampleIndex(self.sldSampleIndex.value(), True,self.sldSampleIndex)
    def __onsldValueChanged(self):
        self.UpdateSampleIndex(self.sldSampleIndex.value(), True,self.sldSampleIndex)
    def __onnmrValueChanged(self):
        self.UpdateSampleIndex(self.nmrSampleIndex.value(), True,self.nmrSampleIndex)
    def __onbtnDuplicate(self):
        self.DuplicateCurrent()

    def __onbtnWindowUp(self):
        self.window = self.window*2
        self.T = int(int(self.recording.fs) * self.window)
        self.__UpdateTotalNumberOfSamples()
        self.window_scale = self.window_scale*2
        self.Plot()

    def __onbtnWindowDown(self):
        self.window = self.window/2
        self.T = int(int(self.recording.fs) * self.window)
        self.__UpdateTotalNumberOfSamples()
        self.window_scale = self.window_scale/2
        if self.T > 2:
            self.Plot()
        else:
            self.window = self.window*2
            self.T = int(int(self.recording.fs) * self.window)
            self.__UpdateTotalNumberOfSamples()

    def DuplicateCurrent(self):
        if(self.verbose):                
            print('detaching...')
        MainWindow = QtWidgets.QMainWindow()
        plotter = plotter_ui(MainWindow=MainWindow, recording=self.recording, window =self.window, start = 0,y=self.y, title=self.title, fs=self.fs, sens=self.sens, channelNames=self.ChannelNames, callback=self.callback)
        self.detachedWindows.append(plotter)
        MainWindow.show()
        MainWindow.resize(self.MainWindow.size())
        plotter.UpdateSampleIndex(self.SampleIndex, rePlot=True, triggeredSignals = False)
        
    class struct():
        pass