# uncompyle6 version 3.4.0
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.5.6 |Anaconda, Inc.| (default, Aug 26 2018, 21:41:56) 
# [GCC 7.3.0]
# Embedded file name: /Users/yuegao/Downloads/code_new-1/code_new/board.py
# Compiled at: 2018-09-30 14:56:17
# Size of source mod 2**32: 8833 bytes


class Board(object):

    def __init__(self, size, piece_rows):#着色，三种颜色：红，蓝，白的涂色；正方形垂直方向数是row
        assert piece_rows < size    #assert（断言）用于判断一个表达式，在表达式条件为 false 的时候触发异常。
        self.size = size
        self.piece_rows = piece_rows
        self.board_status = {}
        for row in range(1, size + 1): #实际取值1,2,3,...,size
            for col in range(1, self.getColNum(row) + 1):
                if row <= piece_rows:
                    self.board_status[(row, col)] = 2
                else:
                    self.board_status[(row, col)] = 0

        for row in range(size + 1, size * 2):
            for col in range(1, self.getColNum(row) + 1):
                if row < size * 2 - piece_rows:
                    self.board_status[(row, col)] = 0
                else:
                    self.board_status[(row, col)] = 1

    def getColNum(self, row):
        if row in range(1, self.size + 1):
            return row
        else:
            return self.size * 2 - row

    def isEmptyPosition(self, pos):#判断是否是“无子区”
        return self.board_status[pos] == 0

    def leftPosition(self, pos):
        row = pos[0]
        col = pos[1]
        if (row, col - 1) in list(self.board_status.keys()):
            return (row, col - 1)

    def rightPosition(self, pos):
        row = pos[0]
        col = pos[1]
        if (row, col + 1) in list(self.board_status.keys()):
            return (row, col + 1)

    def upLeftPosition(self, pos):
        row = pos[0]
        col = pos[1]
        if row <= self.size and (row - 1, col - 1) in list(self.board_status.keys()):
            return (row - 1, col - 1)
        if row > self.size and (row - 1, col) in list(self.board_status.keys()):
            return (row - 1, col)
#这里是不是有问题

        #根据我的理解应该是这个样子的：
        #if row <= self.size and (row + 1, col) in list(self.board_status.keys()):
        #    return (row + 1, col)
        #if row > self.size and (row + 1, col - 1) in list(self.board_status.keys()):
        #    return (row + 1, col - 1)
#对于一个函数，如果没有return值的话，那么这个函数的值为None，也就是下文的None

    def upRightPosition(self, pos):
        row = pos[0]
        col = pos[1]
        if row <= self.size and (row - 1, col) in list(self.board_status.keys()):
            return (row - 1, col)
        if row > self.size and (row - 1, col + 1) in list(self.board_status.keys()):
            return (row - 1, col + 1)

    def downLeftPosition(self, pos):
        row = pos[0]
        col = pos[1]
        if row < self.size and (row + 1, col) in list(self.board_status.keys()):
            return (row + 1, col)
        if row >= self.size and (row + 1, col - 1) in list(self.board_status.keys()):
            return (row + 1, col - 1)

    def downRightPosition(self, pos):
        row = pos[0]
        col = pos[1]
        if row < self.size and (row + 1, col + 1) in list(self.board_status.keys()):
            return (row + 1, col + 1)
        if row >= self.size and (row + 1, col) in list(self.board_status.keys()):
            return (row + 1, col)

    #返回六个方向上毗邻的点，并不管是否被占据，只管是否有这个位置。
    #existence rather than occupation
    def adjacentPositions(self, pos):
        result = []
        result.append(self.leftPosition(pos))
        result.append(self.rightPosition(pos))
        result.append(self.upLeftPosition(pos))
        result.append(self.upRightPosition(pos))
        result.append(self.downLeftPosition(pos))
        result.append(self.downRightPosition(pos))
        return [x for x in result if x is not None]

    #返回某方（红方或者蓝方）的所有棋子的位置
    def getPlayerPiecePositions(self, player):
        # return a list of positions that player's pieces occupy
        result1 = [(row, col) for row in range(1, self.size + 1) for col in range(1, self.getColNum(row) + 1) \
                   if self.board_status[(row, col)] == player]
        result2 = [(row, col) for row in range(self.size + 1, self.size * 2) for col in
                   range(1, self.getColNum(row) + 1) \
                   if self.board_status[(row, col)] == player]
        return result1 + result2

    def getOneDirectionHopPosition(self, pos, dir_func):
        # return possible target hop position in the direction designated by dir_func,(for example, downRightPosition())
        # our rule: can hop as long as there's only one piece on the line between current position and target position
        # and the piece hopped over is at the middle point
        hop_over_pos = dir_func(pos)
        count = 0
        while hop_over_pos is not None:             #这个方向有位置，有延伸空间
            if self.board_status[hop_over_pos] != 0:#这个位置上面有棋子，可以借由此棋子hop
                break
            hop_over_pos = dir_func(hop_over_pos)
            count += 1
        if hop_over_pos is not None:
            target_position = dir_func(hop_over_pos)#实现hop，对称地跳
            while count > 0:
                if target_position is None or self.board_status[target_position] != 0:#根本跳不过去或者对称地路上遇到了障碍
                    break
                target_position = dir_func(target_position)
                count -= 1#对称的目的
            if count == 0 and target_position is not None and self.board_status[target_position] == 0:
                return target_position

    def getOneHopPositions(self, pos):
        result = []
        result.append(self.getOneDirectionHopPosition(pos, self.leftPosition))
        result.append(self.getOneDirectionHopPosition(pos, self.rightPosition))
        result.append(self.getOneDirectionHopPosition(pos, self.upLeftPosition))
        result.append(self.getOneDirectionHopPosition(pos, self.upRightPosition))
        result.append(self.getOneDirectionHopPosition(pos, self.downLeftPosition))
        result.append(self.getOneDirectionHopPosition(pos, self.downRightPosition))
        return [x for x in result if x is not None]

    #这边深度只有两层，只可能跳跃两次，不可能实现get all positions
    def getAllHopPositions(self, pos):
        # return all positions can be reached from current position in several hops
        result = self.getOneHopPositions(pos)
        start_index = 0
        while start_index < len(result):
            cur_size = len(result)
            for i in range(start_index, cur_size):
                for new_pos in self.getOneHopPositions(result[i]):
                    if new_pos not in result:
                        result.append(new_pos)
            start_index = cur_size
            if pos in result: #不能原地跳，防止又跳回来，把当前节点append
                result.remove(pos)
        return result

    def ifPlayerWin(self, player, iter):
        if player == 1:
            for row in range(1, self.piece_rows + 1):
                for col in range(1, self.getColNum(row) + 1):
                    if self.board_status[(row, col)] == 1:
                        continue
                    elif iter > 100 and self.board_status[(row, col)] == 2:
                        return True
                    else:
                        return False

        else:
            for row in range(self.size * 2 - self.piece_rows, self.size * 2):
                for col in range(1, self.getColNum(row) + 1):
                    if self.board_status[(row, col)] == 2:
                        continue
                    elif iter > 100 and self.board_status[(row, col)] == 1:
                        return True
                    else:
                        return False

        return True

    def isEnd(self, iter):
        player_1_reached = self.ifPlayerWin(1, iter)
        player_2_reached = self.ifPlayerWin(2, iter)
        if player_1_reached:
            return (True, 1)
        if player_2_reached:
            return (True, 2)
        return (False, None)

    def printBoard(self):
        for row in range(1, self.size + 1):
            print(' ' * (self.size - row), end=' ')
            for col in range(1, self.getColNum(row) + 1):
                print(str(self.board_status[(row, col)]), end=' ')

            print('\n', end=' ')

        for row in range(self.size + 1, self.size * 2):
            print(' ' * (row - self.size), end=' ')
            for col in range(1, self.getColNum(row) + 1):
                print(str(self.board_status[(row, col)]), end=' ')

            print('\n', end=' ')

    def printBoardOriginal(self):
        for row in range(1, self.size + 1):
            for col in range(1, self.getColNum(row) + 1):
                print(str(self.board_status[(row, col)]), end=' ')

            print('\n', end=' ')

        for row in range(self.size + 1, self.size * 2):
            for col in range(1, self.getColNum(row) + 1):
                print(str(self.board_status[(row, col)]), end=' ')

            print('\n', end=' ')

# okay decompiling board.pyc
