from dataset_selector import *
import sys
import numpy as np
from databasemanager import *



def open_datasets(self):
    self.myOtherWindow = QtWidgets.QMainWindow()
    self.ui = UI_dataset()
    self.ui.setupUi(self.myOtherWindow)
    self.myOtherWindow.show()