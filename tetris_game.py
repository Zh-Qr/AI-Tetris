
# 导入所需的模块和库
import sys, random

import numpy as np
from PyQt5.QtWidgets import QMainWindow, QFrame, QDesktopWidget, QApplication, QHBoxLayout,QVBoxLayout,QPushButton
from PyQt5.QtCore import Qt, QBasicTimer, pyqtSignal
from PyQt5.QtGui import QPainter, QColor

from tetris_model import BOARD_DATA, Shape  # 导入自定义的游戏模型和形状
from tetris_ai import TETRIS_AI  # 导入俄罗斯方块的人工智能模块
from main import flag,speed,update_full_score,current_game_num


full_score = []
auto_game_num=0
# current_game_num = 0

# 创建主游戏窗口类
class Tetris(QMainWindow):
    def __init__(self):
        super().__init__()
        self.isStarted = False  # 游戏是否已开始
        self.isPaused = False  # 游戏是否已暂停
        self.nextMove = None  # 下一个移动
        self.lastShape = Shape.shapeNone  # 上一个形状
        self.initialSpeed = speed  # 设置初始速度


        self.initUI()  # 初始化游戏界面
        self.timer = QBasicTimer()  # 创建游戏定时器
        self.setFocusPolicy(Qt.StrongFocus)

    #设置界面属性
    def initUI(self):
        self.gridSize = 22 # 方格大小
        # self.speed = 0  # 游戏速度

        self.timer = QBasicTimer()  # 游戏定时器
        self.setFocusPolicy(Qt.StrongFocus) #强焦点策略，优先接收键盘返回的数值，以保证游戏的交互性

        hLayout = QHBoxLayout()#水平布局管理器
        self.tboard = Board(self, self.gridSize)  # 创建游戏棋盘，并将其代入窗口中
        hLayout.addWidget(self.tboard)# 游戏棋盘部件 tboard 添加到水平布局管理器 hLayout 中。z

        self.sidePanel = SidePanel(self, self.gridSize)  # 游戏侧边栏
        hLayout.addWidget(self.sidePanel)# 游戏侧边栏部件 sidePanel 添加到水平布局管理器 hLayout 中。

        self.statusbar = self.statusBar()  # 游戏状态栏，用于在底部显示得分
        self.tboard.msg2Statusbar[str].connect(self.statusbar.showMessage)

        # 创建一个按钮，用于重新开始游戏
        restartButton = QPushButton('重新开始', self)
        restartButton.clicked.connect(self.resetGame)
        hLayout.addWidget(restartButton)
        restartButton.setGeometry(235, 300, 80, 30)
        self.start()  # 开始游戏

        self.setWindowTitle('Magic Tetris')  # 设置窗口标题
        self.show()


        self.setFixedSize(self.tboard.width() + self.sidePanel.width(),
                          self.sidePanel.height() + self.statusbar.height())#固定游戏窗口大小

    # 创建一个新的方法来重新启动游戏
    def restartGame(self):
        # 关闭当前游戏窗

        self.close()

    # 修改resetGame方法，调用restartGame方法来重新启动游戏
    def resetGame(self):

        self.isStarted = False
        self.isPaused = False
        self.nextMove = None
        self.lastShape = Shape.shapeNone
        self.tboard.score = 0
        BOARD_DATA.clear()
        self.tboard.msg2Statusbar.emit(str(self.tboard.score))
        BOARD_DATA.createNewPiece()
        # 调用restartGame方法以重新启动游戏
        self.restartGame()


    def start(self):
        if self.isPaused:
            return

        self.isStarted = True
        global current_game_num
        current_game_num+=1
        self.tboard.score = 0#清空分数
        BOARD_DATA.clear()#清空棋盘

        self.tboard.msg2Statusbar.emit(str(self.tboard.score))#通过发出 msg2Statusbar 信号将当前分数显示在状态栏上

        BOARD_DATA.createNewPiece()#创建新的俄罗斯方块（游戏的形状）。游戏通常会以一个随机或预定义的形状开始。
        self.timer.start(speed, self)#这行代码启动游戏的计时器，使游戏开始运行。计时器会以指定的速度（self.speed）周期性地触发 timerEvent 方法，从而推进游戏的运行。

    def pause(self):
        # 若没有开始则返回
        if not self.isStarted:
            return
        # 反转暂停命令：以暂停则开始，未暂停则暂停
        self.isPaused = not self.isPaused#切换游戏的暂停状态

        if self.isPaused:
            self.timer.stop()#停止游戏的计时器，这将导致游戏停止进行下一步操作
            self.tboard.msg2Statusbar.emit("paused")#将 "paused" 信息发送到状态栏，以通知玩家游戏已经暂停
        else:
            self.timer.start(speed, self)#重新启动游戏的计时器，以继续游戏运行

        self.updateWindow()#更新游戏窗口的显示，以反映游戏状态的变化。

    # 更新游戏窗口
    def updateWindow(self):
        self.tboard.updateData()#更新游戏棋盘的数据，包括当前俄罗斯方块的位置和游戏板上的方块情况。
        if not self.isStarted:
            self.tboard.end_of_the_game()
        self.sidePanel.updateData()#调用游戏侧边栏对象，更新侧边栏的数据，通常包括显示下一个俄罗斯方块的形状。
        self.update()#用于触发游戏窗口的重新绘制。这将导致 paintEvent 方法被调用，以根据最新的游戏数据重新绘制游戏窗口。
    def changeAI(self):
        global flag
        flag = 1;

    def closeAi(self):
        global flag
        flag = 0;

    def change_speed(self,new_speed):
        global speed
        speed = new_speed
        self.timer.start(speed, self)  # 重新启动计时器以应用新速度
    def timerEvent(self, event):
        if event.timerId() == self.timer.timerId():#触发由人工智能输入
            if flag and TETRIS_AI and not self.nextMove:#是否启用了俄罗斯方块的人工智能（TETRIS_AI），以及是否已经计算出下一个移动（self.nextMove）。如果尚未计算下一个移动，它会尝试获取下一个移动。
                self.nextMove = TETRIS_AI.nextMove()
            if self.nextMove:
                k = 0#用于计数旋转或移动的尝试次数
                while BOARD_DATA.currentDirection != self.nextMove[0] and k < 4:#用于旋转当前俄罗斯方块以使其方向匹配下一个移动的方向。它会一直循环，直到方向匹配或尝试次数达到4次为止。nextMove第一个数值是旋转角度
                    BOARD_DATA.rotateRight()#将当前俄罗斯方块顺时针旋转
                    k += 1
                k = 0
                while BOARD_DATA.currentX != self.nextMove[1] and k < 5:#nextMove第二个数值是旋转角度
                    if BOARD_DATA.currentX > self.nextMove[1]:
                        BOARD_DATA.moveLeft()
                    elif BOARD_DATA.currentX < self.nextMove[1]:
                        BOARD_DATA.moveRight()
                    k += 1
            lines = BOARD_DATA.moveDown()#向下移动
            self.tboard.score += lines

            if BOARD_DATA.isGameOver():
                self.gameOver()

            if self.lastShape != BOARD_DATA.currentShape:#当前俄罗斯方块的形状是否与上一个俄罗斯方块的形状不同
                self.nextMove = None
                self.lastShape = BOARD_DATA.currentShape#更新
            self.updateWindow()
        else:
            super(Tetris, self).timerEvent(event)#重执行方法

    def gameOver(self):
        # 游戏结束时的处理
        global full_score,auto_num,auto_game_num
        full_score=np.append(full_score,self.tboard.score)
        self.tboard.msg2Statusbar.emit("Game Over. Your Score: " + str(self.tboard.score))
        self.tboard.end_of_the_game()
        self.isStarted = False
        self.isPaused = False
        self.timer.stop()

    #返回自动开始的局数
    def ret_auto_game_num(self):
        global auto_game_num
        return auto_game_num

    # 处理键盘事件
    def keyPressEvent(self, event):
        if not self.isStarted or BOARD_DATA.currentShape == Shape.shapeNone:#没开始或者没形状
            super(Tetris, self).keyPressEvent(event)#重调用
            return

        key = event.key()#读取

        if key == Qt.Key_P:
            self.pause()
            return

        if self.isPaused:
            return
        elif key == Qt.Key_Left:
            BOARD_DATA.moveLeft()
        elif key == Qt.Key_Right:
            BOARD_DATA.moveRight()
        elif key == Qt.Key_Up:
            BOARD_DATA.rotateLeft()
        elif key == Qt.Key_Down:
            self.tboard.score += BOARD_DATA.dropDown()
        else:
            super(Tetris, self).keyPressEvent(event)#重调用

        self.updateWindow()


# 绘制游戏方格
"""
painter: 一个 QPainter 对象，用于绘制游戏方格。
x 和 y: 方格的左上角坐标。
val: 方格的值，它表示方格的颜色和状态。
s: 方格的大小，通常是一个正方形。
"""
def drawSquare(painter, x, y, val, s):
    colorTable = [0x000000, 0xCC6666, 0x66CC66, 0x6666CC,
                  0xCCCC66, 0xCC66CC, 0x66CCCC, 0xDAAA00]

    if val == 0:
        return

    color = QColor(colorTable[val])#选定颜色
    painter.fillRect(x + 1, y + 1, s - 2, s - 2, color)#填充方格内部，其中 (x + 1, y + 1) 是内部的起始坐标，(s - 2, s - 2) 是内部的宽度和高度。绘制有缝隙

    painter.setPen(color.lighter())#设置画笔颜色，绘制方格的边框,lighter()或者darker()
    painter.drawLine(x, y + s - 1, x, y)#用于绘制方格的边框线段，形成边框。上
    painter.drawLine(x, y, x + s - 1, y)#用于绘制方格的边框线段，形成边框。左

    painter.setPen(color.darker())
    painter.drawLine(x + 1, y + s - 1, x + s - 1, y + s - 1)#右侧
    painter.drawLine(x + s - 1, y + s - 1, x + s - 1, y + 1)#下侧


# 游戏侧边栏类，其中包括下一个方块的预览
class SidePanel(QFrame):
    def __init__(self, parent, gridSize):#parent 是该侧边栏的父部件。gridSize 是游戏方格的大小。
        super().__init__(parent)#初始化父部件
        self.setFixedSize(gridSize * 5, gridSize * BOARD_DATA.height)
        self.move(gridSize * BOARD_DATA.width, 0)#函数将侧边栏的位置移到游戏板的右侧。
        self.gridSize = gridSize


    def updateData(self):#状态更新时被调用
        self.update()
    #下一个图形画面
    def paintEvent(self, event):
        painter = QPainter(self)#创建一个 QPainter 对象 painter，用于绘制内容。
        minX, maxX, minY, maxY = BOARD_DATA.nextShape.getBoundingOffsets(0)

        dy = 3 * self.gridSize#纵向高度
        dx = (self.width() - (maxX - minX) * self.gridSize) / 2#横向距离

        val = BOARD_DATA.nextShape.shape
        for x, y in BOARD_DATA.nextShape.getCoords(0, 0, -minY):#(0, -minY) 用于对齐方块的顶部
            drawSquare(painter, x * self.gridSize + dx, y * self.gridSize + dy, val, self.gridSize)


# 游戏棋盘类
class Board(QFrame):
    msg2Statusbar = pyqtSignal(str)
    speed = 0

    def __init__(self, parent, gridSize):
        super().__init__(parent)
        self.setFixedSize(gridSize * BOARD_DATA.width, gridSize * BOARD_DATA.height)
        self.gridSize = gridSize
        self.initBoard()

    def initBoard(self):
        self.score = 0
        BOARD_DATA.clear()

    def paintEvent(self, event):
        painter = QPainter(self)

        # 绘制游戏背景
        for x in range(BOARD_DATA.width):
            for y in range(BOARD_DATA.height):
                val = BOARD_DATA.getValue(x, y)
                drawSquare(painter, x * self.gridSize, y * self.gridSize, val, self.gridSize)

        # 绘制当前形状
        for x, y in BOARD_DATA.getCurrentShapeCoord():
            val = BOARD_DATA.currentShape.shape
            drawSquare(painter, x * self.gridSize, y * self.gridSize, val, self.gridSize)

        # 绘制边框，整个右侧的边框
        painter.setPen(QColor(0x777777))
        painter.drawLine(self.width() - 1, 0, self.width() - 1, self.height())
        painter.setPen(QColor(0xCCCCCC))
        painter.drawLine(self.width(), 0, self.width(), self.height())

    def updateData(self):#是将分数（self.score）发送到状态栏并触发状态栏的更新以显示分数
        self.msg2Statusbar.emit("您现在得分是： "+str(self.score))
        self.update()

    def end_of_the_game(self):
        self.msg2Statusbar.emit("游戏结束，您的最终得分是： "+str(self.score))
        self.update()


if __name__ == '__main__':
    app = QApplication([])#用于管理和控制Qt应用程序的生命周
    tetris = Tetris()
    sys.exit(app.exec_())
