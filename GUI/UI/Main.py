import sys
import time
from collections import defaultdict

from PyQt5.QtWidgets import QDialog, QApplication, qApp
from PyQt5.QtCore import Qt, QEvent, QThread, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QWidget

from GUI.UI.Ui_MainWindow import Ui_MainWindow
from GUI.Data import ReadFile

class MyMainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MyMainWindow, self).__init__(parent)
        MyMainWindow.d = defaultdict(list)
        MyMainWindow.dictionary = {}
        self.setupUi(self)
        self.setupMappingVisualisation()
        self.show()

    def keyPressEvent(self, e):

        if e.key() == Qt.Key_Escape:

            self.update = DataThread()
            self.update.start()
            self.update.progress.connect(self.paintWidget)


    def paintWidget(self, x):
        print(x)


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
            if limit <= 600:
                c = 0
                for cell in rows:
                    self.d["dataSensor{0}".format(c)].append(cell.value)
                    c += 1
            else:
                break;
            limit += 1
        print("--- %s seconds ---" % (time.time() - start_time))

    #------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # updater

class DataThread(QThread):
    progress = pyqtSignal(int)

    def __init__(self):
        QThread.__init__(self)
        self.d = MyMainWindow.d
        self.dictionary = MyMainWindow.dictionary


    def __del__(self):
        self.wait()

    @pyqtSlot()
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
            while True:
                currentTime = time.time()
                sleepTime = 1. / FPS - (currentTime - lastFrameTime)
                if sleepTime > 0:
                    for x in range(len(self.d)):
                        if x == 0 or x == 7 or x == 184 or x == 191:
                            pass
                        else:
                            print("test")
                            value = test.get("dataSensor{0}".format(x))[v]
                            # widget = test2["widget{0}".format(x)].setStyleSheet(
                            #     "background-color: rgb({0}, {0}, {0})".format(value * 150))
                            self.progress.emit(x)
                            DataThread.wait(1000)



                    break;
                lastFrameTime = currentTime
        print("--- %s seconds ---" % (time.time() - start_time))

    def run(self):
        self.update()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MyMainWindow()
    sys.exit(app.exec_())