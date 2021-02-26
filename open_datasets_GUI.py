from dataset_selector import *
import sys
import numpy as np
from databasemanager import *
from PyQt5 import *


def get_dataset(self):
    self.myOtherWindow = QtWidgets.QMainWindow()
    self.ui2 = UI_dataset()
    self.ui2.setupUi(self.myOtherWindow)
    self.ui2.listWidget.addItems(self.datasets)
    self.myOtherWindow.show()
    self.ui2.listWidget.itemDoubleClicked.connect(self.doubleclick)
