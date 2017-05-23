import sys
import time
from collections import defaultdict
from collections import OrderedDict
import numpy as np
import os

import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from PyQt5.QtWidgets import QSizePolicy
from PyQt5.QtWidgets import QDialog, QApplication, qApp
from PyQt5.QtCore import Qt, QEvent, QThread, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QWidget


from GUI.UI.Ui_MainWindow import Ui_MainWindow
from GUI.Data import ReadFile
from GUI.Data.detect_peaks import detect_peaks


class MyMainWindow(QMainWindow, Ui_MainWindow):
    rowValue = pyqtSignal(int)
    def __init__(self, parent=None):
        super(MyMainWindow, self).__init__(parent)
        # initialization of the class wide variables
        self.d = defaultdict(list)
        self.waveDictionary = defaultdict(list)
        self.dictionary = {}
        self.myList = list()
        self.LATdictionary = defaultdict(list)
        self.num_plots = 0
        self.cleanedUpWaveDictionary = defaultdict(list)

        self.setupUi(self)
        self.setupMappingVisualisation()
        self.peakDetection()
        self.calculateWave()
        self.addmpl()
        self.show()
        self.update()


    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.update()
        if e.key() == Qt.Key_X:
            self.peakDetection()
            self.calculateWave()

#   setup of the color mapping part
    def setupMappingVisualisation(self):
        layout = self.gridLayout_3
        counterValue = 0
        # hardcoded, need to be fixed
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

        # hardcoded don't forget to fix
        # Reading of the .E01 files
        filename = r"C:\Users\758051\Desktop\Jelle van den Toren\Hovig_20_10_14_AF_LA2.E01"
        with open(filename, 'rb') as fid:
            fid.seek(4608, os.SEEK_SET)
            data_array = np.fromfile(fid, np.int16).reshape((-1, 256)).T
            gradient = max(np.gradient(data_array[191]))

        # filling a dictionary with the following data [sensor, [all the data in the sensor from .E01 file]]
        i = 0
        sensorID = 0
        for value in data_array:
            if sensorID >= 192:
                break;
            else:
                for i in range(len(value)):
                    while i < 100:
                        self.d["dataSensor{0}".format(sensorID)].append(value[i] / gradient)
                        i += 1
                    sensorID += 1
                    break;

    #   update the GUI.
    def update(self):
        sensors = self.dictionary
        dataOfSensors = self.d
        keyPlace = list()
        color = (["red", "orange", "yellow", "pink", "blue", "violet", "blue", "black", "grey"])
        # get the amount of times the code has to loop, error with this part, has to be rewritten so it doesn't loop to the end but takes another value
        for v in range(len(self.d.get("dataSensor0"))):
            QApplication.processEvents()
            while True:
                for x in range(len(self.d)):
                    if x == 0 or x == 7 or x == 184 or x == 191:
                        pass
                    else:
                        if [v, x] in [x for v in self.orderedWaveCalculations.values() for x in v]:
                            for key, values in self.waveDictionary.items():
                                if [v, x] in values:
                                    if key in keyPlace:
                                        sensors["widget{0}".format(x)].setStyleSheet(
                                            "background-color: {0}".format(color[keyPlace.index(key)]))
                                    else:
                                        if len(keyPlace) == 9:
                                            keyPlace.clear()
                                        keyPlace.append(key)
                                        sensors["widget{0}".format(x)].setStyleSheet(
                                            "background-color: {0}".format(color[keyPlace.index(key)]))

                                sensors["widget{0}".format(x)].repaint()
                self.updatePlot(v)
                break;

    # Adds the graph at the bottom of the GUI
    def addmpl(self):
        self.test = mpl()
        self.gridLayout.addWidget(self.test)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        if not self.myList:
            for c in self.d.get("dataSensor1"):
                self.myList.append(c)
        self.test.axes.plot(self.myList, color="black")
        self.test.draw()

    # Updates the plot every millisecond so you see the red line move, so you can see at what millisecond you are.
    def updatePlot(self, v):
        lines = self.test.axes.axvline(x=[v], color="red")
        self.test.axes.draw_artist(lines)
        self.test.draw()
        self.test.axes.lines[-1].remove()

    # checks the peaks so that the LAT can be calculated
    def peakDetection(self):
        testList = list()
        for v in range(len(self.d)):
            test = detect_peaks(self.d.get("dataSensor{0}".format(v)), mpd=30, mph=0.8)
            if len(detect_peaks(self.d.get("dataSensor{0}".format(v)), mpd=30, mph=0.8)) == 0:
                testList.append([0])
            else:
                testList.append(test)
            for index in testList[v]:
                searchRange = index + 30
                prevValue = self.d.get("dataSensor{0}".format(v))[index]
                loopAmount = 0
                highestLoop = 0
                highestValue = 0
                for value in self.d.get("dataSensor{0}".format(v))[index:searchRange]:
                    currentValue = value
                    value -= prevValue
                    value = abs(value)
                    prevValue = currentValue
                    if loopAmount == 0:
                         highestValue = value
                         pass;
                    elif highestValue < value:
                        highestValue = value
                        highestLoop = loopAmount
                    loopAmount += 1
                indexes = index + highestLoop
                self.LATdictionary["Sensor{0}".format(v)].append(indexes)

    def calculateWave(self):
        # Calculates what is part of a heartwave and what isn't, it first excludes the outer edges of the colormap because they are part of a different calculation
        for c in range(len(self.LATdictionary)):
            finalRow = len(self.LATdictionary) - 8
            if c%8 == 0 or c%8 == 7 or c <= 7 or c >= finalRow:
                print("")
            else:
                #checks for surrounding sensors
                surroundingSensors = [(c - 9), (c - 8), (c - 7), (c - 1), (c + 1), (c + 7), (c + 8), (c + 9)]
                for value in self.LATdictionary.get("Sensor{0}".format(c)):
                    lengthWaveDictionary = [value, c]
                    # checks if the current value + the sensor are already in the wavedictionary, the wavedictionary is a dictionary that contains all the heart waves
                    if [value, c] in [x for v in self.waveDictionary.values() for x in v]:
                        for key, values in self.waveDictionary.items():
                            if [value, c] in values:
                                lengthWaveDictionary = key
                    # checks whether the data passes certain criteria to become part of a wave, if the data passes the criteria it gets added to the wavedictionary.
                    for test in surroundingSensors:
                        sensorValueCheck = self.LATdictionary.get("Sensor{0}".format(test))
                        for valueCheck in sensorValueCheck:
                            if value-4 <= valueCheck <= value+4:
                                if [valueCheck,test] in [x for v in self.waveDictionary.values() for x in v]:
                                    pass
                                else:
                                    self.waveDictionary["{0}".format(lengthWaveDictionary)].append([valueCheck, test])
        self.cleanUpWave()

    # this checks whether the wave itself passes certain criteria, if not it gets deleted.
    def cleanUpWave(self):
        dictionary = self.waveDictionary.items()
        for value in dictionary:
            if len(value[1]) < 4:
                pass
            else:
                for values in value[1]:
                    print(values)
                    self.cleanedUpWaveDictionary[value[0]].append(values)
        self.orderedWaveCalculations = OrderedDict(sorted(self.cleanedUpWaveDictionary.items(), key=lambda x: x[1]))
        for value in self.cleanedUpWaveDictionary.items():
            print(value)

# work in progress
    def redrawGraph(self):
        print()

# the class that creates the graph
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

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = MyMainWindow()
    sys.exit(app.exec_())