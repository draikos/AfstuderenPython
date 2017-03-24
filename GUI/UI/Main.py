from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QWidget
from GUI.Data import ReadFile
import time
from collections import defaultdict

class Ui_MainWindow(object):

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1200, 780)
        MainWindow.setMouseTracking(True)
        self.layout()
        self.groupboxSetup()
        self.bottomLayout()
        self.leftLayout()
        self.rightLayoutPositioner()
        self.leftLayoutPositioner()
        self.rightLayout()
        self.mainLayout()
        self.menubar()
        self.update()
        MainWindow.setCentralWidget(self.centralWidget)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    # -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    #  Layout setup

    def layout(self):
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setAutoFillBackground(False)
        self.centralWidget.setObjectName("centralWidget")

    def groupboxSetup(self):
        self.groupBox = QtWidgets.QGroupBox(self.centralWidget)
        self.groupBox.setObjectName("groupBox")
        self.groupBox_2 = QtWidgets.QGroupBox(self.centralWidget)
        self.groupBox_2.setObjectName("groupBox_2")
        self.groupBox_3 = QtWidgets.QGroupBox(self.centralWidget)
        self.groupBox_3.setObjectName("groupBox_3")


    def bottomLayout(self):
        self.bottomLayout = QtWidgets.QGridLayout()
        self.bottomLayout.setContentsMargins(11, 9, 11, 11)
        self.bottomLayout.setSpacing(6)
        self.bottomLayout.setObjectName("bottomLayout")
        self.bottomLayout.addWidget(self.groupBox_3, 0, 0, 1, 1)

    def leftLayout(self):
        self.leftLayout = QtWidgets.QGridLayout()
        self.leftLayout.setContentsMargins(11, 11, 11, 11)
        self.leftLayout.setSpacing(20)
        self.leftLayout.setObjectName("leftLayout")
        self.leftLayout.addWidget(self.groupBox, 0, 0, 2, 1)

    def rightLayoutPositioner(self):
        self.rightLayoutPositioner = QtWidgets.QGridLayout(self.groupBox_2)
        self.rightLayoutPositioner.setContentsMargins(100, 100, 100, 100)
        self.setupMappingVisualisation()

    def leftLayoutPositioner(self):
        self.leftLayoutPositioner = QtWidgets.QGridLayout(self.groupBox)
        self.leftLayoutPositioner.setContentsMargins(11, 11, 11, 11)
        self.leftLayoutPositioner.setSpacing(6)
        self.leftLayoutPositioner.setObjectName("label1")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setObjectName("label")
        self.leftLayoutPositioner.addWidget(self.label, 0, 0, 1, 1)

    def rightLayout(self):
        self.rightLayout = QtWidgets.QGridLayout()
        self.rightLayout.setContentsMargins(11, 11, 11, 11)
        self.rightLayout.setSpacing(6)
        self.rightLayout.setObjectName("layoutRight")
        self.rightLayout.addWidget(self.groupBox_2, 0, 0, 1, 1)

    def mainLayout(self):
        self.mainLayout = QtWidgets.QGridLayout(self.centralWidget)
        self.mainLayout.setContentsMargins(9, 11, 11, 0)
        self.mainLayout.setHorizontalSpacing(10)
        self.mainLayout.setVerticalSpacing(10)
        self.mainLayout.setObjectName("mainLayout")
        self.mainLayout.addLayout(self.leftLayout, 0, 0, 1, 1)
        self.mainLayout.addLayout(self.rightLayout, 0, 1, 1, 1)
        self.mainLayout.addLayout(self.bottomLayout, 1, 0, 1, 2)
        self.mainLayout.setColumnMinimumWidth(1, 2)
        self.mainLayout.setColumnStretch(0, 1)
        self.mainLayout.setColumnStretch(1, 2)
        self.mainLayout.setRowStretch(0, 3)
        self.mainLayout.setRowStretch(1, 1)

    def menubar(self):
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 750, 21))
        self.menuBar.setObjectName("menuBar")
        MainWindow.setMenuBar(self.menuBar)
        self.mainToolBar = QtWidgets.QToolBar(MainWindow)
        self.mainToolBar.setObjectName("mainToolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.mainToolBar)
        self.statusBar = QtWidgets.QStatusBar(MainWindow)
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)
        self.menuBar.addMenu('&files')

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.groupBox.setTitle(_translate("MainWindow", "GroupBox1"))
        self.label.setText(_translate("MainWindow", "dit is de eerste label"))
        self.groupBox_2.setTitle(_translate("MainWindow", "GroupBox2"))
        self.groupBox_3.setTitle(_translate("MainWindow", "GroupBox3"))

    # ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # visualisation setup
    def setupMappingVisualisation(self):
        layout = self.rightLayoutPositioner
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
            if limit <= 100:
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
        test = self.dictionary["widget1"]
        test.setStyleSheet("background-color: black")




if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

