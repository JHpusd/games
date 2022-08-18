from random import random
import math

class InputPlayer:
  def __init__(self):
    self.symbol = None
    self.number = None
  
  def set_player_symbol(self, n):
    self.symbol = n
  
  def set_player_number(self, n):
    self.number = n

  def update_board(self, game_state):
      pass

  def print_board(self, board):
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
  
  def choose_move(self, game_state):
    choices = [(i,j) for i in range(len(game_state)) for j in range(len(game_state)) if game_state[i][j]==None]
    self.print_board(game_state)
    print(f'Your turn, you are player {self.number}')
    print('Input row, column values (starting from 1) of your desired move')
    inp = input('')
    inp_list = list(inp)

    row_col = []
    for elem in inp_list:
        try:
            row_col.append(int(elem))
        except:
            continue
    if len(row_col) != 2