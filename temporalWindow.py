from PyQt5 import QtWidgets, QtChart, QtGui, QtCore
import sys
from PyQt5 import QtChart




class Window(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Temporal Window")
        self.setGeometry(100,100, 680,500)
        self.show()
        self.create_bar()




    def create_bar(self):
        #The QBarSet class represents a set of bars in the bar chart.
         # It groups several bars into a bar set

        set0 = QtChart.QBarSet("subject1")
        set1 = QtChart.QBarSet("subject2")
        set2 = QtChart.QBarSet("subject3")
        set3 = QtChart.QBarSet("subject4")
        set4 = QtChart.QBarSet("subject4")

        set0 << 1 << 2 << 3 << 4 << 5 << 6
        set1 << 5 << 0 << 0 << 4 << 0 << 7
        set2 << 3 << 5 << 8 << 13 << 8 << 5
        set3 << 5 << 6 << 7 << 3 << 4 << 5
        set4 << 9 << 7 << 5 << 3 << 1 << 2

        series = QtChart.QPercentBarSeries()
        series.append(set0)
        series.append(set1)
        series.append(set2)
        series.append(set3)
        series.append(set4)

        chart = QtChart.QChart()
        chart.addSeries(series)
        chart.setTitle("Percent Example")
        chart.setAnimationOptions(QtChart.QChart.SeriesAnimations)

        categories = ["1", "2", "3", "4", "5", "6"]
        axis = QtChart.QBarCategoryAxis()
        axis.append(categories)
        chart.createDefaultAxes()
        chart.setAxisX(axis, series)

        chart.legend().setVisible(True)
        chart.legend().setAlignment(QtCore.Qt.AlignBottom)

        chartView = QtChart.QChartView(chart)
        chartView.setRenderHint(QtGui.QPainter.Antialiasing)

        self.setCentralWidget(chartView)





App = QtWidgets.QApplication(sys.argv)
window = Window()
sys.exit(App.exec_())