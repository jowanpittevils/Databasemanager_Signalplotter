
# dependencies
 - numpy
 - matplotlib
 - pyqt5
 - pyqtgraph

# Signal Plotter 
'SignalPlotter.Plotter' has two usefull functions for multichannel timeseries visualization:
 - iplot(x): (inline plot) for plotting one segment of data, x is a matrix with a size of (time-samples , channel)
 - gplot(x): (GUI plot) for plotting multiple segments of data, x is a tensor with a size of (semgents, time-samples , channel). 
 
# gplot (graphical-plot)
gplot uses qt GUI for plotting the tensor.

## inputs:
 - x:           the inout tensore. Its dimension should be as (S: Samples, T: Time, K: Channel) (the same as the default dimension of Keras)
                        for instance (200 segments, 10s * 250 hz, 20 channels)
 - y:           optional, the labels of segments. It must be a vector with size of S.
 - title:       optional, the tile of the window.
 - fs:          optional [default is None], the sampling frequensy. If fs is None the data will be plotted in samples, otherwise in seconds. 
                        if fs is -1, then the mean of signal on the Time mode will be plotted with a bar graph. 
 - sens:        optional [default is None], normalizing factor. If it is None, the signals will be normalize automatically with the min and max of each channel in each segment.
 - channelNames:optional [default is None], the name of channels to be plotted on the y-axis.
 - callback:    optional [default is None], a function as func(x, sampleIndex) to be called when the user change the sample index by the GUI.
 - in order to plot tensors on top of each other (holded graphs), x should be a List in List: [[x]] (see below examples)
        
## output: 
list of selected indexes (as favorite)
    
## examples: 
'x=numpy.random.randn(15,fs*10,20)'

 * Standard:

            iplot(x[0,])

            gplot(x)
            gplot(x,title='title', sens=10)
            fav=gplot(x, y=y,title=title, fs=fs, channelNames=chn)

 * Bar graph: fs=-1

            gplot([x4,x4/2,x4*3], fs=-1)

 * Plot holded graphs: '[[]]'

            gplot([[x,x/2,x*3]])
            gplot([[x,x/2,x*3]], fs=-1)

 * plot linked graphs '[]'

            gplot([x1,x2,x3], y=y,title=[title1, title2, title3], fs=[fs1,fs2,fs3], channelNames=[chn1,chn2,chn3])
            gplot([x1,x2,x3], y=y,title=[title1, None, title3], fs=fsAll, channelNames=[chn1,None,None])
            gplot([x1,x2,[x3 , x4]], y=y,title=[title1, None, title3], fs=[fs1,fs2,-1], channelNames=[chn1,None,None])
