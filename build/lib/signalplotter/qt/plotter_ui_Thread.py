from threading import Thread
import threading

class plotter_ui(Thread):
    def __init__(self, MainWindow, x, title=None,fs=1, sens=None, channelNames=None):
        Thread.__init__(self)
        self.lock = threading.Lock()
        
        self.MainWindow = MainWindow
        self.x = x
        self.title = title
        self.fs = fs
        self.sens = sens
        self.channelNames = channelNames
        
    def run(self):
        self.plotter_ui = plotter_ui(self.MainWindow, self.x, self.title, self.fs, self.sens, self.channelNames)