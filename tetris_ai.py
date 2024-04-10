
# 导入所需的模块和库
from tetris_model import BOARD_DATA, Shape
import math
from datetime import datetime
import numpy as np

x1,x2,x3,x4,x5,x6,x7,x8,x9,x10=1.8,1.1,1.0,0.5,0,0.01,0.2,0.3,1.5,0.02
w = np.array([x1,x2,x3,x4,x5,x6,x7,x8,x9,x10])

# 创建俄罗斯方块的人工智能类
class TetrisAI(object):
    # @property
    # 下一个形状的计算
    def nextMove(self):

        currentDirection = BOARD_DATA.currentDirection  # 获取当前形状的方向
        currentY = BOARD_DATA.currentY  # 获取当前形状的纵向位置
        _, _, minY, _ = BOARD_DATA.nextShape.getBoundingOffsets(0)  # 获取下一个形状的边界偏移量
        nextY = -minY  # 计算下一个形状的纵向位置
        all_board = np.array(BOARD_DATA.getData()).reshape((BOARD_DATA.height, BOARD_DATA.width))
        board_height = self.height_count(np.copy(all_board))

        strategy = None  # 定义策略变量，用于保存最优的放置策略
        if BOARD_DATA.currentShape.shape in (Shape.shapeI, Shape.shapeZ, Shape.shapeS):
            d0Range = (0, 1)  # 若当前形状为I、Z或S型，则有两个可能的方向
        elif BOARD_DATA.currentShape.shape == Shape.shapeO:
            d0Range = (0,)  # 若当前形状为O型，则只有一个可能的方向
        else:
            d0Range = (0, 1, 2, 3)  # 其他形状有四个可能的方向

        if BOARD_DATA.nextShape.shape in (Shape.shapeI, Shape.shapeZ, Shape.shapeS):
            d1Range = (0, 1)  # 若下一个形状为I、Z或S型，则有两个可能的方向
        elif BOARD_DATA.nextShape.shape == Shape.shapeO:
            d1Range = (0,)  # 若下一个形状为O型，则只有一个可能的方向
        else:
            d1Range = (0, 1, 2, 3)  # 其他形状有四个可能的方

        score_test = -1000
        att = -1000
        strategy3 = (0, 0, -1000)
        prediction_shape = Shape(0)
        check = 1
        for d0 in d0Range:
            minX, maxX, _, _ = BOARD_DATA.currentShape.getBoundingOffsets(d0)  # 获取当前形状在x轴上的最小和最大边界
            for x0 in range(-minX, BOARD_DATA.width - maxX):  # 遍历所有可能的x轴位置
                board = self.calcStep1Board(d0, x0, np.copy(all_board),BOARD_DATA.currentShape)  # 计算当前形状放置后的游戏板面状态)
                scorefirst = self.score_count(board)
                if (score_test - scorefirst < 1):
                    for d1 in d1Range:
                        minX, maxX, _, _ = BOARD_DATA.nextShape.getBoundingOffsets(d1)  # 获取下一个形状在x轴上的最小和最大边界
                        dropDist = self.calcNextDropDist(board, d1, range(-minX, BOARD_DATA.width - maxX),
                                                         BOARD_DATA.nextShape)  # 计算下一个形状的下落距离
                        for x1 in range(-minX, BOARD_DATA.width - maxX):  # 遍历所有可能的x轴位置
                            score, board2 = self.calculateScore(np.copy(board), BOARD_DATA.nextShape, d1, x1,
                                                                dropDist)  # 计算该放置组合的得分
                            if (att - score < 1):  # np.mean(list(dropDist.values()))>3):
                                score3 = 0
                                for d2 in (range(1, 8)):
                                    score4 = -1000
                                    prediction_shape = Shape(d2)
                                    if d2 == 1 or 6 or 7:
                                        d2range = (0, 1)
                                    elif d2 == 5:
                                        d2range = (0,)
                                    else:
                                        d2range = (0, 1, 2, 3)
                                    for d3 in d2range:
                                        minX1, maxX1, _, _ = prediction_shape.getBoundingOffsets(d3)
                                        dropDist2 = self.calcNextDropDist(board2, d3,
                                                                          range(-minX1, BOARD_DATA.width - maxX1),
                                                                          prediction_shape)
                                        for x2 in range(-minX1, BOARD_DATA.width - maxX1):
                                            score2, _ = self.calculateScore(np.copy(board2), prediction_shape, d3, x2,
                                                                            dropDist2)
                                            if (score2 > score4):
                                                score4 = score2
                                    score3 = score4 + score3
                                if not strategy3 or strategy3[2] < score3:
                                    strategy3 = (d0, x0, score3)
                                    att = score
                                    score_test = scorefirst
                            if not strategy or strategy[
                                2] < score:  # 如果当前得分大于之前记录的最优得分，则更新最,优策略d1, x1, dropDist, nextShape,d1, x1, dropDist, BOARD_DATA.nextShape,
                                strategy = (d0, x0, score)
        # if(strategy3[1]!=strategy[1] or strategy[0]!= strategy3[0]):
        #      # print(strategy3)
        #      # print(strategy)
        if check:
            return strategy3  # 返回得分最高的放置策略
        else:
            return strategy

    # 计算下一个形状在当前位置的下落距离
    def calcNextDropDist(self, data, d0, xRange, shape):
        res = {}  # 用于存储不同x轴位置对应的下落距离
        for x0 in xRange:
            if x0 not in res:
                res[x0] = BOARD_DATA.height - 1  # 初始化下落距离为游戏板面的高度减1
            for x, y in shape.getCoords(d0, x0, 0):
                yy = 0
                while yy + y < BOARD_DATA.height and (yy + y < 0 or data[(y + yy), x] == Shape.shapeNone):
                    yy += 1  # 逐步向下探测下落距离，直到遇到障碍物或达到游戏板面底部
                yy -= 1
                if yy < res[x0]:
                    res[x0] = yy  # 记录每个x轴位置对应的最小下落距离
        return res

    # 计算当前形状在给定方向和x轴位置下，下落一步后的游戏板面状态
    def calcStep1Board(self, d0, x0, board, shape): # 复制游戏板面数据
        self.dropDown(board, shape, d0, x0)  # 将当前形状放置到指定位置
        return board  # 返回放置后的游戏板面状态

    # 计算形状在给定位置的下落距离，并更新游戏板面状态
    def dropDown(self, data, shape, direction, x0):
        dy = BOARD_DATA.height - 1  # 初始化下落距离为游戏板面的高度减1
        for x, y in shape.getCoords(direction, x0, 0):  # 遍历形状的每个方块
            yy = 0
            while yy + y < BOARD_DATA.height and (yy + y < 0 or data[(y + yy), x] == Shape.shapeNone):
                yy += 1  # 逐步向下探测下落距离，直到遇到障碍物或达到游戏板面底部
            yy -= 1
            if yy < dy:
                dy = yy  # 记录形状在该位置的最小下落距离
        self.dropDownByDist(data, shape, direction, x0, dy)  # 将形状按最小下落距离放置到游戏板面上

    # 根据下落距离将形状放置到游戏板面上
    def dropDownByDist(self, data, shape, direction, x0, dist):
        for x, y in shape.getCoords(direction, x0, 0):  # 遍历形状的每个方块
            data[y + dist, x] = shape.shape  # 在对应位置放置形状方块

    # 计算放置组合的得分
    def calculateScore(self, step1Board, pre, d2, x2, dropDist2):
        self.dropDownByDist(step1Board, pre, d2, x2, dropDist2[x2])
        score = self.score_count(step1Board)
        return score, step1Board  # 返回放置组合的得分

    def height_count(self, board):
        width = BOARD_DATA.width  # 获取游戏板面的宽度
        height = BOARD_DATA.height  # 获取游戏板面的高度
        height_score = [0] * width
        for x in range(0, width):
             for y in range(0, height):
                 if board[height-y-1, x] != 0:
                      height_score[x] = y+1
        return height_score

    def score_count(self, borad):
        width = BOARD_DATA.width  # 获取游戏板面的宽度
        height = BOARD_DATA.height  # 获取游戏板面的高度
        fullLines, nearFullLines = 0, 0
        roofY = [0] * width
        holeCandidates = [0] * width
        holeConfirm = [0] * width
        vHoles, vBlocks = 0, 0
        for y in range(height - 1, -1, -1):
            hasHole = False
            hasBlock = False
            for x in range(width):
                if borad[y, x] == Shape.shapeNone:  # 若游戏板面上存在洞
                    hasHole = True
                    holeCandidates[x] += 1  # 记录每个x轴位置可能的洞数
                else:
                    hasBlock = True
                    roofY[x] = height - y  # 记录每个x轴位置的方块堆叠高度
                    if holeCandidates[x] > 0:
                        holeConfirm[x] += holeCandidates[x]
                        holeCandidates[x] = 0
                    if holeConfirm[x] > 0:
                        vBlocks += 1  # 统计垂直方向上的方块堆叠
            if not hasBlock:
                break
            if not hasHole and hasBlock:
                fullLines += 1  # 统计填满的行数
        vHoles = sum([x ** .7 for x in holeConfirm])  # 根据洞的位置分布计算垂直方向的洞数
        maxHeight = max(roofY) - fullLines  # 计算最大堆叠高度
        # print(datetime.now() - t1)

        roofDy = [roofY[i] - roofY[i + 1] for i in range(len(roofY) - 1)]  # 计算相邻列之间的高度差

        if len(roofY) <= 0:
            stdY = 0
        else:
            stdY = math.sqrt(sum([y ** 2 for y in roofY]) / len(roofY) - (sum(roofY) / len(roofY)) ** 2)  # 计算堆叠高度的标准差
        if len(roofDy) <= 0:
            stdDY = 0
        else:
            stdDY = math.sqrt(
                sum([y ** 2 for y in roofDy]) / len(roofDy) - (sum(roofDy) / len(roofDy)) ** 2)  # 计算堆叠高度差的标准差


        absDy = sum([abs(x) for x in roofDy])  # 计算相邻列高度差的绝对值之和
        maxDy = max(roofY) - min(roofY)  # 计算最大和最小堆叠高度之间的差
        # print(datetime.now() - t1)
        if roofDy[0] < -2 and roofDy[8] > 2:
            worse = 100
        else:
            worse = 0

        score = fullLines * w[0] - vHoles ** w[1] * w[2] - vBlocks * w[3] - stdY * w[4] - stdDY * w[5] - absDy * w[6] - maxDy * w[7] - maxHeight ** w[8] * w[9] - worse  # 综合考虑多个因素计算得分
        return score  # 返回放置组合的得分



# 创建人工智能对象并将其导出为TETRIS_AI
TETRIS_AI = TetrisAI()
