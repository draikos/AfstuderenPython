import sys
import time
from collections import defaultdict

import matplotlib
# Make sure that we are using QT5
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np

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
        MyMainWindow.d = defaultdict(list)
        MyMainWindow.dictionary = {}
        self.setupUi(self)
        self.setupMappingVisualisation()

        self.show()

    def keyPressEvent(self, e):

        if e.key() == Qt.Key_Escape:
            self.update()
            self.rowValue.connect(self.addmpl)

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
            self.rowValue.emit(v)
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
                    break;
                lastFrameTime = currentTime

        print("--- %s seconds ---" % (time.time() - start_time))

    def addmpl(self, v):
        print(v)

        # fig1 = Figure()
        # ax1f1 = fig1.add_subplot(111)
        # value = self.d.get("dataSensor1")
        # ax1f1.plot(value)
        # self.canvas = FigureCanvas(fig1)
        # self.gridLayout.addWidget(self.canvas)
        # self.canvas.draw()





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