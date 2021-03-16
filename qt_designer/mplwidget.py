# Imports
from PyQt5 import QtWidgets
from math import ceil
from PyQt5 import QtWidgets, QtCore
from matplotlib.gridspec import GridSpec
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

# Matplotlib canvas class to create figure
class MplCanvas(FigureCanvas):
    """
    Frontend class. This is the FigureCanvas as well as plotting functionality.
    Plotting use pyqt5.
    """

    def __init__(self, parent=None):
        self.figure = Figure()

        gs = GridSpec(1,1)
        self.axes = self.figure.axes

        super().__init__(self.figure)

        self.canvas = self.figure.canvas
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.updateGeometry()
        self.setParent(parent)

    def add(self, cols=2):
        N = len(self.axes) + 1
        rows = int(ceil(N / cols))
        grid = GridSpec(rows, cols)

        for gs, ax in zip(grid, self.axes):
            ax.set_position(gs.get_position(self.figure))

        name = self.figure.add_subplot(grid[N-1])
        self.axes = self.figure.axes
        self.canvas.draw()
        return name


# Matplotlib widget
class MplWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)   # Inherit from QWidget
        self.canvas = MplCanvas()                  # Create canvas object
        self.vbl = QtWidgets.QVBoxLayout()         # Set box for plotting
        self.vbl.addWidget(self.canvas)
        self.setLayout(self.vbl)