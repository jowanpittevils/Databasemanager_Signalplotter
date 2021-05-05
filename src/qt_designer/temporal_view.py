# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\temporal_view.ui'
#
# Created by: PyQt5 UI code generator 5.15.3
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_TemporalView(object):
    def setupUi(self, TemporalView):
        TemporalView.setObjectName("TemporalView")
        TemporalView.resize(650, 450)
        TemporalView.setMinimumSize(QtCore.QSize(600, 400))
        self.centralwidget = QtWidgets.QWidget(TemporalView)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.StartLabel = QtWidgets.QLabel(self.centralwidget)
        self.StartLabel.setObjectName("StartLabel")
        self.verticalLayout_2.addWidget(self.StartLabel)
        self.GapLabel = QtWidgets.QLabel(self.centralwidget)
        self.GapLabel.setObjectName("GapLabel")
        self.verticalLayout_2.addWidget(self.GapLabel)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.StartEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.StartEdit.setObjectName("StartEdit")
        self.verticalLayout.addWidget(self.StartEdit)
        self.GapEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.GapEdit.setObjectName("GapEdit")
        self.verticalLayout.addWidget(self.GapEdit)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.gridLayout_2.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.EventsCheckbox = QtWidgets.QCheckBox(self.centralwidget)
        self.EventsCheckbox.setObjectName("EventsCheckbox")
        self.gridLayout_2.addWidget(self.EventsCheckbox, 1, 0, 1, 1)
        self.gridLayout.addLayout(self.gridLayout_2, 0, 0, 1, 1)
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.Slider = QtWidgets.QSlider(self.centralwidget)
        self.Slider.setOrientation(QtCore.Qt.Horizontal)
        self.Slider.setObjectName("Slider")
        self.gridLayout_3.addWidget(self.Slider, 0, 0, 1, 1)
        self.sliderValue = QtWidgets.QLabel(self.centralwidget)
        self.sliderValue.setObjectName("sliderValue")
        self.gridLayout_3.addWidget(self.sliderValue, 0, 1, 1, 1)
        self.gridLayout.addLayout(self.gridLayout_3, 1, 0, 1, 1)
        self.TemporalPlot = MplWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.TemporalPlot.sizePolicy().hasHeightForWidth())
        self.TemporalPlot.setSizePolicy(sizePolicy)
        self.TemporalPlot.setObjectName("TemporalPlot")
        self.gridLayout.addWidget(self.TemporalPlot, 2, 0, 1, 1)
        TemporalView.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(TemporalView)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 650, 25))
        self.menubar.setObjectName("menubar")
        TemporalView.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(TemporalView)
        self.statusbar.setObjectName("statusbar")
        TemporalView.setStatusBar(self.statusbar)

        self.retranslateUi(TemporalView)
        QtCore.QMetaObject.connectSlotsByName(TemporalView)

    def retranslateUi(self, TemporalView):
        _translate = QtCore.QCoreApplication.translate
        TemporalView.setWindowTitle(_translate("TemporalView", "Temporal Profile"))
        self.StartLabel.setText(_translate("TemporalView", "Start:"))
        self.GapLabel.setText(_translate("TemporalView", "Recording gap:"))
        self.EventsCheckbox.setText(_translate("TemporalView", "Show Events"))
        self.sliderValue.setText(_translate("TemporalView", "sliderValue"))
from qt_designer.mplwidget import MplWidget


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    TemporalView = QtWidgets.QMainWindow()
    ui = Ui_TemporalView()
    ui.setupUi(TemporalView)
    TemporalView.show()
    sys.exit(app.exec_())
