#!/usr/bin/env python3
# coding: utf-8


import random
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
        """ 根据下子序列生成盘面 """
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
        # 提子，如果 count_activity 为 True 时仅计算提掉的散度而不提子 
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
        """ 获取某位置上某方向的棋子 """
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
        """ 获取某步下法的提子情况 """
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
        """ 获取某方的可行位置 """
        available_moves = []
        for row in range(8):
            for column in range(8):
                if self.board[(row, column)]['stone'] is None:
                    if len(self.check_take(colour, self.rc2position(row, column))) > 0:
                        available_moves.append(self.rc2position(row, column))
        return available_moves

    def get_stone_activity(self, position):
        """ 计算某个位置的散度 """
        stone_activity = 0
        r, c = self.position2rc(position)
        for x in range(-1, 2, 1):
            for y in range(-1, 2, 1):
                if x == 0 and y == 0:
                    continue
                if 0 <= r + y <= 7 and 0 <= c + x <= 7:
                    if self.board[(r + y, c + x)]['stone'] is None:
                        stone_activity += 1
        return stone_activity

    def get_decision(self, colour):
        decision = []
        current_activity = 64
        available_moves = self.get_available_moves(colour)
        if len(available_moves) == 0:
            return decision
        for move in available_moves:
            if len(decision) == 0:
                decision.append(move)
                current_activity = self.move(colour, move, count_activity=True)
                continue
            if self.move(colour, move, count_activity=True) < current_activity:
                decision = []
                decision.append(move)
                continue
            if self.move(colour, move, count_activity=True) == current_activity:
                decision.append(move)
                continue
            if self.move(colour, move, count_activity=True) > current_activity:
                continue
        return decision[random.randint(0, len(decision) - 1)]

    def final_count(self):
        blacks = 0
        whites = 0
        for row in range(8):
            for column in range(8):
                if self.board[(row, column)]['stone'] == 0:
                    whites += 1
                if self.board[(row, column)]['stone'] == 1:
                    blacks += 1
        if blacks > whites:
            print('Black wins.')
        elif blacks < whites:
            print('White wins.')
        else:
            print('Draw.')
        exit()

    def print_board(self):
        blacks = 0
        whites = 0
        for row in range(8):
            for column in range(8):
                if self.board[(row, column)]['stone'] == 1:
                    blacks += 1
                if self.board[(row, column)]['stone'] == 0:
                    whites += 1
        print('  A B C D E F G H ')
        for row in range(8):
            print(row + 1, end=' ')
            for column in range(8):
                if self.board[(row, column)]['stone'] is not None:
                    print(self.board[(row, column)]['stone'], end=' ')
                else:
                    print('_', end=' ')
            print()
        print('black({})-({})white'.format(blacks, whites))
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


def run():
    o = Othello()
    ai_colour = int(input('输入 AI 使用的棋子：0 为执白后手，1 为执黑先手\n'))
    user_colour = 0 if ai_colour == 1 else 1
    if ai_colour == 1:
        o.move(ai_colour, o.get_decision(ai_colour))
        o.print_board()
        cannot_move_flag = 0
    else:
        o.print_board()
    while(True):
        if len(o.get_available_moves(user_colour)) > 0:
            while(True):
                user_movement = input('{}方输入：\n'.format('黑' if user_colour == 1 else '白')).upper()
                if user_movement in o.get_available_moves(user_colour):
                    break
            o.move(user_colour, user_movement)
            cannot_move_flag = 0
            o.print_board()
        else:
            cannot_move_flag += 1
        if len(o.get_available_moves(ai_colour)) > 0:
            movement = o.get_decision(ai_colour)
            o.move(ai_colour, movement)
            cannot_move_flag = 0
            print('{}方：{}'.format('黑' if ai_colour == 1 else '白', movement))
            print()
            o.print_board()
        else:
            cannot_move_flag += 1
        if cannot_move_flag >= 2:
            o.final_count()


if __name__ == '__main__':
    run()
