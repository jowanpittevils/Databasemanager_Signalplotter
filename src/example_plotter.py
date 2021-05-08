from database_explorer_plotter.extra_functions import plot_browser
from databasemanager import *


root = "A:\\db\\toyDB"
data_root = "A:\\db\\toyDB\\data"
db = Database(root)

ds = db.load_dataset('all')

recording = ds.subjects[1].recordings[0]

def callback():
    print("Callback working!")

plot_browser(recording = recording, window=30, start=0, y=None, title=None,fs=1,sens=None,channel_names=None, callback=callback(), verbose = True)
