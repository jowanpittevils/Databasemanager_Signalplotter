from custom_plotter.plotter_uiDesign import Ui_MainWindow
from custom_plotter.channel_ui import channel_UI
import pyqtgraph as pg
import numpy as np
from PyQt5.QtCore import QObject, pyqtSignal, Qt
from PyQt5 import QtChart, QtWidgets, QtGui, QtPrintSupport
from PyQt5.QtWidgets import QFileDialog
from databasemanager import *
import math
import datetime
import time
from threading import Thread
import threading



class plotter_ui(QObject, Ui_MainWindow):
    __lastID = 0
    @classmethod
    def __getNewID(cls):
        cls.__lastID += 1
        return cls.__lastID
    
    IndexChanged = pyqtSignal(int, int)
    def __init__(self, MainWindow, recording, window, start=0, y=None, title=None,fs=1, sens=None, channelNames=None, callback=None, verbose=True):
        super().__init__()
        self.fit_to_pane = False
        self.recording = recording
        self.annotations = self.recording.annotations
        self.window = window
        self.start = start
        self.scale_factor = 1
        self.colors_ev = {}
        self.event_colors = ['#4363d8', '#800000', '#3cb44b', '#ffe119', '#f58231', '#911eb4', '#46f0f0', '#f032e6', '#bcf60c', '#fabebe', '#008080', '#e6beff', '#9a6324', '#fffac8', '#aaffc3', '#808000', '#e6194b', '#ffd8b1', '#000075', '#808080', '#ffffff', '#000000']
        self.verbose = verbose
        self.range = 0
        self.norm = plotter_ui.struct()
        self.ID = plotter_ui.__getNewID()
        self.y = y
        self.FavoriteList=list()
        self.setupUi(MainWindow)
        self.MainWindow = MainWindow
        self.window_scale = 1
        self.callback = callback
        self.sens = sens
        self.__UpdateTitleText(recording.subject_name + ': ' + recording.name)
        self.axis.showGrid(True,True)
        self.ChannelNames = channelNames
        self.T = int(self.recording.fs) * self.window
        self.CH = recording.number_of_channels
        self.__UpdateFs(fs)
        self.chbFit.setChecked(False)
        self.chbNight.setChecked(True)
        self.night_mode = 1
        self.UpdateSampleIndex(0)
        self.__AssignCallbacks()
        self.detachedWindows=[]
        self.assign_colors()
        self.axis.setBackgroundBrush(QtGui.QBrush(QtGui.QColor(0, 0, 0, 255))) # set background color here
        self.norm.totalMaxX = 0.01
        self.norm.totalMinX = -0.01
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
            self.nmrSampleIndex.setValue(math.floor(sampleIndex/self.fs))
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
        self.chbFavorite.setChecked(([self.SampleIndex/self.fs,self.SampleIndex/self.fs+self.window] in self.FavoriteList))
        self.chbFavorite.blockSignals(False)

    def __UpdateAmplitude(self):
        if(self.fit_to_pane):
            self.lblAmplitude.setText("Fit to pane")
        else:
            temp = self.format_e(self.range*self.scale_factor)
            self.lblAmplitude.setText(temp)
        
    def __UpdateTotalNumberOfSamples(self):
        if(self.recording.duration_sec - self.window) > 0:
            self.lblTotalSamples.setText("/ " + str(int(self.recording.duration_sec - int(self.window))) + " s")
        else:
            self.lblTotalSamples.setText("/ " + str(0) + " s")
        print(self.T, 'T')
        self.sldSampleIndex.setMaximum(self.recording.duration_samp - self.T)
        self.nmrSampleIndex.setMaximum(self.recording.duration_sec -self.window)
        self.sldSampleIndex.setMinimum(0)
        self.nmrSampleIndex.setMinimum(0)

    def format_e(self, n):
        a = '%E' % n
        return a.split('E')[0].rstrip('0').rstrip('.') + 'E' + a.split('E')[1]
        
    def __AddBias(self, x0):
        x = x0
        for xi in x:
            for ch in range(self.CH):
                xi[ch,:] += (self.CH-ch-1) - 0.5
        return x
        
    def __iNormalize(self, x0, sens = None):
        M = max([v.max() for v in x0]) #Scale factor for changing amplitude
        m = min([v.min() for v in x0])
        x = [(v-self.scale_factor*m)/(self.scale_factor*M-self.scale_factor*m) for v in x0]
        self.range = M-m
        self.__UpdateAmplitude()
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
            
    def PlotLine(self, overlapping_events, recording, window, sampleIndex):
        if(sampleIndex < 0):
            sampleIndex = 0
        if(self.window_scale >= 1):
            window_scale = int(self.window_scale)
        else:
            window_scale = 1
        if(sampleIndex < self.recording.duration_samp - self.T):
            start=sampleIndex
            stop=sampleIndex+self.T
            xx = [recording._get_data_in_sample(start=int(start), stop=int(stop))]
            xx = [xx[0][0:,0::window_scale]]
        else:
            xx = np.zeros(shape=(1,self.CH,self.T))
            print(sampleIndex, "sampleindex")
            print(sampleIndex/self.fs)
            data = np.array([recording.get_data(start=sampleIndex/self.fs)])
            xx[:,:data.shape[1],:data.shape[2]] = data
            xx = [xx[0][0:,0::window_scale]]
        temp = []
        if(self.fit_to_pane):
            for i in range(self.CH):
                temp.append(self.__iNormalize([xx[0][i,0:]], self.sens))
            temp = np.transpose(temp, (1,0,2))
            xx = temp
        else:
            xx = self.__iNormalize(xx, self.sens)
        xx = self.__AddBias(xx)
        t = np.arange(sampleIndex, sampleIndex+self.T)
        ticks = list()
        if(self.fs is not None):
            t = t / self.fs
            if(self.T > 9):
                for i in range(0,int(self.T),int(math.floor(self.T/10))):
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
                if(self.night_mode == 1):
                    self.axis.plot(t,xxi[ch,:], pen=self.GetPen(i))
                else:
                    self.axis.plot(t,xxi[ch,:], pen=self.GetPen(21))
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
        # move buttons
        self.btnFirst.clicked.connect(self.__onbtnFirstClicked)
        self.btnLast.clicked.connect(self.__onbtnLastClicked)
        self.btnPrevious.clicked.connect(self.__onbtnPreviousClicked)
        self.btnNext.clicked.connect(self.__onbtnNextClicked)
        self.btnPreviousSimilarY.clicked.connect(self.__onbtnPreviousSimilarYClicked)
        self.btnNextSimilarY.clicked.connect(self.__onbtnNextSimilarYClicked)
        #slider+spinbox
        self.sldSampleIndex.valueChanged.connect(self.__onsldValueChanged)
        self.nmrSampleIndex.valueChanged.connect(self.__onnmrValueChanged)
        #checkboxes + duplicate&print buttons
        self.chbNight.stateChanged.connect(self.__onchbNightStateChanged)        
        self.chbFavorite.stateChanged.connect(self.__onchbFavoriteStateChanged)
        self.chbFit.stateChanged.connect(self.__onchbFitStateChanged)
        self.btnPrint.clicked.connect(self.__onbtnPrintClicked)
        self.btnDuplicate.clicked.connect(self.__onbtnDuplicate)
        ###menubar###
        #channels
        self.signals_add.triggered.connect(self.__onbtnChannelsAdd)
        self.signals_remove.triggered.connect(self.__onbtnChannelsRemove)
        #timescale
        self.window1sec.triggered.connect(lambda: self.__windowResize(1))
        self.window2sec.triggered.connect(lambda: self.__windowResize(2))
        self.window5sec.triggered.connect(lambda: self.__windowResize(5))
        self.window10sec.triggered.connect(lambda: self.__windowResize(10))
        self.window20sec.triggered.connect(lambda: self.__windowResize(20))
        self.window30sec.triggered.connect(lambda: self.__windowResize(30))
        self.window60sec.triggered.connect(lambda: self.__windowResize(60))
        #amplitude
        self.amp5x.triggered.connect(lambda: self.__amplitudeResize(5))
        self.amp2x.triggered.connect(lambda: self.__amplitudeResize(2))
        self.amp1_5x.triggered.connect(lambda: self.__amplitudeResize(1.5))
        self.amp1_2x.triggered.connect(lambda: self.__amplitudeResize(1.2))
        self.amp1x.triggered.connect(lambda: self.__amplitudeResize(1))
        self.amp0_8x.triggered.connect(lambda: self.__amplitudeResize(0.8))
        self.amp0_5x.triggered.connect(lambda: self.__amplitudeResize(0.5))
        self.amp0_3x.triggered.connect(lambda: self.__amplitudeResize(0.3))
        self.amp0_1x.triggered.connect(lambda: self.__amplitudeResize(0.1))

    #move buttons
    def __onbtnFirstClicked(self):
        self.UpdateSampleIndex(0, True)
    def __onbtnLastClicked(self):
        self.UpdateSampleIndex(self.recording.duration_samp-self.T, True)
    def __onbtnPreviousClicked(self):
        if(self.SampleIndex>math.floor(self.T*0.3)):
            self.UpdateSampleIndex(self.SampleIndex - math.floor(self.T*0.3), True)
        else:
            self.UpdateSampleIndex(0, True)
    def __onbtnNextClicked(self):
        if(self.SampleIndex<(self.recording.duration_samp - 1.3*math.floor(self.T))):
            self.UpdateSampleIndex(self.SampleIndex + math.floor(self.T*0.3), True)
        else:
            self.UpdateSampleIndex(self.recording.duration_samp - self.T, True)
    def __onbtnPreviousSimilarYClicked(self):
        if(self.SampleIndex>self.T):
            self.UpdateSampleIndex(self.SampleIndex-self.T,True)
        else:
            self.UpdateSampleIndex(0,True)
    def __onbtnNextSimilarYClicked(self):
        if(self.SampleIndex<(self.recording.duration_samp-2*self.T)):
            self.UpdateSampleIndex(self.SampleIndex+self.T,True)
        else:
            self.UpdateSampleIndex(self.recording.duration_samp-self.T,True)

    #slider+spinbox
    def __onsldValueChanged(self):
        self.UpdateSampleIndex(self.sldSampleIndex.value(), True, self.sldSampleIndex)
    def __onnmrValueChanged(self):
        self.UpdateSampleIndex(self.nmrSampleIndex.value()*self.fs, True, self.nmrSampleIndex)

    #checkboxes + duplicate&print buttons
    def __onchbFavoriteStateChanged(self, state):
        if(self.chbFavorite.isChecked()):
            self.FavoriteList.append([self.SampleIndex/self.fs,self.SampleIndex/self.fs+self.window])
            print(self.FavoriteList)
        else:
            self.FavoriteList.remove([self.SampleIndex/self.fs,self.SampleIndex/self.fs+self.window])
            print(self.FavoriteList)

    def __onchbFitStateChanged(self, state):
        self.scale_factor = 1
        self.fit_to_pane = state
        self.Plot()
    
    def __onchbNightStateChanged(self, state):
        if(state):
            self.night_mode = 1
            self.axis.setBackgroundBrush(QtGui.QBrush(QtGui.QColor(0, 0, 0, 255))) # set background color here
            self.Plot()
        else:
            self.night_mode = 0
            self.axis.setBackgroundBrush(QtGui.QBrush(QtGui.QColor(255, 255, 255, 255))) # set background color here
            self.Plot() 

    def __onbtnDuplicate(self):
        self.DuplicateCurrent()
    
    def DuplicateCurrent(self):
        if(self.verbose):                
            print('detaching...')
        MainWindow = QtWidgets.QMainWindow()
        plotter = plotter_ui(MainWindow=MainWindow, recording=self.recording, window =self.window, start = 0,y=self.y, title=self.title, fs=self.fs, sens=self.sens, channelNames=self.ChannelNames, callback=self.callback)
        self.detachedWindows.append(plotter)
        MainWindow.show()
        MainWindow.resize(self.MainWindow.size())
        plotter.UpdateSampleIndex(self.SampleIndex, rePlot=True, triggeredSignals = False)

    def __onbtnPrintClicked(self):
        printer = QtPrintSupport.QPrinter(QtPrintSupport.QPrinter.HighResolution)
        dialog = QtPrintSupport.QPrintDialog(printer, self.MainWindow)
        if dialog.exec_() == QtPrintSupport.QPrintDialog.Accepted:
            self.handle_paint_request(printer)

    def handle_paint_request(self, printer):
        printer.setPaperSize(QtPrintSupport.QPrinter.A4)
        painter = QtGui.QPainter()
        # Start painter
        painter.begin(printer)
        scaleX = printer.pageRect().width() / self.MainWindow.rect().width()
        scaleY = printer.pageRect().height() / self.MainWindow.rect().height()
        useScale = min(scaleX, scaleY)
        painter.scale(useScale, useScale)
        # Grab a widget you want to print
        screen = self.MainWindow.grab()
        # Draw grabbed pixmap
        painter.drawPixmap(0, 0, screen)
        # End painting
        painter.end()

    ###menubar
    # channels menu
    def __onbtnChannelsAdd(self):
        self.ch_ui = channel_UI()
        self.ch_window = QtWidgets.QMainWindow()
        self.ch_ui.setupUi(self.ch_window)
        self.ch_window.show()
        all_channels = ['fp1','fp2','f3','f4','p3','p4','c3','c4','t1','t2','t3','t4','t5','t6','o1','o2','a1','a2','f7','f8','fz','cz','pz','ecg','emg','resp','sao2','eogl','eogr','pulse']
        self.ch_ui.channelsList.addItems(all_channels)
        self.ch_ui.btnChannels.setText("Add channel(s)")
        self.ch_ui.btnChannels.clicked.connect(self.addChannels)
    
    def addChannels(self):
        channels = self.ch_ui.channelsList.selectedItems()
        for i in range(len(channels)):
            self.ChannelNames.append(str(self.ch_ui.channelsList.selectedItems()[i].text()))
        self.ch_window.close()
        self.Plot()
    
    def __onbtnChannelsRemove(self):
        self.ch_ui = channel_UI()
        self.ch_window = QtWidgets.QMainWindow()
        self.ch_ui.setupUi(self.ch_window)
        self.ch_window.show()
        self.ch_ui.channelsList.addItems(self.ChannelNames)
        self.ch_ui.btnChannels.clicked.connect(self.removeChannels)

    def removeChannels(self):
        channels = self.ch_ui.channelsList.selectedItems()
        for i in range(len(channels)):
            self.ChannelNames.remove(str(self.ch_ui.channelsList.selectedItems()[i].text()))
        self.ch_window.close()
        self.Plot()

    # timescale menu
    def __windowResize(self, window):
        if self.window == window:
            return
        if self.window < window : 
            if(window*self.recording.fs < self.recording.duration_samp):
                self.window_scale = self.window_scale*window/self.window
                self.window = window
                self.T = int(int(self.recording.fs)*self.window)
                self.__UpdateTotalNumberOfSamples()
            else:
                self.window = self.recording.duration_sec
                self.T = int(int(self.recording.fs)*self.window)
                self.__UpdateTotalNumberOfSamples
            self.Plot()
        else:       
            self.window_scale = self.window_scale/(self.window/window)  
            self.T = int(int(self.recording.fs) * window)
            self.__UpdateTotalNumberOfSamples()
            if self.T > self.window/window:
                self.window = window
                self.Plot()
            else:
                self.window = window
                self.T = int(int(self.recording.fs) * self.window)
                self.__UpdateTotalNumberOfSamples()

    # amplitude menu
    def __amplitudeResize(self, scale):
        if self.scale_factor == scale:
            return
        else:
            self.scale_factor = 1/scale
        self.__UpdateAmplitude()
        self.Plot()
        
    class struct():
        pass