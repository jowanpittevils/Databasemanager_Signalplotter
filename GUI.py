#%%
#%reload_ext autoreload
#%autoreload 2


#%%

from base_GUI import *
import sys
import numpy as np
from databasemanager import *

#%%

root = 'C:\\db\\toyDB'
db = Database(root)
db.summary()

#%%


UserSettings.global_settings().loading_data_missing_channel_type = 'error'
UserSettings.global_settings().loading_data_channels = ['fp1','fp2','t3','t4','o1','o2','c3','c4']
ds = db.load_dataset('ds1')

subjects = ds.subjects
recordings = []
for rec in subjects[1].recordings:
    recordings.append(rec.name)


subject_names = ds.subject_names

annotations = ['annotation1','annotation2', 'annotation3', 'annotation4']
events = ['event1','event2']

app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(MainWindow)


ui.subject_list.addItems(subject_names)
ui.recordings_list.addItems(recordings)
ui.annotations_list.addItems(annotations)
ui.events_list.addItems(events)


MainWindow.show()
sys.exit(app.exec_())
# %%
