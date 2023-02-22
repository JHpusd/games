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
    
    def nested_list_in_list(self, parent_list, nested_list):
        for l in parent_list:
            if all(x == y for x, y in zip(l, nested_list)):
                return True
        return False
    
    def find_translation(self, coord1, coord2):
        return [coord1[0] - coord2[0], coord1[1] - coord2[1]]
    
    def get_all_moves(self, player, state=None):
        
        if state == None: state = self.state

        possible_moves = []

        # loop through all coordinates

        for i in range(8):
            for j in range(8):

                current_coords = [i, j]
                current_piece = state[i][j]

                # check if there is a piece on the current coord

                if abs(current_piece) == player.player_num:

                    # get moves that the piece might be able to do

                    moves_to_check = self.add_moves_to_check(current_piece, current_coords, [], [])

                    while len(moves_to_check) > 0:

                        # check first move in moves_to_check

                        move_to_check = moves_to_check.pop(0) # moves_to_check is a queue
                        coord, translation_to_check, captured_coords = move_to_check

                        new_i, new_j = self.arr_add(coord, translation_to_check)
                        if new_i < 0 or new_i > 7 or new_j < 0 or new_j > 7: continue
                        new_piece = state[new_i][new_j]

                        # check if the new spot is empty

                        if abs(new_piece) == 0 and captured_coords == []:
                            possible_moves.append(move_to_check)
                    
                        # check if the opponent is in the new spot

                        elif abs(new_piece) == 3 - player.player_num:
                            
                            # if so, and if the next next spot is empty, add that spot to moves_to_check

                            next_translation = [2*t for t in translation_to_check]
                            new_new_i, new_new_j = self.arr_add(coord, next_translation)
                            if new_new_i < 0 or new_new_i > 7 or new_new_j < 0 or new_new_j > 7: continue
                            new_new_piece = state[new_new_i][new_new_j]

                            if abs(new_new_piece) == 0 and not self.nested_list_in_list(captured_coords, [new_i, new_j]):

                                # add capture to possible moves

                                previous_translation = self.find_translation(coord, current_coords)
                                new_translation = self.arr_add(previous_translation, next_translation)
                                new_captured_coords = captured_coords + [[new_i, new_j]]
                                possible_moves.append([current_coords, new_translation, new_captured_coords])

                                # add potential to combo captures

                                next_next_coords = self.arr_add(current_coords, new_translation)
                                moves_to_check = self.add_moves_to_check(current_piece, next_next_coords, new_captured_coords, moves_to_check)

                                # then, it'll loop back to the start of moves_to_check
        
        return possible_moves

    def add_moves_to_check(self, current_piece, current_coords, captured_coords, moves_to_check):
        
        direction = 1 - 2*(current_piece % 2)

        moves_to_check.append([current_coords, [direction, -1], captured_coords])
        moves_to_check.append([current_coords, [direction, 1], captured_coords])

        if current_piece < 0:
            moves_to_check.append([current_coords, [-direction, -1], captured_coords])
            moves_to_check.append([current_coords, [-direction, 1], captured_coords])
        
        return moves_to_check

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
    
    def del_captured_pieces(self, capt_move):
        for capt_coord in capt_move[2]:
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
            options = self.get_all_moves(player, self.board)
            if len(options) == 0:
                self.winner = 3-player.player_num
                continue
            move = player.choose_move(self.board, options)
            if move not in options:
                move = random.choice(options)
            self.del_captured_pieces(move)
            
            coord = move[0]
            coord_val = self.coord_val(coord)
            new_coord = self.arr_add(coord,move[1])
            self.board[new_coord[0]][new_coord[1]] = coord_val
            self.board[coord[0]][coord[1]] = 0
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
