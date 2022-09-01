import sys
sys.path.append('game_tree_logs')
from logger import *

class ConnectFour():
    def __init__(self, players, log_name='c4_logs.txt'):
        self.players = players
        self.set_player_numbers()
        self.logs = Logger('/workspace/games/game_tree_logs/'+log_name)
        self.logs.clear_log()

        self.board = [[0 for _ in range(7)] for _ in range(6)] # each list is col
        self.winner = None
        self.round = 1 # both players go to complete a round
        self.log_board()
    
    def set_player_numbers(self):
        self.players[0].set_player_number(1)
        self.players[1].set_player_number(2)
    
    def transpose(self, board=None):
        if board == None:
            board = self.board
        t_board = []
        for i in range(len(board[0])):
            t_row = []
            for arr in board:
                t_row.append(arr[i])
            t_board.append(t_row)
        return t_board
    
    def log_board(self):
        for i in range(len(self.board)):
            row = self.board[i]
            row_string = ''
            for space in row:
                if space == None:
                    row_string += '_|'
                else:
                    row_string += str(space) + '|'
            self.logs.write(row_string[:-1]+'\n')
        self.logs.write('\n')
    
    def print_board(self):
        for i in range(len(self.board)):
            row = self.board[i]
            row_string = ''
            for space in row:
                if space == None:
                    row_string += '_|'
                else:
                    row_string += str(space) + '|'
            print(row_string[:-1])
        print('\n')
    
    def get_possible_moves(self):
        col_board = self.transpose(self.board)
        return [i for i,col in enumerate(col_board) if 0 in col]
    
    def make_move(self, player_num, col_index): # assuming input is valid
        col_board = self.transpose(self.board)
        col = col_board[col_index]
        i_r = col[::-1].index(0)
        col[len(col)-1-i_r] = player_num
        self.board = self.transpose(col_board)
    
    def complete_round(self):
        for player in self.players:
            choices = self.get_possible_moves()
            move = player.choose_move(self.board, choices)
            if move not in choices:
                move = choices[0]
                logs.write(f'Player {player.number} made invalid move')
            self.make_move(player.number, move)
            if self.check_for_winner() != None:
                self.winner = self.check_for_winner()
                for player in self.players:
                    player.report_winner(self.winner, self.board)
                break
        self.round += 1
        self.log_board()
    
    def arr_add(self, arr_1, arr_2):
        assert len(arr_1) == len(arr_2), 'different len arrays'
        result = []
        for i in range(len(arr_1)):
            result.append(arr_1[i] + arr_2[i])
        return result
    
    def coords_to_elem(self, coords):
        if type(coords)!=list:
            coords = [coords]
        elems = []
        for coord in coords:
            elems.append(self.board[coord[0]][coord[1]])
        return elems
    
    def get_diags(self):
        coords = [[0,i] for i in range(7)]+[[5,2],[5,3],[5,4]]
        diags = []
        for coord in coords:
            coord_diags = []
            dummy = list(coord)
            options = [[1,1], [1,-1],[-1,1],[-1,-1]]
            for option in options:
                diag = []
                while dummy[0]>=0 and dummy[0]<6 and dummy[1]>=0 and dummy[1]<7:
                    diag.append(dummy)
                    dummy = self.arr_add(dummy, option)
                if len(diag) > 3:
                    coord_diags.append(diag)
                dummy = list(coord)
            dummy = list(coord)
            diags += coord_diags
        
        diag_elems = []
        for diag in diags:
            diag_elems.append(self.coords_to_elem(diag))
        
        return diag_elems
    
    def check_len_four(self, arr):
        for i,val in enumerate(arr[:-3]):
            if val == 0:
                continue
            len_four = arr[i:i+4]
            if len(set(len_four)) == 1:
                return val
    
    def check_for_winner(self):
        rows = self.board
        cols = self.transpose()
        diags = self.get_diags()
        rcd = rows + cols + diags

        for arr in rcd:
            winner = self.check_len_four(arr)
            if winner != None:
                self.winner = winner
                return winner
        if 0 not in [item for item in arr for arr in rcd]:
            return 'Tie'
    
    def run_to_completion(self):
        while self.winner == None:
            self.complete_round()
        if self.winner != 'Tie':
            self.logs.write(f'PLAYER {self.winner} WINS')
        else:
            self.logs.write('TIE')