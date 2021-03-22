from signalplotter.qt.plotter_ui import plotter_ui
from signalplotter.plotter import plotter_countainer
import matplotlib.pyplot as plt
import numpy as np
import math
import numbers
from databasemanager import *


class plot(Object):
        

        def __init__(self, window=30, title=None,fs=1,sens=None,channel_names=None, callback=None, channel_first:bool = True, verbose:bool = True, lazy_plotting:bool = True):
                self.window = window
                self.title = title
                self.fs = fs
                self.sens = sens
                self.channel_names = channel_names
                self.callback = callback
                self.channel_first = channel_first
                self.verbose = verbose

                                                                                        

        def cplot(self, recording):
                self.recording = recording
                x = self.recording.get_data()
                if(type(x) != list):
                        x=[x]
                                                                                                # shape = 1, #channels, #time intervals       
                self.x = self.prepare_x(self.x, self.window, self.fs, self.channel_first)            # shape = 1, #segments, #channels, #time intervals per segment
                self.gplot(self, x=self.x, y=None, title=self.title, fs=self.fs, sens=self.sens,channel_names=self.channel_names, callback=self.callback, channel_first=self.channel_first, verbose=selfverbose)
        
                
                


        def prepare_x(self, x, window, fs, channel_first):
                if(type(x) == list):
                        xx = []
                        for i in range(len(x)):
                                xx.append(self.prepare_x(x[i], window, fs, channel_first))
                        return xx

                assert(isinstance(x, np.ndarray))
                print(x.ndim)
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

        
        def gplot(self, x, y=None, title=None,fs=1,sens=None,channel_names=None, callback=None, channel_first:bool = True, verbose:bool = True):
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

                self.recording_plotter_container = plotter_countainer()
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

                for i in range(N):
                        self.recording_plotter_container.add(x[i],y,title[i],fs[i],sens[i],channel_names[i],callback[i], channel_first, verbose)



                return self.recording_plotter_container.getFavorites()