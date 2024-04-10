"""
作者：仲启瑞
联系方式：
TEL:18305125976
QQ：1062127784
"""
import sys, random
from PyQt5.QtWidgets import QMainWindow, QFrame, QDesktopWidget, QApplication
import set_mainWindow
import tetris_game
import game_option
import choose_level

flag = 1
refresh = 0
app = None
tetris = None
options = None
level = None
speed = 500

current_game_num = 0

def choose_game_level():
    global level
    if level is not None:
        level.close()  # 关闭之前的窗口
    level = QMainWindow()
    ui_level = choose_level.Ui_level()
    ui_level.setupUi(level)
    level.show()
    ui_level.back_last.clicked.connect(quit_level_option)
    ui_level.easy_level.clicked.connect(choose_easy_level)
    ui_level.normal_level.clicked.connect(choose_normal_level)
    ui_level.hard_model.clicked.connect(choose_hard_level)

def choose_easy_level():
    get_level = tetris_game.Tetris()
    get_level.change_speed(500)

    quit_level_option()

def choose_normal_level():
    get_level = tetris_game.Tetris()
    get_level.change_speed(200)

    quit_level_option()

def choose_hard_level():
    get_level = tetris_game.Tetris()
    get_level.change_speed(0)

    quit_level_option()

def show_game_option():
    global options
    if options is not None:
        options.close()  # 关闭之前的窗口
    options = QMainWindow()  # 创建一个新的窗口对象
    ui_option = game_option.Ui_game_option()
    ui_option.setupUi(options)
    options.show()
    ui_option.back_last.clicked.connect(quit_game_option)
    ui_option.pushButton.clicked.connect(choose_AI)
    ui_option.pushButton_2.clicked.connect(choose_NOT_AI)


def choose_AI():
    global flag
    flag = 1
    tetris = tetris_game.Tetris()  # 创建 Tetris 实例
    tetris.changeAI()  # 调用 changeAI 方法
    print("choosing Ai Sucessfully")
    quit_game_option()

def choose_NOT_AI():
    global flag
    flag = 0
    tetris = tetris_game.Tetris()  # 创建 Tetris 实例
    tetris.closeAi()  # 调用 closeAi 方法
    print("close Ai Sucessfully")
    quit_game_option()


def quit_game_option():
    global options
    if options:
        options.close()

def quit_level_option():
    global level
    if level:
        level.close()


def start_the_game():
    global tetris
    if tetris is None:
        tetris = tetris_game.Tetris()
    global current_game_num
    current_game_num+=1
    update_game_num(current_game_num)
    tetris.show()
    tetris.start()

def update_game_num(new_game_num):
    new_game_num += tetris_game.Tetris.ret_auto_game_num(tetris)
    ui.now_num.setText("当前局数：" +str(new_game_num))
    update_full_score()

def update_full_score():
    ui.full_score.setText("总得分："+str(int(sum(tetris_game.full_score))))

def update_average_score():
    ui.label_2.setText("平均得分："+str("{:.2f}".format(float(sum(tetris_game.full_score))/(current_game_num+tetris_game.Tetris.ret_auto_game_num(tetris)))))

# def update_average_score():
#
#     ui.sc.setText("总得分："+str(tetris_game.full_score))

def quit_the_game():
    app.quit()

def refresh_score():
    update_full_score()
    update_average_score()
    global current_game_num
    update_game_num(current_game_num)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = QMainWindow()
    ui = set_mainWindow.Ui_Tetris()
    ui.setupUi(mainWindow)
    mainWindow.show()
    if current_game_num==0:
        ui.now_num.setText("当前局数：" + str(current_game_num))
        ui.full_score.setText("总得分："+str(sum(tetris_game.full_score)))

    ui.game_start.clicked.connect(start_the_game)
    ui.exit_prog.clicked.connect(quit_the_game)
    ui.Option_of_way.clicked.connect(show_game_option)
    ui.Game_level.clicked.connect(choose_game_level)
    ui.check_score.clicked.connect(refresh_score)

    sys.exit(app.exec_())