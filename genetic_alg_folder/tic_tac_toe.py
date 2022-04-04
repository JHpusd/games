import random as r
import math as m
from gene_players import *

class TicTacToeGene():
    def __init__(self, players, override_init=False):
        self.players = players
        self.board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.turn = 0
        self.winner = None
        # players should already be set up
        if override_init:
            return
        if None in [p.strategy for p in self.players]:
            print('Cannot run game with a player that doesnt have strat')
            return
    
    def update_board_state(self):
        board_state = ''
        for row in self.board:
            for val in row:
                if val == 0:
                    board_state += '0'
                else:
                    board_state += str(val)
        self.board_state = board_state
        return board_state
    
    def get_rows_cols_diags(self, board):
        assert len(board) == 3 and len(board[0]) == 3, 'board size error (in game, get rcd)'

        rows = [row for row in board]

        cols = []
        for col_index in range(len(board[0])):
            cols.append([row[col_index] for row in board])

        diag_1 = []
        top_left = (0,0)
        diag_2 = []
        top_right = (0,2)
        for i in range(len(board[0])):
            diag_1.append(board[top_left[0]+i][top_left[1]+i])
            diag_2.append(board[top_right[0]+i][top_right[1]-i])
        diags = [diag_1, diag_2]
        return rows + cols + diags
    
    def rcd_of_coord(self, board, coord):
        coord_rcd = []
        labeled_board = [[(0,0), (0,1), (0,2)], [(1,0), (1,1), (1,2)], [(2,0), (2,1), (2,2)]]
        rcd = self.get_rows_cols_diags(labeled_board)
        for item in rcd:
            if coord in item:
                coord_rcd.append(item)
        
        result = []
        for i in range(len(coord_rcd)):
            item = coord_rcd[i]
            result.append([])
            for x,y in item:
                result[i].append(board[x][y])
        return result

    def valid_only(self, nested_list):
        result = list(nested_list)
        for row in result:
            if row.count(0) == len(row):
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
                if self.board[i][j] == 0:
                    valid_coords.append((i,j))
        return valid_coords
    
    def flatten(self, nested_list):
        result = []
        for i in nested_list:
            result += i
        return result
    
    def check_for_winner(self, board):
        # rcd is rows, columns, diagonals
        rcd = self.get_rows_cols_diags(board)
        valid_rcd = self.valid_only(rcd)
        for item in valid_rcd:
            if self.all_what_elem(item) == 1:
                return 1
            if self.all_what_elem(item) == 2:
                return 2
        if 0 not in self.flatten(rcd):
            return 'Tie'
        return None
    
    def print_board(self):
        print('\n-----------')
        for row in self.board:
            for item in row[:-1]:
                if item == 0:
                    print('0', end=' | ')
                    continue
                print(item, end=' | ')
            if row[-1] == 0:
                print('0 |')
                continue
            print(row[-1],"|")
        print('-----------')
    
    def board_to_player_state(self, board, player_num):
        # 1 represents self and 2 represents opponent
        board_state = ''
        for row in board:
            for val in row:
                if val == 0:
                    board_state += '0'
                if val == player_num:
                    board_state += '1'
                if val == 3-player_num:
                    board_state += '2'
        return board_state
    
    def state_to_board(self, board_state):
        assert len(board_state) == 9, 'board state length error (in game, state to board)'
        board = []
        for i in [0, 3, 6]:
            board.append([int(board_state[n]) for n in [i, i+1, i+2]])
        return board
    
    def get_player_board(self, player, board):
        if type(board) == str:
            board = self.state_to_board(board)
        player_num = self.players.index(player) + 1

        player_board = []
        for i in range(3):
            row = board[i]
            player_board.append([])
            for item in row:
                if item == player_num:
                    player_board[i].append(1)
                elif item == 3 - player_num:
                    player_board[i].append(2)
                elif item == 0:
                    player_board[i].append(0)
        return player_board
    
    def board_copy(self, board):
        result = []
        for i in range(len(board)):
            result.append([])
            for j in range(len(board[0])):
                result[i].append(board[i][j])
        return result

    def complete_turn(self):
        if self.winner != None:
            return
        for i in range(len(self.players)):
            player = self.players[i]
            board_state = self.board_to_player_state(self.board, i+1)
            choice = player.move(board_state)
            # check win cap and loss prev with player, board state, and choice
            row = int(m.floor(choice/3))
            col = int(choice % 3)
            self.board[row][col] = i+1
            self.winner = self.check_for_winner(self.board)
            if self.winner != None:
                break
        self.turn += 1
    
    def run_to_completion(self, print_board=False):
        while self.winner == None:
            self.complete_turn()
            if print_board:
                self.print_board()

