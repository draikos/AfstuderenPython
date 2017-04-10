import sys
import time
from collections import defaultdict

import matplotlib
# Make sure that we are using QT5
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
import peakutils

from PyQt5.QtWidgets import QSizePolicy
from PyQt5.QtWidgets import QDialog, QApplication, qApp
from PyQt5.QtCore import Qt, QEvent, QThread, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QWidget


from GUI.UI.Ui_MainWindow import Ui_MainWindow
from GUI.Data import ReadFile


class MyMainWindow(QMainWindow, Ui_MainWindow):
    rowValue = pyqtSignal(int)
    def __init__(self, parent=None):
        super(MyMainWindow, self).__init__(parent)
        self.d = defaultdict(list)
        self.dictionary = {}
        self.myList = list()

        self.setupUi(self)
        self.setupMappingVisualisation()
        self.addmpl()
        self.peakDetection()
        self.show()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.update()
        if e.key() == Qt.Key_X:
            self.peakDetection()


    def setupMappingVisualisation(self):
        layout = self.gridLayout_3
        counterValue = 0
        i = 24
        j = 8
        for g in range(i):
            if g == 0 or g == 23:
                for t in range(j):
                    if t == 0 or t == 7:
                        self.dictionary["widget{0}".format(counterValue)] = QWidget()
                        test = self.dictionary.get("widget{0}".format(counterValue))
                        test.setMinimumHeight(20)
                        test.setMinimumWidth(20)
                        test.setMaximumHeight(60)
                        test.setMaximumWidth(60)
                        layout.addWidget(test, t, g)
                        counterValue+= 1

                    else:
                        self.dictionary["widget{0}".format(counterValue)] = QWidget()
                        test = self.dictionary.get("widget{0}".format(counterValue))
                        test.setMinimumHeight(20)
                        test.setMinimumWidth(20)
                        test.setMaximumHeight(60)
                        test.setMaximumWidth(60)
                        test.setAutoFillBackground(True)
                        test.setStyleSheet("background-color: red")
                        layout.addWidget(test, t, g)
                        counterValue += 1
            else:
                for t in range(j):
                    self.dictionary["widget{0}".format(counterValue)] = QWidget()
                    test = self.dictionary.get("widget{0}".format(counterValue))
                    test.setMinimumHeight(20)
                    test.setMinimumWidth(20)
                    test.setMaximumHeight(60)
                    test.setMaximumWidth(60)
                    test.setAutoFillBackground(True)
                    test.setStyleSheet("background-color: green")
                    layout.addWidget(test, t, g)
                    counterValue += 1
        start_time = time.time()
        object1 = ReadFile.ReadFile()
        limit = 0
        for rows in object1.ws.rows:
            if limit <= 100:
                c = 0
                for cell in rows:
                    self.d["dataSensor{0}".format(c)].append(cell.value)
                    c += 1
            else:
                break;
            limit += 1
        print("--- %s seconds ---" % (time.time() - start_time))

    def update(self):
        FPS = 60
        counterSensor = 0
        counterValue = 0
        lastFrameTime = time.time()
        start_time = time.time()
        test2 = self.dictionary
        test = self.d
        print("--- %s seconds ---" % (time.time() - start_time))
        for v in range(len(self.d.get("dataSensor0"))):
            QApplication.processEvents()
            while True:
                currentTime = time.time()
                sleepTime = 1. / FPS - (currentTime - lastFrameTime)
                if sleepTime > 0:
                    for x in range(len(self.d)):
                        if x == 0 or x == 7 or x == 184 or x == 191:
                            pass
                        else:
                            value = test.get("dataSensor{0}".format(x))[v]
                            test2["widget{0}".format(x)].setStyleSheet(
                                "background-color: rgb(244, {0}, {0})".format(value * 150))
                            test2["widget{0}".format(x)].repaint()
                    # self.updatePlot(v)
                    break;
                lastFrameTime = currentTime

        print("--- %s seconds ---" % (time.time() - start_time))

    def addmpl(self):
        self.test = mpl()
        self.gridLayout.addWidget(self.test)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)

    def updatePlot(self, v):
        if not self.myList :
            for c in self.d.get("dataSensor1"):
                self.myList.append(c)
        markers_on = [v]
        self.test.axes.plot(self.myList, color="black")
        self.test.axes.axvline(x = markers_on, color="red")
        self.test.draw()
        del(self.test.axes.lines[-1])

    def peakDetection(self):
        myList = list()
        for v in range(len(self.d)):
            if v == 0 or v == 7 or v == 183 or v == 191:
                pass;
            else:
                indexes = peakutils.indexes(self.d.get("dataSensor{0}".format(v)), thres=1, min_dist=30)
                if not indexes:
                    pass;
                else:
                    # for index in np.nditer(indexes):
                    #     searchRange = index + 20
                    #     prevValue = self.d.get("dataSensor1")[index]
                    #     loopAmount = 0
                    #     highestLoop = 0
                    #     highestValue = 0
                    #     for value in self.d.get("dataSensor1")[index:searchRange]:
                    #         currentValue = value
                    #         value -= prevValue
                    #         value = abs(value)
                    #         prevValue = currentValue
                    #         if loopAmount == 0:
                    #              highestValue = value
                    #              pass;
                    #         elif highestValue < value:
                    #             highestValue = value
                    #             highestLoop = loopAmount
                    #         loopAmount += 1
                    #     print(str(highestValue) + " " + str(indexes + highestLoop) +" "+ str(v))

class mpl(FigureCanvas):
    def __init__(self, parent=None):
        self.fig = Figure()
        self.fig.set_tight_layout("tight")
        self.axes = self.fig.add_subplot(111)

        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)
        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas(self.fig)
        FigureCanvas.draw(self)



class DataThread(QThread):
    progress = pyqtSignal(int)

    def __init__(self):
        QThread.__init__(self)

    def __del__(self):
        self.wait()

    def run(self):
        print()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = MyMainWindow()
    sys.exit(app.exec_())