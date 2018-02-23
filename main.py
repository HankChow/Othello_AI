#!/usr/bin/env python3
# coding: utf-8


import re
from pprint import pprint

class Othello(object):

    def __init__(self):
        self.board = {}
        for r in range(8):
            for c in range(8):
                self.board[(r, c)] = {'row': r, 'column': c, 'stone': None}
        self.board[(3, 3)]['stone'] = 0
        self.board[(4, 4)]['stone'] = 0
        self.board[(3, 4)]['stone'] = 1
        self.board[(4, 3)]['stone'] = 1
        self.sequence = []

    def generate(self, seq=None):
        # 根据下子序列生成盘面
        pass # TO_BE_IMPLEMENTED
        return

    def move(self, colour, position, count_activity=False):
        position = position.upper()
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
        # 提子，如果 count_activity 为 True 时仅计算提掉的散度，不提子 
        taking = self.check_take(colour, position)
        if count_activity:
            activity = 0
            if len(taking) == 0:
                return 0
            for t in taking:
                activity += self.get_stone_activity(t)
            return activity
        self.board[(row, column)]['stone'] = colour
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
        return stones

    def check_take(self, colour, position):
        taking = []
        for i in range(8):
            direction_stones = self.get_direction_stones(position, i * 45)[1:]
            if colour not in list(map(lambda x: x['stone'], direction_stones)):
                continue
            nearest = list(map(lambda x: x['stone'], direction_stones)).index(colour)
            if None in list(map(lambda x: x['stone'], direction_stones[:nearest])):
                continue
            taking.extend(list(map(lambda x: self.rc2position(x['row'], x['column']), direction_stones[:nearest])))
        return taking

    def get_available_moves(self, colour):
        available_moves = []
        for row in range(8):
            for column in range(8):
                if self.board[(row, column)]['stone'] is None:
                    if len(self.check_take(colour, self.rc2position(row, column))) > 0:
                        available_moves.append(self.rc2position(row, column))
        return available_moves

    def get_stone_activity(self, position):
        stone_activity = 0
        r, c = self.position2rc(position)
        for x in range(-1, 2, 1):
            for y in range(-1, 2, 1):
                if x == 0 and y == 0:
                    continue
                if r + y >= 0 and c + x >= 0:
                    if self.board[(r + y, c + x)]['stone'] is None:
                        stone_activity += 1
        return stone_activity

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
