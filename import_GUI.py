# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'import_GUI.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_LoadWindow(object):
    def setupUi(self, LoadWindow):
        LoadWindow.setObjectName("LoadWindow")
        LoadWindow.resize(1569, 1012)
        self.centralwidget = QtWidgets.QWidget(LoadWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.db_name = QtWidgets.QLineEdit(self.centralwidget)
        self.db_name.setGeometry(QtCore.QRect(190, 30, 1111, 41))
        self.db_name.setObjectName("db_name")
        self.ds_name = QtWidgets.QLineEdit(self.centralwidget)
        self.ds_name.setGeometry(QtCore.QRect(190, 100, 1111, 41))
        self.ds_name.setObjectName("ds_name")
        self.db_root = QtWidgets.QLabel(self.centralwidget)
        self.db_root.setGeometry(QtCore.QRect(20, 30, 171, 31))
        self.db_root.setObjectName("db_root")
        self.ds_root = QtWidgets.QLabel(self.centralwidget)
        self.ds_root.setGeometry(QtCore.QRect(20, 100, 171, 31))
        self.ds_root.setObjectName("ds_root")
        self.browse1 = QtWidgets.QPushButton(self.centralwidget)
        self.browse1.setGeometry(QtCore.QRect(1330, 30, 168, 51))
        self.browse1.setObjectName("browse1")
        self.browse2 = QtWidgets.QPushButton(self.centralwidget)
        self.browse2.setGeometry(QtCore.QRect(1330, 100, 168, 51))
        self.browse2.setObjectName("browse2")
        self.dataset_list = QtWidgets.QListWidget(self.centralwidget)
        self.dataset_list.setGeometry(QtCore.QRect(10, 250, 371, 651))
        self.dataset_list.setObjectName("dataset_list")
        self.datasets = QtWidgets.QLabel(self.centralwidget)
        self.datasets.setGeometry(QtCore.QRect(10, 200, 111, 31))
        self.datasets.setObjectName("datasets")
        self.Load = QtWidgets.QPushButton(self.centralwidget)
        self.Load.setGeometry(QtCore.QRect(210, 190, 168, 51))
        self.Load.setObjectName("Load")
        LoadWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(LoadWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1569, 43))
        self.menubar.setObjectName("menubar")
        LoadWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(LoadWindow)
        self.statusbar.setObjectName("statusbar")
        LoadWindow.setStatusBar(self.statusbar)

        self.retranslateUi(LoadWindow)
        QtCore.QMetaObject.connectSlotsByName(LoadWindow)

    def retranslateUi(self, LoadWindow):
        _translate = QtCore.QCoreApplication.translate
        LoadWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.db_root.setText(_translate("MainWindow", "Database root:"))
        self.ds_root.setText(_translate("MainWindow", "Dataset folder:"))
        self.browse1.setText(_translate("MainWindow", "Browse"))
        self.browse2.setText(_translate("MainWindow", "Browse"))
        self.datasets.setText(_translate("MainWindow", "Datasets:"))
        self.Load.setText(_translate("MainWindow", "Load"))
 

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_LoadWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
