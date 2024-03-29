# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\dataset_selector.ui'
#
# Created by: PyQt5 UI code generator 5.15.3
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
import os

class Ui_dataset(object):
    def setupUi(self, dataset):
        icon = QtGui.QIcon()
        plg_dir = os.path.dirname(__file__)
        icon.addPixmap(QtGui.QPixmap(plg_dir+"\\heartbeat.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        dataset.setWindowIcon(icon)
        dataset.setObjectName("dataset")
        dataset.resize(190, 170)
        dataset.setMinimumSize(QtCore.QSize(190, 170))
        self.centralwidget = QtWidgets.QWidget(dataset)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.listWidget = QtWidgets.QListWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.listWidget.sizePolicy().hasHeightForWidth())
        self.listWidget.setSizePolicy(sizePolicy)
        self.listWidget.setMinimumSize(QtCore.QSize(1, 1))
        self.listWidget.setObjectName("listWidget")
        self.horizontalLayout.addWidget(self.listWidget)
        dataset.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(dataset)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 190, 25))
        self.menubar.setObjectName("menubar")
        dataset.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(dataset)
        self.statusbar.setObjectName("statusbar")
        dataset.setStatusBar(self.statusbar)

        self.retranslateUi(dataset)
        QtCore.QMetaObject.connectSlotsByName(dataset)

    def retranslateUi(self, dataset):
        _translate = QtCore.QCoreApplication.translate
        dataset.setWindowTitle(_translate("dataset", "Dataset_selector"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    dataset = QtWidgets.QMainWindow()
    ui = Ui_dataset()
    ui.setupUi(dataset)
    dataset.show()
    sys.exit(app.exec_())
