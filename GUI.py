#%%
#%reload_ext autoreload
#%autoreload 2
#%%
from GUI_wrapper import *
import sys
import numpy as np
from databasemanager import *
from open_datasets_GUI import *


#%%
root = 'C:\\db\\toyDB'
#%%

#%%

app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()
ui = GUI_wrapper()

ui.setupUi(MainWindow)
ui.Dataset_label.clicked.connect(lambda: get_dataset(ui))

MainWindow.show()
get_dataset(ui)
sys.exit(app.exec_())
# %%
