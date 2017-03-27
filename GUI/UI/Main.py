import sys
import time
from collections import defaultdict
from PyQt5.QtWidgets import QDialog, QApplication, qApp
from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QWidget
from GUI.UI.Ui_MainWindow import Ui_MainWindow
from GUI.Data import ReadFile

class MyMainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MyMainWindow, self).__init__(parent)
        qApp.installEventFilter(self)
        self.setupUi(self)
        self.setupMappingVisualisation()
        self.show()

    def keyPressEvent(self, e):

        if e.key() == Qt.Key_Escape:
            self.update()



    def setupMappingVisualisation(self):
        layout = self.gridLayout_3
        self.dictionary = {}
        i = 24
        j = 8
        for g in range(i):
            if g == 0 or g == 23:
                for t in range(j):
                    if t == 0 or t == 7:
                        self.dictionary["widget{0}".format(g)] = QWidget()
                        test = self.dictionary.get("widget{0}".format(g))
                        test.setMinimumHeight(20)
                        test.setMinimumWidth(20)
                        test.setMaximumHeight(60)
                        test.setMaximumWidth(60)
                        layout.addWidget(test, t, g)


                    else:
                        self.dictionary["widget{0}".format(g)] = QWidget()
                        test = self.dictionary.get("widget{0}".format(g))
                        test.setMinimumHeight(20)
                        test.setMinimumWidth(20)
                        test.setMaximumHeight(60)
                        test.setMaximumWidth(60)
                        test.setAutoFillBackground(True)
                        test.setStyleSheet("background-color: red")
                        layout.addWidget(test, t, g)
            else:
                for t in range(j):
                    self.dictionary["widget{0}".format(g)] = QWidget()
                    test = self.dictionary.get("widget{0}".format(g))
                    test.setMinimumHeight(20)
                    test.setMinimumWidth(20)
                    test.setMaximumHeight(60)
                    test.setMaximumWidth(60)
                    test.setAutoFillBackground(True)
                    test.setStyleSheet("background-color: green")
                    layout.addWidget(test, t, g)

        start_time = time.time()
        object1 = ReadFile.ReadFile()
        limit = 0
        self.d = defaultdict(list)
        for rows in object1.ws.rows:
            if limit <= 3:
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
    def update(self):
        FPS = 1
        lastFrameTime = time.time()
        start_time = time.time()
        test2 = self.dictionary["widget1"]
        test = self.d.get("dataSensor1")
        print("--- %s seconds ---" % (time.time() - start_time))
        for x in test:
            test2.setStyleSheet("background-color: rgb(244, 0, {0})".format(x * 170))
            while True:
                currentTime = time.time()
                sleepTime = 1. / FPS - (currentTime - lastFrameTime)
                if sleepTime > 0:
                    time.sleep(sleepTime)
                    x += x
                    print(x)
                    break;

                lastFrameTime = currentTime
        print("--- %s seconds ---" % (time.time() - start_time))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MyMainWindow()
    sys.exit(app.exec_())