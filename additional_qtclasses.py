from PyQt5 import QtCore, QtGui, QtWidgets

class QLabel_Clickable(QLabel):
    clicked=pyqtSignal()

    def mousePressEvent(self, ev):
        self.clicked.emit()