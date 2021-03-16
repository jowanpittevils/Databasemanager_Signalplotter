# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'temporal_view.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_TemporalView(object):
    def setupUi(self, TemporalView):
        TemporalView.setObjectName("TemporalView")
        TemporalView.resize(886, 449)
        self.centralwidget = QtWidgets.QWidget(TemporalView)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
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
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        self.EventsCheckbox = QtWidgets.QCheckBox(self.centralwidget)
        self.EventsCheckbox.setObjectName("EventsCheckbox")
        self.verticalLayout_3.addWidget(self.EventsCheckbox)
        self.verticalLayout_4.addLayout(self.verticalLayout_3)
        self.TemporalPlot = MplWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.TemporalPlot.sizePolicy().hasHeightForWidth())
        self.TemporalPlot.setSizePolicy(sizePolicy)
        self.TemporalPlot.setObjectName("TemporalPlot")
        self.verticalLayout_4.addWidget(self.TemporalPlot)
        TemporalView.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(TemporalView)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 886, 21))
        self.menubar.setObjectName("menubar")
        TemporalView.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(TemporalView)
        self.statusbar.setObjectName("statusbar")
        TemporalView.setStatusBar(self.statusbar)

        self.retranslateUi(TemporalView)
        QtCore.QMetaObject.connectSlotsByName(TemporalView)

    def retranslateUi(self, TemporalView):
        _translate = QtCore.QCoreApplication.translate
        TemporalView.setWindowTitle(_translate("TemporalView", "MainWindow"))
        self.StartLabel.setText(_translate("TemporalView", "Start:"))
        self.GapLabel.setText(_translate("TemporalView", "Recording gap:"))
        self.EventsCheckbox.setText(_translate("TemporalView", "Show Events"))
from qt_designer.mplwidget import MplWidget


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    TemporalView = QtWidgets.QMainWindow()
    ui = Ui_TemporalView()
    ui.setupUi(TemporalView)
    TemporalView.show()
    sys.exit(app.exec_())
