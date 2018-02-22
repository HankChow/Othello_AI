#!/usr/bin/env python3
# coding: utf-8


import re

class Othello(object):

    def __init__(self):
        self.board = {}
        for r in range(8):
            for c in range(8):
                self.board[(r, c)] = {'row': r, 'column': c, 'stone': None}
        self.board[(3, 3)]['stone'] = 1
        self.board[(4, 4)]['stone'] = 1
        self.board[(3, 4)]['stone'] = 0
        self.board[(4, 3)]['stone'] = 0
        self.sequence = []

    def generate(self, seq=None):
        # 根据下子序列生成盘面
        pass # TO_BE_IMPLEMENTED
        return

    def move(self, colour, position):
        position = position.upper()
        # 检查 position 参数合法性
        if not re.match('^[A-H][1-8]$', position):
            pass # TO_BE_IMPLEMENTED
            return
        # 检查 position 是否已被占
        centers = ['D4', 'E4', 'D5', 'E5']
        if position in centers + self.sequence:
            pass # TO_BE_IMPLEMENTED
            return 
        # 下子
        row, column = self.position2rc(position)
        self.sequence.append({
            'position': position,
            'colour': colour
        })
        self.board[(row, column)]['stone'] = colour
        # 提子
        taking = self.check_take(colour, position)
        if len(taking) > 0:
            for t in taking:
                self.board[self.position2rc(t)]['stone'] = colour
        
    def get_direction_stones(self, position, direction):
        stones = []
        r, c = self.position2rc(position)
        x, y = None, None
        if direction == 0:
            x, y = 1, 0
        if direction == 45:
            x, y = 1, -1
        if direction == 90:
            x, y = 0, -1
        if direction == 135:
            x, y = -1, -1
        if direction == 180:
            x, y = -1, 0
        if direction == 225:
            x, y = -1, 1
        if direction == 270:
            x, y = 0, 1
        if direction == 315:
            x, y = 1, 1
        for i in range(8):
            if 0 <= r + y * i <= 7 and 0 <= c + x * i <= 7:
                stones.append(self.board[(r + y * i, c + x * i)])
            else:
                return stones

    def check_take(self, colour, position):
        taking = []
        for i in range(8):
            direction_stones = self.get_direction_stones(position, i * 45)[1:]
            if colour not in list(map(lambda x: x['stone'], direction_stones)):
                continue
            nearest = list(map(lambda x: x['stone'], direction_stones)).index(colour)
            if None in direction_stones[:nearest]:
                continue
            taking.extend(list(map(lambda x: self.rc2position(x['row'], x['column']), direction_stones[:nearest])))
        return taking

    def print_board(self):
        for row in range(8):
            for column in range(8):
                if self.board[(row, column)]['stone'] is not None:
                    print(self.board[(row, column)]['stone'], end='')
                else:
                    print('_', end='')
            print()

    @staticmethod
    def rc2position(row, column):
        position = chr(column + 65) + str(row + 1)
        return position

    @staticmethod
    def position2rc(position):
        row = int(position[1]) - 1
        column = int(ord(position[0]) - ord('A'))
        return (row, column)

if __name__ == '__main__':
    pass
