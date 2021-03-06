import os
import sys
from collections import OrderedDict
from collections import defaultdict

import matplotlib
import numpy as np
import copy
from PyQt5.QtGui import QMouseEvent
from PyQt5.QtWidgets import QAction
from PyQt5.QtWidgets import QMenuBar

matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from PyQt5.QtWidgets import QSizePolicy, qApp, QFileDialog
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt, pyqtSignal, QEvent
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QWidget

from GUI.UI.Ui_MainWindow import Ui_MainWindow
from GUI.Data.detect_peaks import detect_peaks


class MyMainWindow(QMainWindow, Ui_MainWindow):
    rowValue = pyqtSignal(int)
    def __init__(self):
        QMainWindow.__init__(self)
        # initialization of the class wide variables
        self.d = defaultdict(list)
        self.waveDictionary = defaultdict(list)
        self.dictionary = {}
        self.myList = list()
        self.LATdictionary = defaultdict(list)
        self.orderedQRSList = defaultdict(list)
        self.num_plots = 0
        self.SensorNumber = 1
        self.cleanedUpWaveDictionary = defaultdict(list)
        self.stop = False
        self.x = 0
        self.currentIterations = 0
        self.List = list()
        qApp.installEventFilter(self)
        self.setMouseTracking(True)
        self.switch = False
        self.qrsFilterValues = list()
        self.qrsFilteredList = list()
        self.qrsBeforeFilterList = list()
        self.coordinateList = list()
        self.fileName = r"C:\Users\draikos\Desktop\Marshall Croes\data\AF\Hovig_20_10_14_AF_LA3.E01"
        # self.fileName = r"F:\Marshall Croes\data\AF\Hovig_20_10_14_AF_LA2.E01"




        self.press = None
        self.cur_xlim = None
        self.cur_ylim = None
        self.x0 = None
        self.y0 = None
        self.x1 = None
        self.y1 = None
        self.xpress = None
        self.ypress = None




        self.setupUi(self)
        self.setupMappingVisualisation()
        self.peakDetection()
        self.calculateWave()
        self.addmpl()
        self.createUI()
        self.show()
        self.SensorClickEvent()

    def processtrigger(self, q):
        print(q.text() + " is triggered")

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.update()
        if e.key() == Qt.Key_X:
            self.peakDetection()
            self.calculateWave()
        if e.key() == Qt.Key_1:
            self.stop = True
        if e.key() == Qt.Key_2:
            self.changePlotSensorUp()
        if e.key() == Qt.Key_3:
            self.changePlotSensorDown()
        if e.key() == Qt.Key_4:
            self.qrsDetection()
        if e.key() == Qt.Key_5:
            print(self.switch)
            if self.switch == False:
                self.switch = True
            else:
                self.switch = False
        if e.key() == Qt.Key_6:
            self.qrsFiltering()
            self.calculateWave()
            self.peakDetection()

        if e.key() == Qt.Key_7:
            self.surroundingSensorCheckQRSFiltering()

        if e.key() == Qt.Key_O:
            self.changeFile()

    def createUI(self):
        self.setWindowTitle('AF viewer')
        menu = self.menuBar.addMenu('File')
        action = menu.addAction('Change File Path')
        action.triggered.connect(self.changeFile)
        self.lineEdit.setText(str(self.SensorNumber))
        self.pushButton.clicked.connect(self.buttonClicked)
        self.pushButton_2.clicked.connect(self.buttonClicked2)

    def buttonClicked(self):
        self.update()

    def buttonClicked2(self):
        self.stop = True

    def changeFile(self):
        options = QFileDialog.Options()
        self.fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()",
                                                       r'C:\Users\draikos\Desktop\Marshall Croes\data\AF',
                                                       "All Files (*);;Python Files (*.py)", options=options)
        self.setupMappingVisualisation()
        self.peakDetection()
        self.resetPlot()

        #   setup of the color mapping part
    def setupMappingVisualisation(self):
        layout = self.gridLayout_2
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
                        test.setStyleSheet("background-color: white")
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
                    test.setStyleSheet("background-color: white")
                    layout.addWidget(test, t, g)
                    counterValue += 1

        # hardcoded don't forget to fix
        # Reading of the .E01 files
        with open(self.fileName, 'rb') as fid:
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
                    while i < 1000:
                        self.d["dataSensor{0}".format(sensorID)].append(value[i] / gradient)
                        i += 1
                    sensorID += 1
                    break;

    ####################################################################################################################
    def eventFilter(self, obj, event):
        if event.type() == QEvent.MouseButtonPress and obj == self.test:
            if self.switch == False:
                self.panning(event)
            else:
                self.qrsGetValues(event)
        if event.type() == QEvent.MouseButtonRelease and obj == self.test:
            if self.switch == False:
                self.release(event)
        if event.type() == QEvent.MouseMove and obj == self.test:
            self.onMotion(event)
        return super(MyMainWindow, self).eventFilter(obj, event)

    # update the GUI.
    def update(self):
        sensors = self.dictionary
        keyPlace = list()
        color = (["red", "orange", "yellow", "pink", "blue", "violet", "blue", "black", "grey"])
        i = 0
        # get the amount of times the code has to loop, error with this part, has to be rewritten so it doesn't loop to the end but takes another value
        for v in range(len(self.d.get("dataSensor0"))):
            QApplication.processEvents()
            print(v, 'eerste ')
            if v <= self.currentIterations:
                v == self.currentIterations
                continue
            if self.stop:
                self.currentIterations = v
                self.stop = False
                return
            while v <= 1000:
                for x in range(len(self.d)):
                    if x == 0 or x == 7 or x == 184 or x == 191:
                        pass
                    else:
                        if [v, x] in [x for x in self.orderedWaveCalculations.values() for x in x]:
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
                self.turnBackColors(v)
                break;

    def qrsGetValues(self, event):
        if len(self.coordinateList) == 0:
            self.coordinateList.append(event.globalX())
        elif len(self.coordinateList) == 1:
            self.coordinateList.append(event.globalX())
            self.filterQRS()
            self.coordinateList.clear()


    def filterQRS(self):
        firstvalue = self.coordinateList[0] - 455
        secondvalue = self.coordinateList[1] - 455
        self.qrsBeforeFilterList.append([firstvalue, secondvalue])

    def qrsFiltering(self):
        for value in self.qrsBeforeFilterList:
            firstvalue = value[0]
            secondvalue = value[1]
            for amount in range(len(self.d)):
                i = 0
                for value in self.d.get("dataSensor{0}".format(amount)):
                    if i >= firstvalue and i <= secondvalue:
                        self.d.get("dataSensor{0}".format(amount))[i] = 0
                    i += 1







################################################################################################################


    def surroundingSensorCheckQRSFiltering(self):
        c = self.SensorNumber
        surroundingSensorList = list()
        currentSensor = list()
        missedQRSlist = list()
        orderedMissingQRSList = list()
        orderedMissingQRSListofLists = list()
        surroundingSensors = [(c - 9), (c - 8), (c - 7), (c - 1), c, (c + 1), (c + 7), (c + 8), (c + 9)]
        print("test")
        for values in surroundingSensors:
            for value in self.orderedWaveCalculations.values():
                for v in value:
                    if values == v[1]:
                        if values == self.SensorNumber:
                            currentSensor.append(v)
                        else:
                            surroundingSensorList.append(v)


        print("surrounding", surroundingSensorList)
        print("current", currentSensor)
        for value in currentSensor:
            for v in surroundingSensorList:
                if v[0]+5 >= value[0] and v[0]-5 <= value[0]:
                    pass
                else:
                    if v not in missedQRSlist:
                        missedQRSlist.append(v)
                    else:
                        pass


        for value in missedQRSlist:
            for v in missedQRSlist:
                if v[0] + 5 >= value[0] and v[0] - 5 <= value[0] and v!= value:
                    if v not in orderedMissingQRSList:
                        orderedMissingQRSList.append(v)
            orderedMissingQRSListofLists.append(copy.copy(orderedMissingQRSList))
            orderedMissingQRSList.clear()

        for value in orderedMissingQRSListofLists:
            waveValues = 0
            if len(value) > 2:
                for v in value:
                    waveValues += v[0]
                waveValue = int(waveValues / len(value))
                print(waveValue)
                for key, value in self.orderedWaveCalculations.items():
                    for c in value:
                        if self.SensorNumber == c[1]:
                            print(waveValue)
                            print(key,value)
                            self.orderedWaveCalculations[key].append([waveValue, self.SensorNumber])
                            break


################################################################################################################




    def removeKeys(self):
        print()


    def averageCalculations(self, averageHeight):
        test = 0
        currentAverageHeight = 0
        averageHeightList = list()
        averageHeight = 0
        previousValues = list()
        counterUp = 0
        counterDown = 0
        prevvalue = 0
        i = 0
        for value in self.d.get("dataSensor{0}".format(self.SensorNumber)):
            value = value - prevvalue
            i += 1
            if value > 0:
                counterDown = 0
                counterUp =+ 1
                previousValues.append(value)
            else:
                if not previousValues:
                    pass
                else:
                    counterDown += 1
                    print(counterDown)
                    if counterDown >= 3:
                        for value in previousValues:
                            test = test + value
                            currentAverageHeight = test / len(previousValues)
                            averageHeightList.append(currentAverageHeight)
                        previousValues.clear()
                        counterDown = 0
            value = prevvalue
        for averageHeightValue in averageHeightList:
            averageHeight = averageHeight + averageHeightValue
        averageHeight = averageHeight / len(averageHeightList)
        print(averageHeight)
        return averageHeight


    def turnBackColors(self, v):
        for value in self.orderedWaveCalculations.values():
            if v - 100 >= max(value[0]):
                for x in value:
                    self.dictionary["widget{0}".format(x[1])].setStyleSheet("background-color: white")
                    self.dictionary["widget{0}".format(x[1])].repaint()

    # Adds the graph at the bottom of the GUI
    def addmpl(self):
        self.test = mpl()
        self.gridLayout_3.addWidget(self.test)
        self.gridLayout_3.setSpacing(0)
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        if not self.myList:
            for c in self.d.get("dataSensor1"):
                self.myList.append(c)
        self.test.axes.plot(self.myList, color="black")
        self.test.draw()

    # Updates the plot every millisecond so you see the red line move, so you can see at what millisecond you are.
    def updatePlot(self, v):
        lines = self.test.axes.axvline(x=[v], color="red")
        self.test.axes.draw_artist(lines)
        self.createRedLines()
        self.test.draw()
        self.test.axes.lines[-1].remove()

    def changePlotSensorUp(self):
        if self.SensorNumber == 191:
            self.SensorNumber = 0
        else:
            self.SensorNumber += 1
        print(self.SensorNumber)
        self.myList.clear()
        for c in self.d.get("dataSensor{0}".format(self.SensorNumber)):
            self.myList.append(c)
        self.createRedLines()
        self.test.axes.lines[-1].remove()
        if not self.List:
            pass
        else:
            for values in self.List:
                lines = self.test.axes.axvline(x=[values[0]], color="red")
                self.test.axes.draw_artist(lines)
        self.test.axes.plot(self.myList, color="black")
        self.test.draw()
        for i, line in enumerate(self.test.axes.lines):
            line.remove()


    def resetPlot(self):
        self.createRedLines()
        self.myList.clear()
        for c in self.d.get("dataSensor{0}".format(self.SensorNumber)):
            self.myList.append(c)
        self.test.axes.lines[0].remove()
        self.test.axes.plot(self.myList, color="black")
        self.test.draw()

    def changePlotSensorDown(self):
        if self.SensorNumber == 0:
            self.SensorNumber = 191
        else:
            self.SensorNumber -= 1
        self.createRedLines()
        print(self.SensorNumber)
        self.myList.clear()
        for c in self.d.get("dataSensor{0}".format(self.SensorNumber)):
            self.myList.append(c)
        self.test.axes.lines[0].remove()
        self.test.axes.plot(self.myList, color="black")
        self.test.draw()


    def wheelEvent(self, QWheelEvent):
        ax = self.test.axes
        cur_xlim = ax.get_xlim()
        cur_xrange = (cur_xlim[1] - cur_xlim[0]) * .9
        xdata = QWheelEvent.globalX()
        test = QWheelEvent.angleDelta() / 120
        if test.y() == 1:
            scale_factor = 1 / 3.
        elif test.y() == -1:
            scale_factor = 1.
        else:
            scale_factor = 1
        ax.set_xlim([xdata - cur_xrange * scale_factor,
                     xdata + cur_xrange * scale_factor])
        self.test.draw()

    ####################################################################################################################
    def panning(self, event):
        ax = self.test.axes
        self.cur_xlim = ax.get_xlim()
        self.press = self.x0, event.globalX()
        self.x0, self.xpress = self.press

    def release(self, event):
        ax = self.test.axes
        self.press = None
        self.test.draw()
        self.updateGraph(event, value=self.SensorNumber)

    def onMotion(self, event):
        ax = self.test.axes
        if self.press is None: return
        dx = event.globalX() - self.xpress
        self.cur_xlim = list(self.cur_xlim)
        self.cur_xlim[0] -= dx / 20
        self.cur_xlim[1] -= dx / 20
        self.cur_xlim = tuple(self.cur_xlim)
        ax.set_xlim(self.cur_xlim)

        self.updateGraph(event, value=self.SensorNumber)
        self.test.draw()

    def SensorClickEvent(self):
        for value in range(len(self.dictionary)):
            self.dictionary["widget{0}".format(value)].mouseReleaseEvent = lambda event, value=value: self.updateGraph(
                event, value)


    def updateGraph(self, event, value):
        self.SensorNumber = value
        self.myList.clear()
        for c in self.d.get("dataSensor{0}".format(value)):
            self.myList.append(c)
        self.createRedLines()
        for i, line in enumerate(self.test.axes.lines):
            line.remove()
        for values in self.List:
            lines = self.test.axes.axvline(x=[values[0]], color="red")
            self.test.axes.draw_artist(lines)
        self.test.axes.plot(self.myList, color="black")
        self.lineEdit.setText(str(self.SensorNumber))
        self.test.draw()
        for i, line in enumerate(self.test.axes.lines):
            line.remove()

    # checks the peaks so that the LAT can be calculated
    def peakDetection(self):
        averageHeight = 0
        testList = list()
        average = self.averageCalculations(averageHeight)
        for v in range(len(self.d)):
            test = detect_peaks(self.d.get("dataSensor{0}".format(v)), mpd=70, mph=average)
            if len(detect_peaks(self.d.get("dataSensor{0}".format(v)), mpd=70, mph=average)) == 0:
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
                pass
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

    def createRedLines(self):
        self.List.clear()
        for value in self.orderedWaveCalculations.values():
            for v in value:
                if self.SensorNumber == v[1]:
                    print(v)
                    self.List.append(v)


    # this checks whether the wave itself passes certain criteria, if not it gets deleted.
    def cleanUpWave(self):
        dictionary = self.waveDictionary.items()
        for value in dictionary:
            if len(value[1]) < 4:
                pass
            else:
                for values in value[1]:
                    self.cleanedUpWaveDictionary[value[0]].append(values)
        self.orderedWaveCalculations = OrderedDict(sorted(self.cleanedUpWaveDictionary.items(), key=lambda x: x[1]))

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



sys._excepthook = sys.excepthook
def exception_hook(exctype, value, traceback):
    sys._excepthook(exctype, value, traceback)
    sys.exit(1)
sys.excepthook = exception_hook

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = MyMainWindow()
    try:
        sys.exit(app.exec_())
    except:
        print("Exiting")