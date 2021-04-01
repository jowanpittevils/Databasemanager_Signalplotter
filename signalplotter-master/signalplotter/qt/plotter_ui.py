from .plotter_uiDesign import Ui_MainWindow
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
    def __init__(self, MainWindow, x, recording, lazy_plot:bool, window, y=None, title=None,fs=1, sens=None, channelNames=None, callback=None, channelFirst=True, verbose=True):
        super().__init__()
        self.recording = recording
        self.annotations = self.recording.annotations
        self.window = window
        self.scale_factor = 1
        self.lazy_plot = lazy_plot
        self.colors_ev = {}
        self.event_colors = ['#4363d8', '#800000', '#3cb44b', '#ffe119', '#f58231', '#911eb4', '#46f0f0', '#f032e6', '#bcf60c', '#fabebe', '#008080', '#e6beff', '#9a6324', '#fffac8', '#aaffc3', '#808000', '#e6194b', '#ffd8b1', '#000075', '#808080', '#ffffff', '#000000']
        self.verbose = verbose
        self.norm = plotter_ui.struct()
        self.ID = plotter_ui.__getNewID()
        self.FavoriteList=set()
        self.setupUi(MainWindow)
        self.MainWindow = MainWindow
        self.channelFirst = channelFirst
        self.callback = callback
        self.sens = sens
        self.__UpdateTitleText(recording.name)
        self.axis.showGrid(True,True)
        self.ChannelNames = channelNames
        self.__UpdateY(y)
        self.UpdateSampleIndex(0)
        self.__AssignCallbacks()
        self.detachedWindows=[]
        self.assign_colors()
        self.axis.setBackgroundBrush(QtGui.QBrush(QtGui.QColor(0, 0, 0, 255))) # set background color here

        if self.lazy_plot == True:
            self.norm.totalMaxX = 0.01
            self.norm.totalMinX = -0.01
            if(self.channelFirst):
                self.T = int(self.recording.fs) * self.window
                self.CH = recording.number_of_channels
            else:
                self.T = int(self.recording.fs) * self.window
                self.CH = recording.number_of_channels
            N = math.ceil(recording.duration_samp/self.T)
            self.__UpdateFs(fs)
            self.__UpdateTotalNumberOfSamples(N)

        else:
            if(type(x) == list):
                self.xx = x
                self.x = x[0]
            else:
                self.xx = [x]
                self.x = x
            self.norm.totalMaxX = max([tx.max() for tx in self.xx])
            self.norm.totalMinX = min([tx.min() for tx in self.xx])
            N = self.x.shape[0]
            if(self.channelFirst):
                self.T = self.x.shape[2]
                self.CH = self.x.shape[1]
            else:
                self.T = self.x.shape[1]
                self.CH = self.x.shape[2]
            self.__UpdateFs(fs)
            self.__UpdateTotalNumberOfSamples(N)
        self.vb = self.axis.getViewBox()
        self.vb.setLimits(yMin=-1, yMax=self.CH, xMin = 0, xMax=self.window*N)
        self.vb.setMouseEnabled(x=False, y=False)
        self.vb.autoRange(padding = 0)
        self.UpdateSampleIndex(0)
        self.Plot()


    def assign_colors(self):
        i = 0
        for ann in self.annotations:
            for event in ann.events:
                t = i%len(self.event_colors)
                self.colors_ev[event] = pg.intColor(i, alpha = 255)
                i = i+1



    def __CheckAnnotationOverlap(self, SampleIndex):
        overlapping_events = []
        start = SampleIndex*self.window
        end = (SampleIndex+1)*self.window
        for ann in self.annotations:
            for event in ann.events:

                ev_start = event.start
                ev_stop = event.stop
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
        
    def __UpdateY(self, y):
        self.y = y
        self.btnPreviousY.setEnabled(y is not None)
        self.btnNextY.setEnabled(y is not None)
        self.btnPreviousSimilarY.setEnabled(y is not None)
        self.btnNextSimilarY.setEnabled(y is not None)

    
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
        if(areChannelsVertical): 
            side = 'left'
        else:
            side = 'bottom'
        if(channelNames is not None):
            for i,t in enumerate(channelNames[::-1]):
                ttick.append((i,  t))
        else:
            self.axis.setLabel(side, 'Channel Index')
            for ch in range(self.CH):
                ttick.append((ch,  self.CH-ch-1))
        for i,event in enumerate(overlapping_events):
            ttick.append((self.CH-0.1-i/8, event.label))
        ax=self.axis.getAxis(side) 
        ax.setTicks([ttick])
    
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
        if (self.lazy_plot == False) and (self.callback is not None):
            if(len(self.xx)==1):
                self.callback(self.x[self.SampleIndex,],self.SampleIndex)
            else:
               xx = [v[self.SampleIndex,] for v in self.xx]
               self.callback(self.xx,self.SampleIndex)
        self.chbFavorite.blockSignals(True)
        self.chbFavorite.setChecked((self.SampleIndex in self.FavoriteList))
        self.chbFavorite.blockSignals(False)
        
        

    def __UpdateTotalNumberOfSamples(self,N):
        self.N = N
        self.lblTotalSamples.setText("/ " + str(N))
        self.sldSampleIndex.setMaximum(N-1)
        self.nmrSampleIndex.setMaximum(N-1)
        self.sldSampleIndex.setMinimum(0)
        self.nmrSampleIndex.setMinimum(0)
        
    def __AddBias(self, x0):
        x = x0
        for xi in x:
            for ch in range(self.CH):
                if(self.channelFirst):
                    xi[ch,:] += (self.CH-ch-1) - 0.5
                else:
                    xi[:,ch] += (self.CH-ch-1) - 0.5
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
        if self.lazy_plot == True:
            if(self.fs != -1):
                self.PlotLine(None,overlapping_events, self.recording,self.window, self.SampleIndex)
                self.__UpdateChannelNames(self.ChannelNames,overlapping_events, True)
            else:
                self.PlotBar(None, self.recording, self.window, self.SampleIndex)
                self.__UpdateChannelNames(self.ChannelNames,overlapping_events, False)
        else:
            if(self.fs != -1):
                self.PlotLine(self.xx, overlapping_events, None, None, self.SampleIndex)
                self.__UpdateChannelNames(self.ChannelNames,overlapping_events, True)
            else:
                self.PlotBar(self.xx, None, None, self.SampleIndex)
                self.__UpdateChannelNames(self.ChannelNames, overlapping_events,False)
        self.vb.autoRange(padding = 0)

            
    def PlotLine(self, xx, overlapping_events, recording,window, sampleIndex):
        
        if self.lazy_plot == True:
            if(sampleIndex < self.N - 1):
                xx = [recording.get_data(start=sampleIndex*window, stop=(sampleIndex+1)*window)]
            else:
                xx = np.zeros(shape=(1,self.CH,self.T))
                data = np.array([recording.get_data(start=sampleIndex*window)])
                xx[:,:data.shape[1],:data.shape[2]] = data
        else:
            xx = [v[sampleIndex,] for v in xx]

        xx = self.__iNormalize(xx, self.sens)
        xx = self.__AddBias(xx)
        
        t = np.arange(sampleIndex*self.T, (sampleIndex+1)*self.T)


        tEvent = {}
        ToPlot = {}
        starts = {}
        stops = {}
        for i, event in enumerate(overlapping_events):
            tEvent[event] = np.arange(sampleIndex*self.T, (sampleIndex+1)*self.T)
            tEvent[event] = tEvent[event]/self.fs
            starts[event] = max(sampleIndex*self.T/self.fs, event.start)
            stops[event] = min((sampleIndex+1)*self.T/self.fs, event.stop)
            tEvent[event] = [item for item in tEvent[event] if (item >= starts[event] and item <= stops[event])]
            ToPlot[event] = [self.CH-i/8-0.1 for item in tEvent[event] if (item >= starts[event] and item <= stops[event])]

        ticks = list()

        if(self.fs is not None):
            t = t / self.fs
            if(self.T > 9):
                for i in range(0,self.T,math.floor(self.T/10)):
                    ticks.append((t[i],time.strftime('%H:%M:%S', time.gmtime(t[i]))))
    
        stringaxis = self.axis.getAxis('bottom')
        stringaxis.setTicks([ticks])

        self.Clear()
        for i, xxi in enumerate(xx):
            for ch in range(self.CH):
                if(self.channelFirst):
                    self.axis.plot(t,xxi[ch,:], pen=self.GetPen(i))
                else:
                    self.axis.plot(t,xxi[:,ch], pen=self.GetPen(i))
        for i, event in enumerate(overlapping_events):
            if(self.channelFirst):
                self.axis.plot(tEvent[event],ToPlot[event], pen=pg.mkPen(self.colors_ev[event],width=8))
            else:
                self.axis.plot(tEvent[event],ToPlot[event], pen=pg.mkPen(self.colors_ev[event],width=8,))
        self.axis.setDownsampling(auto = True, mode = 'subsample')
        self.vb.setLimits(yMin=-1, yMax=self.CH, xMin = 0, xMax=t[-1])
        self.__UpdateTitle()
    def GetColorString(self, colorIndex=0):
        strL = ('#4363d8', '#800000', '#3cb44b', '#ffe119', '#f58231', '#911eb4', '#46f0f0', '#f032e6', '#bcf60c', '#fabebe', '#008080', '#e6beff', '#9a6324', '#fffac8', '#aaffc3', '#808000', '#e6194b', '#ffd8b1', '#000075', '#808080', '#ffffff', '#000000')
        return str(strL[colorIndex])
    def GetPen(self, colorIndex=0):
        return pg.mkPen(self.GetColorString(colorIndex))
    def PlotBar(self, xx, recording, window, sampleIndex):
        if self.lazy_plot == True:
            if(sampleIndex < self.N - 1):
                xx0 = [recording.get_data(start=sampleIndex*window, stop=(sampleIndex+1)*window)]
            else:
                xx0 = np.zeros(shape=(1,8,2500))
                data = np.array([recording.get_data(start=sampleIndex*window)])
                xx0[:,:data.shape[1],:data.shape[2]] = data
        else:
            xx0 = [v[sampleIndex,] for v in xx]
        
        xx = []
        for v in xx0:
            if((len(v.shape)==2) or (not self.channelFirst)):
                mm = v.mean(0)
                t = np.arange(v.shape[0]) # for the next lines 'pg.BarGraphItem'
            else:
                mm = v.mean(1)
                t = np.arange(v.shape[1]) # for the next lines 'pg.BarGraphItem'
            xx.append(mm)

        self.Clear()
        w = 1/len(xx)/1.5
        for i,xxi in enumerate(xx):
            bg1 = pg.BarGraphItem(x=t-(len(xx)-1)*w/2+i*w, height=xxi,width = w, brush=self.GetColorString(i))
            self.axis.addItem(bg1)
         
        m = min(self.norm.totalMinX-1,0)
        M = self.norm.totalMaxX * 1.1
        self.__UpdateTitle()
        self.autoRange(padding = 0)
        
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
        self.btnPreviousY.clicked.connect(self.__onbtnPreviousYClicked)
        self.btnPreviousSimilarY.clicked.connect(self.__onbtnPreviousSimilarYClicked)
        self.btnPrevious.clicked.connect(self.__onbtnPreviousClicked)
        self.btnNext.clicked.connect(self.__onbtnNextClicked)
        self.btnNextY.clicked.connect(self.__onbtnNextYClicked)
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
    def __onbtnPreviousYClicked(self):
        n = self.__FindYIndex(False, False)
        if(n is not None):
            self.UpdateSampleIndex(n, True)
    def __onbtnPreviousSimilarYClicked(self):
        n = self.__FindYIndex(False, True)
        if(n is not None):
            self.UpdateSampleIndex(n, True)
    def __onbtnPreviousClicked(self):
        if(self.SampleIndex>0):
            self.UpdateSampleIndex(self.SampleIndex-1, True)
    def __onbtnNextClicked(self):
        if(self.SampleIndex<(self.N-1)):
            self.UpdateSampleIndex(self.SampleIndex+1, True)
    def __onbtnNextYClicked(self):
        n = self.__FindYIndex(True, False)
        if(n is not None):
            self.UpdateSampleIndex(n, True)
    def __onbtnNextSimilarYClicked(self):
        n = self.__FindYIndex(True, True)
        if(n is not None):
            self.UpdateSampleIndex(n, True)
    def __onbtnLastClicked(self):
        self.UpdateSampleIndex(self.N-1, True)
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
        N = math.ceil(self.recording.duration_samp/self.T)
        #self.__UpdateFs(fs)
        self.__UpdateTotalNumberOfSamples(N)
        self.UpdateSampleIndex(math.floor(self.SampleIndex / 2))
        self.Plot()


    def __onbtnWindowDown(self):
        self.window = self.window/2
        self.T = int(int(self.recording.fs) * self.window)
        if self.T > 2:
            N = math.ceil(self.recording.duration_samp/self.T)
            #self.__UpdateFs(fs)
            self.__UpdateTotalNumberOfSamples(N)
            self.UpdateSampleIndex(self.SampleIndex * 2)
            self.Plot()
        else:
            self.window = self.window*2
            self.T = int(int(self.recording.fs) * self.window)


    def __FindYIndex(self, forward, similar):
        if(self.y is None):
            return None
        n = self.SampleIndex
        cy = self.y[n]
        if(forward):
            searchRange = range(n+1,self.N)
        else:
            searchRange = range(n-1,-1,-1)
            
        for i in searchRange:
            if(similar):
                if(isinstance(self.y[i], list) or isinstance(self.y[i], np.ndarray)):
                    if((all(self.y[i] == cy))):
                        return i
                else:
                    if(self.y[i] == cy):
                        return i
            else:
                if(isinstance(self.y[i], list) or isinstance(self.y[i], np.ndarray)):
                    if((all(self.y[i] != cy))):
                        return i
                else:
                    if(self.y[i] != cy):
                        return i
        return None
    
    def DuplicateCurrent(self):
        if(self.verbose):                
            print('detaching...')
        MainWindow = QtWidgets.QMainWindow()
        plotter = plotter_ui(MainWindow=MainWindow, x=self.x, recording=self.recording, lazy_plot=self.lazy_plot, window =self.window, y=self.y, title=self.title, fs=self.fs, sens=self.sens, channelNames=self.ChannelNames, callback=self.callback)
        self.detachedWindows.append(plotter)
        MainWindow.show()
        MainWindow.resize(self.MainWindow.size())
        plotter.UpdateSampleIndex(self.SampleIndex, rePlot=True, triggeredSignals = False)
        
    class struct():
        pass

       
                