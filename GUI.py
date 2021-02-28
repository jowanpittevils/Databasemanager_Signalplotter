#%%
#%reload_ext autoreload
#%autoreload 2
#%%
from GUI_wrapper import GUI_wrapper
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import numpy as np
#%%

app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()
ui = GUI_wrapper()

ui.setupUi(MainWindow)
ui.Dataset_label.clicked.connect(lambda: ui.get_dataset())
ui.lineEdit.textChanged.connect(lambda: ui.update_subject_list())


MainWindow.show()
#ui.get_dataset()
sys.exit(app.exec_())
# %%
