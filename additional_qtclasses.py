from PyQt5 import QtCore, QtGui, QtWidgets

class QLabel_Clickable(QtWidgets.QLabel):
    clicked=QtCore.pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

    def mousePressEvent(self, ev):
        self.clicked.emit()

class lineEdit_autocomplete(QtWidgets.QLineEdit):
    model = QtCore.QStringListModel()
    completer = QtWidgets.QCompleter()
    def start(self, subject_names):
        self.model.setStringList(subject_names)
        self.completer.setModel(self.model)
        self.setCompleter(self.completer)