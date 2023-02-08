import sys, math, random
from test_player import *
from random import random
sys.path.append('game_tree_logs')
from logger import *

class Checkers():
    def __init__(self, players, log_name='checkers_log.txt'):
        self.players = players
        self.board = [[((i+j)%2)*((3-((j<3)-(j>4))))%3 for i in range(8)] for j in range(8)]
        self.set_player_numbers()
        self.winner = None
        self.turn = 1
        # add log stuff later
    
    def set_player_numbers(self):
        self.players[0].set_player_number(1)
        self.players[1].set_player_number(2)
    
    def arr_add(self, arr_1, arr_2):
        return [arr_1[i] + arr_2[i] for i in range(len(arr_1))]
    
    def coord_val(self, coord):
        if coord[0] < 0 or coord[1] < 0:
            return None
        try:
            return self.board[coord[0]][coord[1]]
        except:
            return None
    
    def get_moves(self, coord):
        coord_val = self.coord_val(coord)
        moves = []
        options = []
        if coord_val == 0:
            return []
        if coord_val == 1:
            options = [(-1,1),(-1,-1)]
        if coord_val == 2:
            options = [(1,1),(1,-1)]
        if coord_val < 0:
            options = [(-1,1),(-1,-1),(1,1),(1,-1)]
        for option in options:
            if self.coord_val(self.arr_add(option, coord)) == 0:
                moves.append([coord, option])
        return moves
    
    def get_captures(self, coord):
        coord_val = self.coord_val(coord)
        captures = []
        if coord_val == 0:
            return []
        if coord_val == 1:
            options = [(-2,2),(-2,-2)]
        if coord_val == 2:
            options = [(2,2),(2,-2)]
        if coord_val < 0:
            options = [(-2,2),(-2,-2),(2,2),(2,-2)]
        for capture in options:
            if self.coord_val(self.arr_add(coord, capture)) != 0:
                continue
            direction = (int(capture[0]/2), int(capture[1]/2))
            check_coord = self.arr_add(coord, direction)
            check_coord_val = self.coord_val(check_coord)
            if check_coord_val == 3-abs(coord_val):
                captures.append([coord, capture])
        return captures
    
    def get_all_moves(self, player):
        valid_moves = []
        player_num = player.player_num
        for i, row in enumerate(self.board):
            for j, item in enumerate(row):
                if abs(item) == player_num:
                    moves = self.get_moves((i,j))
                    captures = self.get_captures((i,j))
                    valid_moves += captures
                    valid_moves += moves
        return valid_moves

    def print_board(self):
        print("\n   0 1 2 3 4 5 6 7")
        for i in range(8):
            row_to_print = f"{i} "
            for j in range(8):
                elem = self.board[i][j]
                if elem == 0:  row_to_print += "⬜" if ((i + j) % 2 == 0) else "  "
                if elem == 1:  row_to_print += "🔵"
                if elem == 2:  row_to_print += "🔴"
                if elem == -1: row_to_print += "💙"
                if elem == -2: row_to_print += "❤️ "
            print(row_to_print)
    
    def check_promotions(self):
        top_row = self.board[0]
        bottom_row = self.board[7]
        for i, item in enumerate(top_row):
            if item == 1:
                self.board[0][i] = -1
        for i, item in enumerate(bottom_row):
            if item == 2:
                self.board[7][i] = -2
    
    def del_captured_piece(self, capt_move):
        coord = capt_move[0]
        translation = capt_move[1]
        if abs(translation[0]) != 2:
            return
        direction = (int(translation[0]/2), int(translation[1]/2))
        capt_coord = self.arr_add(coord, direction)
        self.board[capt_coord[0]][capt_coord[1]] = 0
    
    def flatten(self, nested_arr):
        result = []
        for arr in nested_arr:
            result += arr
        return result
    
    def run_turn(self):
        for player in self.players:
            if self.winner != None:
                return
            options = self.get_all_moves(player)
            if len(options) == 0:
                self.winner = 3-player.player_num
                continue
            move = player.choose_move(self.board, options)
            if move not in options:
                move = random.choice(options)
            self.del_captured_piece(move)
            
            coord = move[0]
            coord_val = self.coord_val(coord)
            translation = move[1]
            new_coord = self.arr_add(coord, translation)
            self.board[coord[0]][coord[1]] = 0
            self.board[new_coord[0]][new_coord[1]] = coord_val
            self.check_promotions()

            while abs(translation[0]) == 2:
                no_move_opt = [[new_coord, (0,0)]]
                chain_opts = self.get_captures(new_coord)
                options = chain_opts + no_move_opt
                move = player.choose_move(self.board, options)
                self.del_captured_piece(move)
                coord = move[0]
                coord_val = self.coord_val(coord)
                translation = move[1]
                new_coord = self.arr_add(coord, translation)
                self.board[coord[0]][coord[1]] = 0
                self.board[new_coord[0]][new_coord[1]] = coord_val
                self.check_promotions()

        self.turn += 1
        if self.turn >= 100:
            self.winner = 'Tie'
        flat_board = self.flatten(self.board)
        flat_board = [abs(item) for item in flat_board]
        if flat_board.count(1)==1 and flat_board.count(2)==1:
            self.winner = 'Tie'
    
    def run_to_completion(self):
        while self.winner == None:
            self.run_turn()

test_board = [
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,2,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,0,2,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,0,1,0,0,0,0],
    [0,0,1,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
]
