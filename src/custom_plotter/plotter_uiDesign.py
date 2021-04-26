# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\plotter_uiDesign.ui'
#
# Created by: PyQt5 UI code generator 5.15.3
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1103, 919)
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
        self.btnNext = QtWidgets.QPushButton(self.centralwidget)
        self.btnNext.setObjectName("btnNext")
        self.horizontalLayout.addWidget(self.btnNext)
        self.btnNextSimilarY = QtWidgets.QPushButton(self.centralwidget)
        self.btnNextSimilarY.setObjectName("btnNextSimilarY")
        self.horizontalLayout.addWidget(self.btnNextSimilarY)
        self.btnLast = QtWidgets.QPushButton(self.centralwidget)
        self.btnLast.setObjectName("btnLast")
        self.horizontalLayout.addWidget(self.btnLast)
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
        self.btnAmpUp = QtWidgets.QPushButton(self.centralwidget)
        self.btnAmpUp.setObjectName("btnAmpUp")
        self.horizontalLayout.addWidget(self.btnAmpUp)
        self.btnAmpDown = QtWidgets.QPushButton(self.centralwidget)
        self.btnAmpDown.setObjectName("btnAmpDown")
        self.horizontalLayout.addWidget(self.btnAmpDown)
        self.btnWindowUp = QtWidgets.QPushButton(self.centralwidget)
        self.btnWindowUp.setObjectName("btnWindowUp")
        self.horizontalLayout.addWidget(self.btnWindowUp)
        self.btnWindowDown = QtWidgets.QPushButton(self.centralwidget)
        self.btnWindowDown.setObjectName("btnWindowDown")
        self.horizontalLayout.addWidget(self.btnWindowDown)
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
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.axis = PlotWidget(self.centralwidget)
        self.axis.setObjectName("axis")
        self.verticalLayout.addWidget(self.axis)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.chbFit = QtWidgets.QCheckBox(self.centralwidget)
        self.chbFit.setObjectName("chbFit")
        self.horizontalLayout_2.addWidget(self.chbFit)
        self.chbNight = QtWidgets.QCheckBox(self.centralwidget)
        self.chbNight.setObjectName("chbNight")
        self.horizontalLayout_2.addWidget(self.chbNight)
        self.chbFavorite = QtWidgets.QCheckBox(self.centralwidget)
        self.chbFavorite.setObjectName("chbFavorite")
        self.horizontalLayout_2.addWidget(self.chbFavorite)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.btnDuplicate = QtWidgets.QPushButton(self.centralwidget)
        self.btnDuplicate.setMaximumSize(QtCore.QSize(25, 16777215))
        self.btnDuplicate.setObjectName("btnDuplicate")
        self.horizontalLayout_2.addWidget(self.btnDuplicate)
        self.btnPrint = QtWidgets.QPushButton(self.centralwidget)
        self.btnPrint.setObjectName("btnPrint")
        self.horizontalLayout_2.addWidget(self.btnPrint)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1103, 25))
        self.menubar.setObjectName("menubar")
        self.menusignals = QtWidgets.QMenu(self.menubar)
        self.menusignals.setObjectName("menusignals")
        self.menutimescale = QtWidgets.QMenu(self.menubar)
        self.menutimescale.setObjectName("menutimescale")
        self.menuamplitude = QtWidgets.QMenu(self.menubar)
        self.menuamplitude.setObjectName("menuamplitude")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.signals_add = QtWidgets.QAction(MainWindow)
        self.signals_add.setObjectName("signals_add")
        self.signals_remove = QtWidgets.QAction(MainWindow)
        self.signals_remove.setObjectName("signals_remove")
        self.window1sec = QtWidgets.QAction(MainWindow)
        self.window1sec.setObjectName("window1sec")
        self.window2sec = QtWidgets.QAction(MainWindow)
        self.window2sec.setObjectName("window2sec")
        self.window5sec = QtWidgets.QAction(MainWindow)
        self.window5sec.setObjectName("window5sec")
        self.window10sec = QtWidgets.QAction(MainWindow)
        self.window10sec.setObjectName("window10sec")
        self.window20sec = QtWidgets.QAction(MainWindow)
        self.window20sec.setObjectName("window20sec")
        self.window30sec = QtWidgets.QAction(MainWindow)
        self.window30sec.setObjectName("window30sec")
        self.window60sec = QtWidgets.QAction(MainWindow)
        self.window60sec.setObjectName("window60sec")
        self.amp0_1x = QtWidgets.QAction(MainWindow)
        self.amp0_1x.setObjectName("amp0_1x")
        self.amp0_3x = QtWidgets.QAction(MainWindow)
        self.amp0_3x.setObjectName("amp0_3x")
        self.amp0_5x = QtWidgets.QAction(MainWindow)
        self.amp0_5x.setObjectName("amp0_5x")
        self.action0_05 = QtWidgets.QAction(MainWindow)
        self.action0_05.setObjectName("action0_05")
        self.action0_02x = QtWidgets.QAction(MainWindow)
        self.action0_02x.setObjectName("action0_02x")
        self.amp1x = QtWidgets.QAction(MainWindow)
        self.amp1x.setObjectName("amp1x")
        self.amp2x = QtWidgets.QAction(MainWindow)
        self.amp2x.setObjectName("amp2x")
        self.amp1_5x = QtWidgets.QAction(MainWindow)
        self.amp1_5x.setObjectName("amp1_5x")
        self.amp5x = QtWidgets.QAction(MainWindow)
        self.amp5x.setObjectName("amp5x")
        self.amp0_8x = QtWidgets.QAction(MainWindow)
        self.amp0_8x.setObjectName("amp0_8x")
        self.amp1_2x = QtWidgets.QAction(MainWindow)
        self.amp1_2x.setObjectName("amp1_2x")
        self.menusignals.addAction(self.signals_add)
        self.menusignals.addAction(self.signals_remove)
        self.menutimescale.addAction(self.window1sec)
        self.menutimescale.addAction(self.window2sec)
        self.menutimescale.addAction(self.window5sec)
        self.menutimescale.addAction(self.window10sec)
        self.menutimescale.addAction(self.window20sec)
        self.menutimescale.addAction(self.window30sec)
        self.menutimescale.addAction(self.window60sec)
        self.menuamplitude.addAction(self.amp5x)
        self.menuamplitude.addAction(self.amp2x)
        self.menuamplitude.addAction(self.amp1_5x)
        self.menuamplitude.addAction(self.amp1_2x)
        self.menuamplitude.addAction(self.amp1x)
        self.menuamplitude.addAction(self.amp0_8x)
        self.menuamplitude.addAction(self.amp0_5x)
        self.menuamplitude.addAction(self.amp0_3x)
        self.menuamplitude.addAction(self.amp0_1x)
        self.menubar.addAction(self.menusignals.menuAction())
        self.menubar.addAction(self.menutimescale.menuAction())
        self.menubar.addAction(self.menuamplitude.menuAction())

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
        self.btnNext.setToolTip(_translate("MainWindow", "Go to the next segment"))
        self.btnNext.setText(_translate("MainWindow", ">"))
        self.btnNextSimilarY.setToolTip(_translate("MainWindow", "Jump to the next similar segment"))
        self.btnNextSimilarY.setText(_translate("MainWindow", "|>"))
        self.btnLast.setToolTip(_translate("MainWindow", "Jump to the last segment"))
        self.btnLast.setText(_translate("MainWindow", ">>"))
        self.nmrSampleIndex.setToolTip(_translate("MainWindow", "Sample index (starts from 0)"))
        self.lblTotalSamples.setToolTip(_translate("MainWindow", "Total number fo samples"))
        self.lblTotalSamples.setText(_translate("MainWindow", "/ 99999999"))
        self.btnAmpUp.setText(_translate("MainWindow", "Amplitude+"))
        self.btnAmpDown.setText(_translate("MainWindow", "Amplitude-"))
        self.btnWindowUp.setText(_translate("MainWindow", "Timescale+"))
        self.btnWindowDown.setText(_translate("MainWindow", "Timescale-"))
        self.label.setText(_translate("MainWindow", "Amplitude:"))
        self.chbFit.setText(_translate("MainWindow", "Fit to pane"))
        self.chbNight.setText(_translate("MainWindow", "Night mode"))
        self.chbFavorite.setToolTip(_translate("MainWindow", "Mark as favorite"))
        self.chbFavorite.setText(_translate("MainWindow", "Favorite"))
        self.btnDuplicate.setToolTip(_translate("MainWindow", "Duplicate"))
        self.btnDuplicate.setText(_translate("MainWindow", "D"))
        self.btnPrint.setText(_translate("MainWindow", "Print"))
        self.menusignals.setTitle(_translate("MainWindow", "Channels"))
        self.menutimescale.setTitle(_translate("MainWindow", "Timescale"))
        self.menuamplitude.setTitle(_translate("MainWindow", "Amplitude"))
        self.signals_add.setText(_translate("MainWindow", "add"))
        self.signals_remove.setText(_translate("MainWindow", "remove"))
        self.window1sec.setText(_translate("MainWindow", "1sec/window"))
        self.window2sec.setText(_translate("MainWindow", "2sec/window"))
        self.window5sec.setText(_translate("MainWindow", "5sec/window"))
        self.window10sec.setText(_translate("MainWindow", "10sec/window"))
        self.window20sec.setText(_translate("MainWindow", "20sec/window"))
        self.window30sec.setText(_translate("MainWindow", "30sec/window"))
        self.window60sec.setText(_translate("MainWindow", "60sec/window"))
        self.amp0_1x.setText(_translate("MainWindow", "0.1x"))
        self.amp0_3x.setText(_translate("MainWindow", "0.3x"))
        self.amp0_5x.setText(_translate("MainWindow", "0.5x"))
        self.action0_05.setText(_translate("MainWindow", "0.05x"))
        self.action0_02x.setText(_translate("MainWindow", "0.02x"))
        self.amp1x.setText(_translate("MainWindow", "1x"))
        self.amp2x.setText(_translate("MainWindow", "2x"))
        self.amp1_5x.setText(_translate("MainWindow", "1.5x"))
        self.amp5x.setText(_translate("MainWindow", "5x"))
        self.amp0_8x.setText(_translate("MainWindow", "0.8x"))
        self.amp1_2x.setText(_translate("MainWindow", "1.2x"))
from pyqtgraph import PlotWidget


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
