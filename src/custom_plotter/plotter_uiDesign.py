# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'plotter_uiDesign.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1092, 906)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.lblTitle = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.lblTitle.setFont(font)
        self.lblTitle.setAlignment(QtCore.Qt.AlignCenter)
        self.lblTitle.setObjectName("lblTitle")
        self.verticalLayout.addWidget(self.lblTitle)
        self.sldSampleIndex = QtWidgets.QSlider(self.centralwidget)
        self.sldSampleIndex.setOrientation(QtCore.Qt.Horizontal)
        self.sldSampleIndex.setObjectName("sldSampleIndex")
        self.verticalLayout.addWidget(self.sldSampleIndex)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.btnFirst = QtWidgets.QPushButton(self.centralwidget)
        self.btnFirst.setObjectName("btnFirst")
        self.horizontalLayout.addWidget(self.btnFirst)
        self.btnPreviousSimilarY = QtWidgets.QPushButton(self.centralwidget)
        self.btnPreviousSimilarY.setObjectName("btnPreviousSimilarY")
        self.horizontalLayout.addWidget(self.btnPreviousSimilarY)
        self.btnPrevious = QtWidgets.QPushButton(self.centralwidget)
        self.btnPrevious.setObjectName("btnPrevious")
        self.horizontalLayout.addWidget(self.btnPrevious)
        self.btnAmpUp = QtWidgets.QPushButton(self.centralwidget)
        self.btnAmpUp.setObjectName("btnAmpUp")
        self.horizontalLayout.addWidget(self.btnAmpUp)
        self.btnAmpDown = QtWidgets.QPushButton(self.centralwidget)
        self.btnAmpDown.setObjectName("btnAmpDown")
        self.horizontalLayout.addWidget(self.btnAmpDown)
        self.label = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.lblAmplitude = QtWidgets.QLabel(self.centralwidget)
        self.lblAmplitude.setText("")
        self.lblAmplitude.setObjectName("lblAmplitude")
        self.horizontalLayout.addWidget(self.lblAmplitude)
        self.nmrSampleIndex = QtWidgets.QSpinBox(self.centralwidget)
        self.nmrSampleIndex.setObjectName("nmrSampleIndex")
        self.horizontalLayout.addWidget(self.nmrSampleIndex)
        self.lblTotalSamples = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblTotalSamples.sizePolicy().hasHeightForWidth())
        self.lblTotalSamples.setSizePolicy(sizePolicy)
        self.lblTotalSamples.setMaximumSize(QtCore.QSize(60, 16777215))
        self.lblTotalSamples.setObjectName("lblTotalSamples")
        self.horizontalLayout.addWidget(self.lblTotalSamples)
        self.btnWindowUp = QtWidgets.QPushButton(self.centralwidget)
        self.btnWindowUp.setObjectName("btnWindowUp")
        self.horizontalLayout.addWidget(self.btnWindowUp)
        self.btnWindowDown = QtWidgets.QPushButton(self.centralwidget)
        self.btnWindowDown.setObjectName("btnWindowDown")
        self.horizontalLayout.addWidget(self.btnWindowDown)
        self.btnNext = QtWidgets.QPushButton(self.centralwidget)
        self.btnNext.setObjectName("btnNext")
        self.horizontalLayout.addWidget(self.btnNext)
        self.btnNextSimilarY = QtWidgets.QPushButton(self.centralwidget)
        self.btnNextSimilarY.setObjectName("btnNextSimilarY")
        self.horizontalLayout.addWidget(self.btnNextSimilarY)
        self.btnLast = QtWidgets.QPushButton(self.centralwidget)
        self.btnLast.setObjectName("btnLast")
        self.horizontalLayout.addWidget(self.btnLast)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.axis = PlotWidget(self.centralwidget)
        self.axis.setObjectName("axis")
        self.verticalLayout.addWidget(self.axis)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.chbFavorite = QtWidgets.QCheckBox(self.centralwidget)
        self.chbFavorite.setObjectName("chbFavorite")
        self.horizontalLayout_2.addWidget(self.chbFavorite)
        self.btnDuplicate = QtWidgets.QPushButton(self.centralwidget)
        self.btnDuplicate.setMaximumSize(QtCore.QSize(25, 16777215))
        self.btnDuplicate.setObjectName("btnDuplicate")
        self.horizontalLayout_2.addWidget(self.btnDuplicate)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1092, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.lblTitle.setText(_translate("MainWindow", "Title"))
        self.btnFirst.setToolTip(_translate("MainWindow", "Jump to the first segment"))
        self.btnFirst.setText(_translate("MainWindow", "<<"))
        self.btnPreviousSimilarY.setToolTip(_translate("MainWindow", "Jump to the previous similar segment"))
        self.btnPreviousSimilarY.setText(_translate("MainWindow", "<|"))
        self.btnPrevious.setToolTip(_translate("MainWindow", "Go to the previous segment"))
        self.btnPrevious.setText(_translate("MainWindow", "<"))
        self.btnAmpUp.setText(_translate("MainWindow", "+"))
        self.btnAmpDown.setText(_translate("MainWindow", "-"))
        self.label.setText(_translate("MainWindow", "Amplitude:"))
        self.nmrSampleIndex.setToolTip(_translate("MainWindow", "Sample index (starts from 0)"))
        self.lblTotalSamples.setToolTip(_translate("MainWindow", "Total number fo samples"))
        self.lblTotalSamples.setText(_translate("MainWindow", "/ 99999999"))
        self.btnWindowUp.setText(_translate("MainWindow", "Window+"))
        self.btnWindowDown.setText(_translate("MainWindow", "Window-"))
        self.btnNext.setToolTip(_translate("MainWindow", "Go to the next segment"))
        self.btnNext.setText(_translate("MainWindow", ">"))
        self.btnNextSimilarY.setToolTip(_translate("MainWindow", "Jump to the next similar segment"))
        self.btnNextSimilarY.setText(_translate("MainWindow", "|>"))
        self.btnLast.setToolTip(_translate("MainWindow", "Jump to the last segment"))
        self.btnLast.setText(_translate("MainWindow", ">>"))
        self.chbFavorite.setToolTip(_translate("MainWindow", "Mark as favorite"))
        self.chbFavorite.setText(_translate("MainWindow", "*"))
        self.btnDuplicate.setToolTip(_translate("MainWindow", "Duplicate"))
        self.btnDuplicate.setText(_translate("MainWindow", "D"))
from pyqtgraph import PlotWidget


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
