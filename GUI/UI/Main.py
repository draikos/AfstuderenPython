# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.8.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPen, QColor, QPainter, QColor, QBrush
from PyQt5.QtWidgets import QWidget,QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import QRect

class Ui_MainWindow(object):

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1200, 780)
        MainWindow.setMouseTracking(True)
        self.layout()
        self.groupboxSetup()
        self.bottomLayout()
        self.leftLayout()
        self.label2()
        self.label1()
        self.layoutRight()
        self.mainLayout()
        self.menubar()

        MainWindow.setCentralWidget(self.centralWidget)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)


    def layout(self):
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_5 = QtWidgets.QGridLayout()
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
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setContentsMargins(11, 9, 11, 11)
        self.gridLayout.setSpacing(6)
        self.gridLayout.setObjectName("bottomLayout")
        self.gridLayout.addWidget(self.groupBox_3, 0, 0, 1, 1)

    def leftLayout(self):
        self.gridLayout_2.setContentsMargins(11, 11, 11, 11)
        self.gridLayout_2.setSpacing(20)
        self.gridLayout_2.setObjectName("leftLayout")
        self.gridLayout_2.addWidget(self.groupBox, 0, 0, 2, 1)

    def label2(self):
        self.gridLayout_3 = QtWidgets.QGridLayout(self.groupBox_2)
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_3.totalHeightForWidth(200)
        self.setupMappingVisualisation()





    def setupMappingVisualisation(self):
        v = 0
        layout = self.gridLayout_3
        indexSensors = 192
        listV = []
        listT = []
        for t in range(indexSensors):
            sensor = "sensor"+str(t)
            listV.append(sensor)

        i = 24
        j = 8
        for g in range(i):
            if g == 0 or g == 23:
                for t in range(j):
                    if t == 0 or t == 7:
                        listV[v] = QWidget()
                        test = listV[v]
                        v += 1
                        listT.append(test)
                        test.setFixedSize(20, 20)
                        layout.addWidget(test, t, g)

                    else:
                        listV[v] = QWidget()
                        test = listV[v]
                        v += 1
                        listT.append(test)
                        test.setAutoFillBackground(True)
                        test.setFixedSize(20, 20)
                        test.setStyleSheet("background-color: red")
                        layout.addWidget(test, t, g)
            else:
                for t in range(j):
                    listV[v] = QWidget()
                    test = listV[v]
                    v += 1
                    listT.append(test)
                    test.setAutoFillBackground(True)
                    test.setFixedSize(20,20)
                    test.setStyleSheet("background-color: green")
                    layout.addWidget(test, t, g)

    def label1(self):
        self.gridLayout_4 = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout_4.setContentsMargins(11, 11, 11, 11)
        self.gridLayout_4.setSpacing(6)
        self.gridLayout_4.setObjectName("label1")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setObjectName("label")
        self.gridLayout_4.addWidget(self.label, 0, 0, 1, 1)


    def layoutRight(self):
        self.gridLayout_5.setContentsMargins(11, 11, 11, 11)
        self.gridLayout_5.setSpacing(6)
        self.gridLayout_5.setObjectName("layoutRight")
        self.gridLayout_5.addWidget(self.groupBox_2, 0, 0, 1, 1)

    def mainLayout(self):
        self.gridLayout_6 = QtWidgets.QGridLayout(self.centralWidget)
        self.gridLayout_6.setContentsMargins(9, 11, 11, 0)
        self.gridLayout_6.setHorizontalSpacing(15)
        self.gridLayout_6.setVerticalSpacing(10)
        self.gridLayout_6.setObjectName("mainLayout")
        self.gridLayout_6.addLayout(self.gridLayout_2, 0, 0, 1, 1)
        self.gridLayout_6.addLayout(self.gridLayout_5, 0, 1, 1, 1)
        self.gridLayout_6.addLayout(self.gridLayout, 1, 0, 1, 2)
        self.gridLayout_6.setColumnMinimumWidth(1, 2)
        self.gridLayout_6.setColumnStretch(0, 1)
        self.gridLayout_6.setColumnStretch(1, 2)
        self.gridLayout_6.setRowStretch(0, 3)
        self.gridLayout_6.setRowStretch(1, 1)

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
        self.groupBox.setTitle(_translate("MainWindow", "GroupBox"))
        self.label.setText(_translate("MainWindow", "dit is de eerste label"))
        self.groupBox_2.setTitle(_translate("MainWindow", "GroupBox"))
        self.groupBox_3.setTitle(_translate("MainWindow", "GroupBox"))




if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

