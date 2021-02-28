#%%
#%reload_ext autoreload
#%autoreload 2
#%%
from loadGui_wrapper import loadGUI_wrapper
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import numpy as np
#%%

app = QtWidgets.QApplication(sys.argv)
w = loadGUI_wrapper()
w.show()
sys.exit(app.exec_())
# %%
