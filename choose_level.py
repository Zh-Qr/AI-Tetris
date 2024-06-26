from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_level(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(270, 60, 221, 91))
        font = QtGui.QFont()
        font.setPointSize(22)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.back_last = QtWidgets.QPushButton(self.centralwidget)
        self.back_last.setGeometry(QtCore.QRect(320, 440, 93, 28))
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.back_last.setFont(font)
        self.back_last.setObjectName("back_last")
        self.easy_level = QtWidgets.QPushButton(self.centralwidget)
        self.easy_level.setGeometry(QtCore.QRect(100, 240, 131, 41))
        self.easy_level.setObjectName("easy_level")
        self.normal_level = QtWidgets.QPushButton(self.centralwidget)
        self.normal_level.setGeometry(QtCore.QRect(310, 240, 131, 41))
        self.normal_level.setObjectName("normal_level")
        self.hard_model = QtWidgets.QPushButton(self.centralwidget)
        self.hard_model.setGeometry(QtCore.QRect(520, 240, 131, 41))
        self.hard_model.setObjectName("hard_model")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "选择游戏难度"))
        self.back_last.setText(_translate("MainWindow", "退出"))
        self.easy_level.setText(_translate("MainWindow", "简单"))
        self.normal_level.setText(_translate("MainWindow", "一般"))
        self.hard_model.setText(_translate("MainWindow", "困难"))
