import random as r
import math as m
from gene_players import *

class TicTacToeGene():
    def __init__(self, players):
        self.players = players
        self.board = [[None, None, None], [None, None, None], [None, None, None]]
        self.turn = 0
        self.winner = None
        # players should already be set up
        if None in [p.strategy for p in self.players]:
            print('Cannot run game with a player that doesnt have strat')
            return
    
    def update_board_state(self):
        board_state = ''
        for row in self.board:
            for val in row:
                if val == None:
                    board_state += '0'
                else:
                    board_state += str(val)
        self.board_state = board_state
        return board_state
    
    def get_rows_cols_diags(self):
        rows = [row for row in self.board]

        cols = []
        for col_index in range(len(self.board[0])):
            cols.append([row[col_index] for row in self.board])

        diag_1 = []
        top_left = (0,0)
        diag_2 = []
        top_right = (0,2)
        for i in range(len(self.board[0])):
            diag_1.append(self.board[top_left[0]+i][top_left[1]+i])
            diag_2.append(self.board[top_right[0]+i][top_right[1]-i])
        diags = [diag_1, diag_2]
        return rows + cols + diags
    
    def valid_only(self, nested_list):
        result = list(nested_list)
        for row in result:
            if row.count(None) == len(row):
                result.remove(row)
        return result
    
    def all_what_elem(self, ex_list):
        ex = ex_list[0]
        for item in ex_list:
            if item != ex:
                return False
        return ex
    
    def get_coord_options(self):
        valid_coords = []
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                if self.board[i][j] == None:
                    valid_coords.append((i,j))
        return valid_coords
    
    def flatten(self, nested_list):
        result = []
        for i in nested_list:
            result += i
        return result
    
    def check_for_winner(self):
        # rcd is rows, columns, diagonals
        rcd = self.get_rows_cols_diags()
        valid_rcd = self.valid_only(rcd)
        for item in valid_rcd:
            if self.all_what_elem(item) == 1:
                return 1
            if self.all_what_elem(item) == 2:
                return 2
        if None not in self.flatten(rcd):
            return 'Tie'
        return None
    
    def print_board(self):
        print('\n-----------')
        for row in self.board:
            for item in row[:-1]:
                if item == None:
                    print('0', end=' | ')
                    continue
                print(item, end=' | ')
            if row[-1] == None:
                print('0 |')
                continue
            print(row[-1],"|")
        print('-----------')
    
    def board_to_player_state(self, player_num):
        # 1 represents self and 2 represents opponent
        board_state = ''
        for row in self.board:
            for val in row:
                if val == None:
                    board_state += '0'
                if val == player_num:
                    board_state += '1'
                if val == 3-player_num:
                    board_state += '2'
        return board_state
    
    def state_to_board(self, board_state):
        board = []
        for i in [0, 3, 6]:
            board.append([int(board_state[n]) for n in [i, i+1, i+2]])
        return board
    
    def win_cap(self, player, board, choice):
        pass

    def complete_turn(self):
        if self.winner != None:
            return
        for i in range(len(self.players)):
            player = self.players[i]
            board_state = self.board_to_player_state(i+1)
            choice = player.move(board_state)
            row = int(m.floor(choice/3))
            col = int(choice % 3)
            self.board[row][col] = i+1
            if self.check_for_winner() != None:
                self.winner = self.check_for_winner()
                break
        self.turn += 1
    
    def run_to_completion(self, print_board=False):
        while self.winner == None:
            self.complete_turn()
            if print_board:
                self.print_board()

