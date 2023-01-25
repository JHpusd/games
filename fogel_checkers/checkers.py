import sys
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
        player_num = abs(self.coord_val(coord))
        moves = []
        if player_num == 0:
            return []
        if player_num == 1:
            options = [(-1,1),(-1,-1)]
            for option in options:
                if self.coord_val(self.arr_add(option, coord)) == 0:
                    moves.append([coord, option])
        if player_num == 2:
            options = [(1,1),(1,-1)]
            for option in options:
                if self.coord_val(self.arr_add(option, coord)) == 0:
                    moves.append([coord, option])
        return moves
    
    def get_captures(self, coord):
        player_num = abs(self.coord_val(coord))
        captures = []
        if player_num == 0:
            return []
        if player_num == 1:
            check = [self.arr_add(coord,(-1,1)),self.arr_add(coord,(-1,-1))]
            options = [(-2,2),(-2,-2)]
            option_coords = [self.arr_add(coord,opt) for opt in options]
            for i, check_coord in enumerate(check):
                if self.coord_val(check_coord) == 3-player_num:
                    if self.coord_val(option_coords[i]) == 0:
                        captures.append([coord, options[i]])
        if player_num == 2:
            check = [self.arr_add(coord,(1,1)),self.arr_add(coord,(1,-1))]
            options = [(2,2),(2,-2)]
            option_coords = [self.arr_add(coord,opt) for opt in options]
            for i, check_coord in enumerate(check):
                if self.coord_val(check_coord) == 3-player_num:
                    if self.coord_val(option_coords[i]) == 0:
                        captures.append([coord, options[i]])
        return captures
    
    def get_valid_moves(self, player):
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
        for row in self.board:
            print(row)
    
    def run_turn(self):
        for player in players:
            

p1 = TestPlayer()
p2 = TestPlayer()
test = Checkers([p1,p2])
test.print_board()
print(test.get_valid_moves(p2))