import sys
sys.path.append('game_tree_logs')
from logger import *

class ConnectFour():
    def __init__(self, players, log_name='c4_logs.txt'):
        self.players = players
        self.set_player_numbers()
        self.logs = Logger('/workspace/games/game_tree_logs/'+log_name)
        self.logs.clear_log()

        self.col_board = [[0 for _ in range(6)] for _ in range(7)] # each list is col
        self.winner = None
        self.round = 1 # both players go to complete a round
        self.log_board()
    
    def set_player_numbers(self):
        self.players[0].set_player_number(1)
        self.players[1].set_player_number(2)
    
    def transpose(self, col_board=None):
        if col_board == None:
            col_board = self.col_board
        board = []
        for i in range(6):
            row = []
            for col in col_board:
                row.append(col[i])
            board.append(row)
        return board
    
    def log_board(self):
        board = self.transpose()
        for i in range(len(board)):
            row = board[i]
            row_string = ''
            for space in row:
                if space == None:
                    row_string += '_|'
                else:
                    row_string += str(space) + '|'
            self.logs.write(row_string[:-1]+'\n')
        self.logs.write('\n')
    
    def print_board(self):
        board = self.transpose()
        for i in range(len(board)):
            row = board[i]
            row_string = ''
            for space in row:
                if space == None:
                    row_string += '_|'
                else:
                    row_string += str(space) + '|'
            print(row_string[:-1])
        print('\n')
    
    def get_possible_moves(self):
        return [i for i,col in enumerate(self.col_board) if col.count(0)>0]
    
    def complete_round(self):
        for player in self.players:
            choices = self.get_possible_moves()