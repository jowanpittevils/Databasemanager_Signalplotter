#%%
%reload_ext autoreload
%autoreload 2


#%%

from eerste_test import *
import sys

#%%

app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(MainWindow)
entries = ['one','two', 'three', 'four']
ui.listWidget_annotations.addItems(entries)
MainWindow.show()
sys.exit(app.exec_())