

import random
import time

# 定义俄罗斯方块的形状，标记不同形状
class Shape(object):
    shapeNone = 0#没有方块
    shapeI = 1
    shapeL = 2
    shapeJ = 3
    shapeT = 4
    shapeO = 5
    shapeS = 6
    shapeZ = 7

    # 每种形状的坐标偏移，用于旋转和移动俄罗斯方块
    shapeCoord = (
        ((0, 0), (0, 0), (0, 0), (0, 0)),
        ((0, -1), (0, 0), (0, 1), (0, 2)),
        ((0, -1), (0, 0), (0, 1), (1, 1)),
        ((0, -1), (0, 0), (0, 1), (-1, 1)),
        ((0, -1), (0, 0), (0, 1), (1, 0)),
        ((0, 0), (0, -1), (1, 0), (1, -1)),
        ((0, 0), (0, -1), (-1, 0), (1, -1)),
        ((0, 0), (0, -1), (1, 0), (-1, -1))
    )
    #类的构造函数，它接受一个可选参数 shape，默认值为0。这个参数表示俄罗斯方块的形状，用于创建 Shape 类的实例。例如，shape=1 表示创建一个 shapeI 形状的俄罗斯方块。
    def __init__(self, shape=0):
        self.shape = shape
    #获取给定方向的旋转后的俄罗斯方块的坐标偏移，direction 参数表示方块的旋转方向，可以是0、1、2、3，分别代表0度、90度、180度和270度的旋转。
    def getRotatedOffsets(self, direction):
        tmpCoords = Shape.shapeCoord[self.shape]#tmpCoords 获取了当前形状（self.shape）的原始坐标偏移信息。
        if direction == 0 or self.shape == Shape.shapeO:#那么直接返回原始坐标偏移，不进行任何旋转。
            return ((x, y) for x, y in tmpCoords)

        if direction == 1:#果方块需要进行90度的旋转（direction == 1），则返回原始坐标的逆时针旋转
            return ((-y, x) for x, y in tmpCoords)

        if direction == 2:
            if self.shape in (Shape.shapeI, Shape.shapeZ, Shape.shapeS):#根据方块的形状来决定返回原始坐标或其镜像坐标。
                return ((x, y) for x, y in tmpCoords)
            else:
                return ((-x, -y) for x, y in tmpCoords)

        if direction == 3:
            if self.shape in (Shape.shapeI, Shape.shapeZ, Shape.shapeS):
                return ((-y, x) for x, y in tmpCoords)
            else:
                return ((y, -x) for x, y in tmpCoords)
    #旋转后新坐标结合当前坐标（受旋转影响）
    def getCoords(self, direction, x, y):
        return ((x + xx, y + yy) for xx, yy in self.getRotatedOffsets(direction))

    #获取旋转后的俄罗斯方块的边界坐标，以便进行碰撞检测和边界检测。
    def getBoundingOffsets(self, direction):
        tmpCoords = self.getRotatedOffsets(direction)#获得旋转后的坐标偏移。
        minX, maxX, minY, maxY = 0, 0, 0, 0
        for x, y in tmpCoords:
            if minX > x:
                minX = x
            if maxX < x:
                maxX = x
            if minY > y:
                minY = y
            if maxY < y:
                maxY = y
        return (minX, maxX, minY, maxY)#返回一个包含这些边界坐标的元组 (minX, maxX, minY, maxY)

# 定义游戏板的数据
class BoardData(object):
    #表示游戏板的宽度和高度
    width = 10
    height = 10

    def __init__(self):
        #一个列表，用于表示游戏板上每个位置的状态。初始时，所有位置都被设置为 0，表示空白。一维数组
        self.backBoard = [0] * BoardData.width * BoardData.height

        #表示当前俄罗斯方块的位置，初始值为 -1，表示没有当前方块。
        self.currentX = -1
        self.currentY = -1
        #表示当前俄罗斯方块的方向（旋转状态），初始值为 0。
        self.currentDirection = 0
        #表示当前俄罗斯方块的形状，初始值是一个空白方块
        self.currentShape = Shape()
        #表示下一个俄罗斯方块的形状，初始值是一个随机生成的俄罗斯方块（从 1 到 7 的随机整数）。
        self.nextShape = Shape(random.randint(1, 7))
        #用于跟踪每种形状的方块在游戏中的出现次数
        self.shapeStat = [0] * 8

    #返回游戏板的数据，即 backBoard 的副本，以防止直接修改原始数据。
    def getData(self):
        return self.backBoard[:]

    #这个方法用于获取指定位置 (x, y) 处的值，也就是游戏板上对应位置的状态。
    def getValue(self, x, y):
        return self.backBoard[x + y * BoardData.width]
    #返回当前俄罗斯方块的所有坐标，考虑了当前的位置和方向。
    def getCurrentShapeCoord(self):
        return self.currentShape.getCoords(self.currentDirection, self.currentX, self.currentY)

    #创建新的俄罗斯方块
    def createNewPiece(self):
        # 创建新的方块
        minX, maxX, minY, maxY = self.nextShape.getBoundingOffsets(0)#新生成一个shape类，获取边界
        result = False
        if self.tryMoveCurrent(0, 5, -minY):
            self.currentX = 5
            self.currentY = -minY
            self.currentDirection = 0
            self.currentShape = self.nextShape
            self.nextShape = Shape(random.randint(1, 7))
            result = True
        else:
            self.currentShape = Shape()
            self.currentX = -1
            self.currentY = -1
            self.currentDirection = 0
            result = False
        self.shapeStat[self.currentShape.shape] += 1
        return result

    #检查当前方块是否可以在指定的方向 direction、横坐标 x 和纵坐标 y 处移动，而不会发生碰撞，碰撞检测
    def tryMoveCurrent(self, direction, x, y):
        return self.tryMove(self.currentShape, direction, x, y)

    def tryMove(self, shape, direction, x, y):
        for x, y in shape.getCoords(direction, x, y):#遍历新形状中的每一个方块
            if x >= BoardData.width or x < 0 or y >= BoardData.height or y < 0:
                return False
            if self.backBoard[x + y * BoardData.width] > 0:
                return False
        return True
    #检查当前方块是否可以向下移动
    def moveDown(self):
        # 向下移动方块
        lines = 0
        if self.tryMoveCurrent(self.currentDirection, self.currentX, self.currentY + 1):#可以竖直向下1格
            self.currentY += 1#向下1格

        else:#不可以向下的情况
            self.mergePiece()
            lines = self.removeFullLines()#方法检查是否有满行，并移除满行。
            self.createNewPiece()
        return lines

    def dropDown(self):
        # 快速下落方块
        while self.tryMoveCurrent(self.currentDirection, self.currentX, self.currentY + 1):#判断可以向下移动
            self.currentY += 1


        self.mergePiece()
        lines = self.removeFullLines()
        self.createNewPiece()
        return lines

    def moveLeft(self):
        # 向左移动方块
        if self.tryMoveCurrent(self.currentDirection, self.currentX - 1, self.currentY):#检测是否可行
            self.currentX -= 1

    def moveRight(self):
        # 向右移动方块
        if self.tryMoveCurrent(self.currentDirection, self.currentX + 1, self.currentY):#检测是否可行
            self.currentX += 1

    def rotateRight(self):
        # 右旋转方块
        if self.tryMoveCurrent((self.currentDirection + 1) % 4, self.currentX, self.currentY):#检测是否可行
            self.currentDirection += 1
            self.currentDirection %= 4

    def rotateLeft(self):
        # 左旋转方块
        if self.tryMoveCurrent((self.currentDirection - 1) % 4, self.currentX, self.currentY):#检测是否可行
            self.currentDirection -= 1
            self.currentDirection %= 4

    def removeFullLines(self):
        # 移除完整的行
        newBackBoard = [0] * BoardData.width * BoardData.height#创建一个新的游戏板 newBackBoard，初始化为全0，与当前游戏板 self.backBoard 大小相同。
        newY = BoardData.height - 1#个变量 newY，表示新游戏板中当前处理的行数，初始值为游戏板高度减1。
        lines = 0#已移除的行数
        for y in range(BoardData.height - 1, -1, -1):
            blockCount = sum([1 if self.backBoard[x + y * BoardData.width] > 0 else 0 for x in range(BoardData.width)])#统计一行中有多少非0
            if blockCount < BoardData.width:#未满则在newBoard中复制oldBoard中的一行
                for x in range(BoardData.width):
                    newBackBoard[x + newY * BoardData.width] = self.backBoard[x + y * BoardData.width]
                newY -= 1
            else:#否则不复制
                lines += 1
        if lines > 0:
            self.backBoard = newBackBoard#有行被消除，则形成新的board
        return lines

    #将当前方块合并到游戏板
    def mergePiece(self):
        # 合并方块到游戏板
        for x, y in self.currentShape.getCoords(self.currentDirection, self.currentX, self.currentY):#获取当前方块在当前方向和位置的坐标
            self.backBoard[x + y * BoardData.width] = self.currentShape.shape#获取形状编号

        #设置成新的形状
        self.currentX = -1
        self.currentY = -1
        self.currentDirection = 0
        self.currentShape = Shape()

    def isGameOver(self):
        # 检查新生成的俄罗斯方块是否可以在初始位置下降
        if not BOARD_DATA.tryMoveCurrent(0, 5, -BOARD_DATA.nextShape.getBoundingOffsets(0)[2]):
            return True
        return False

    def clear(self):
        # 清空游戏数据
        self.currentX = -1#当前方块X坐标-1
        self.currentY = -1#当前方块y坐标-1
        self.currentDirection = 0#当前方块方向-1
        self.currentShape = Shape()#创建新的图形
        self.backBoard = [0] * BoardData.width * BoardData.height#创建尺寸大小全0背景矩阵

# 创建游戏数据对象
BOARD_DATA = BoardData()
