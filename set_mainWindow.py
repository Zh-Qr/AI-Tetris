# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'set_mainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Tetris(object):
    def setupUi(self, Tetris):
        Tetris.setObjectName("Tetris")
        Tetris.resize(868, 670)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Tetris.sizePolicy().hasHeightForWidth())
        Tetris.setSizePolicy(sizePolicy)
        self.centralwidget = QtWidgets.QWidget(Tetris)
        self.centralwidget.setObjectName("centralwidget")
        self.now_num = QtWidgets.QLabel(self.centralwidget)
        self.now_num.setGeometry(QtCore.QRect(220, 460, 181, 19))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.now_num.setFont(font)
        self.now_num.setObjectName("now_num")
        self.full_score = QtWidgets.QLabel(self.centralwidget)
        self.full_score.setGeometry(QtCore.QRect(400, 460, 151, 19))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.full_score.setFont(font)
        self.full_score.setObjectName("full_score")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(570, 460, 261, 19))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.layoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget.setGeometry(QtCore.QRect(220, 0, 431, 441))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.Game_level = QtWidgets.QPushButton(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(50)
        sizePolicy.setHeightForWidth(self.Game_level.sizePolicy().hasHeightForWidth())
        self.Game_level.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.Game_level.setFont(font)
        self.Game_level.setObjectName("Game_level")
        self.verticalLayout.addWidget(self.Game_level)
        self.Option_of_way = QtWidgets.QPushButton(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.Option_of_way.setFont(font)
        self.Option_of_way.setObjectName("Option_of_way")
        self.verticalLayout.addWidget(self.Option_of_way)
        self.game_start = QtWidgets.QPushButton(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.game_start.setFont(font)
        self.game_start.setObjectName("game_start")
        self.verticalLayout.addWidget(self.game_start)
        self.exit_prog = QtWidgets.QPushButton(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.exit_prog.setFont(font)
        self.exit_prog.setObjectName("exit_prog")
        self.verticalLayout.addWidget(self.exit_prog)
        self.check_score = QtWidgets.QPushButton(self.centralwidget)
        self.check_score.setGeometry(QtCore.QRect(380, 510, 101, 31))
        font = QtGui.QFont()
        font.setPointSize(13)
        font.setBold(True)
        font.setWeight(75)
        self.check_score.setFont(font)
        self.check_score.setObjectName("check_score")
        Tetris.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(Tetris)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 868, 23))
        self.menubar.setObjectName("menubar")
        Tetris.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(Tetris)
        self.statusbar.setObjectName("statusbar")
        Tetris.setStatusBar(self.statusbar)

        self.retranslateUi(Tetris)
        QtCore.QMetaObject.connectSlotsByName(Tetris)

    def retranslateUi(self, Tetris):
        _translate = QtCore.QCoreApplication.translate
        Tetris.setWindowTitle(_translate("Tetris", "菜单页"))
        self.now_num.setText(_translate("Tetris", "当前局数："))
        self.full_score.setText(_translate("Tetris", "总得分："))
        self.label_2.setText(_translate("Tetris", "平局得分："))
        self.Game_level.setText(_translate("Tetris", "选择难度"))
        self.Option_of_way.setText(_translate("Tetris", "游玩方式"))
        self.game_start.setText(_translate("Tetris", "开始游戏"))
        self.exit_prog.setText(_translate("Tetris", "退出游戏"))
        self.check_score.setText(_translate("Tetris", "查看分数"))
