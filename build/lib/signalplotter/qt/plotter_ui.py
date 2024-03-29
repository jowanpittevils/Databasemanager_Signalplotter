from .plotter_uiDesign import Ui_MainWindow
import pyqtgraph as pg
import numpy as np
from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5 import QtWidgets

class plotter_ui(QObject, Ui_MainWindow):
    __lastID = 0
    @classmethod
    def __getNewID(cls):
        cls.__lastID += 1
        return cls.__lastID
    
    IndexChanged = pyqtSignal(int, int)
    def __init__(self, MainWindow, x, y=None, title=None,fs=1, sens=None, channelNames=None, callback=None, channelFirst=True, verbose=True):
        super().__init__()
        
        if(type(x) == list):
            self.xx = x
            self.x = x[0]
        else:
            self.xx = [x]
            self.x = x
        self.verbose = verbose
        self.norm = plotter_ui.struct()
        self.norm.totalMaxX = max([tx.max() for tx in self.xx])
        self.norm.totalMinX = min([tx.min() for tx in self.xx])
        
        self.ID = plotter_ui.__getNewID()
        self.FavoriteList=set()
        self.setupUi(MainWindow)
        self.MainWindow = MainWindow
        self.channelFirst = channelFirst
        N = self.x.shape[0]
        self.callback = callback
        if(self.channelFirst):
            self.T = self.x.shape[2]
            self.CH = self.x.shape[1]
        else:
            self.T = self.x.shape[1]
            self.CH = self.x.shape[2]

        self.__UpdateFs(fs)
        self.sens = sens
        self.__UpdateTitleText(title)
        self.axis.showGrid(True,True)
        self.ChannelNames = channelNames
        self.__UpdateY(y)

        self.__UpdateTotalNumberOfSamples(N)
        self.UpdateSampleIndex(0)
        self.Plot()
        self.__AssignCallbacks()
        self.detachedWindows=[]
        
    def __UpdateTitleText(self, title):
        self.title = title
        wintitle =  str(self.ID) + '-Signal plotter'
        if(title is not None):
            wintitle += ' - ' + title
        self.MainWindow.setWindowTitle(wintitle)
        
        
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
                self.axis.setLabel('bottom', 'Time', units='s')
            self.T_sec = self.T/fs
        else:
            self.axis.setLabel('bottom', 'Sample')
            
    def __UpdateChannelNames(self, channelNames, areChannelsVertical):
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
        if(self.callback is not None):
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
            M = max([v.max() for v in x0])
            m = min([v.min() for v in x0])
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
        if(self.fs != -1):
            self.PlotLine(self.xx, self.SampleIndex)
            self.__UpdateChannelNames(self.ChannelNames, True)
        else:
            self.PlotBar(self.xx,self.SampleIndex)
            self.__UpdateChannelNames(self.ChannelNames, False)
            
    def PlotLine(self, xx, sampleIndex):
        xx = [v[sampleIndex,] for v in xx]
        xx = self.__iNormalize(xx, self.sens)
        xx = self.__AddBias(xx)
        
        t = np.arange(self.T)
        if(self.fs is not None):
            t = t / self.fs
            
        self.Clear()
        for i, xxi in enumerate(xx):
            for ch in range(self.CH):
                if(self.channelFirst):
                    self.axis.plot(t,xxi[ch,:], pen=self.GetPen(i))
                else:
                    self.axis.plot(t,xxi[:,ch], pen=self.GetPen(i))
            
        vb = self.axis.getViewBox()
        vb.setLimits(yMin=-1, yMax=self.CH, xMin = 0, xMax=t[-1])
        self.__UpdateTitle()
    def GetColorString(self, colorIndex=0):
        strL = ('#4363d8', '#800000', '#3cb44b', '#ffe119', '#f58231', '#911eb4', '#46f0f0', '#f032e6', '#bcf60c', '#fabebe', '#008080', '#e6beff', '#9a6324', '#fffac8', '#aaffc3', '#808000', '#e6194b', '#ffd8b1', '#000075', '#808080', '#ffffff', '#000000')
        return str(strL[colorIndex])
    def GetPen(self, colorIndex=0):
        return pg.mkPen(self.GetColorString(colorIndex))
    def PlotBar(self, xx, sampleIndex):
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
         
        vb = self.axis.getViewBox()
        m = min(self.norm.totalMinX-1,0)
        M = self.norm.totalMaxX * 1.1
        vb.setLimits(yMin=m, yMax=M, xMin = -1, xMax=t[-1]+1)
        self.__UpdateTitle()
        
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
        plotter = plotter_ui(MainWindow=MainWindow, x=self.xx, y=self.y, title=self.title, fs=self.fs, sens=self.sens, channelNames=self.ChannelNames, callback=self.callback)
        self.detachedWindows.append(plotter)
        MainWindow.show()
        MainWindow.resize(self.MainWindow.size())
        plotter.UpdateSampleIndex(self.SampleIndex, rePlot=True, triggeredSignals = False)
        
    class struct():
        pass

       
                