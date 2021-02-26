from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QCursor


class Qlabel_click(QtWidgets.QLabel):
    clicked=QtCore.pyqtSignal()
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setCursor(QCursor(QtCore.Qt.PointingHandCursor))

    def mousePressEvent(self, ev):
        self.clicked.emit()
        print('testttt')