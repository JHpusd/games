from random import random
import math

class AntonLastMinPlayer:
  def __init__(self):
    self.symbol = None
    self.number = None
    self.first = None
  
  def set_player_symbol(self, n):
    self.symbol = n
  
  def set_player_number(self, n):
    self.number = n
  
  def set_first(self, first):
    self.first = first

  def transpose_board(self, state):
    return [[state[i][j] for i in range(7)] for j in range(6)] 
    
  def get_diagonals(self, state, row_index):
    forward_diag = []
    back_diag = []
    
    forward_coord = [row_index, 3]
    back_coord = [row_index, 3]
    while back_coord[0] >= 0 and back_coord[1] >= 0:
      forward_diag.append(state[forward_coord[1]][forward_coord[0]])
      back_diag.append(state[back_coord[1]][back_coord[0]])
      forward_coord[0]-=1
      back_coord[0]-=1
      forward_coord[1]+=1
      back_coord[1]-=1

    forward_coord = [row_index+1, 2]
    back_coord = [row_index+1, 4]
    while back_coord[0] <= 5 and back_coord[1] <= 6:
      forward_diag.insert(0,state[forward_coord[1]][forward_coord[0]])
      back_diag.insert(0,state[back_coord[1]][back_coord[0]])
      forward_coord[0]+=1
      back_coord[0]+=1
      forward_coord[1]-=1
      back_coord[1]+=1
      
    return [forward_diag, back_diag]
  
  def get_all_diagonals(self, state):
    all_diags = []
    for i in range(6):
      all_diags += self.get_diagonals(state, i)
    return all_diags
  
  def four_in_a_row(self, player, line):
    four_str = ''.join([player for _ in range(4)])
    line_str = ''.join([val if val != None else '0' for val in line])

    return four_str in line_str
  
  def check_for_winner(self, state):
    cols = state.copy()
    rows = self.transpose_board(state)
    diags = self.get_all_diagonals(state)

    board_full = True
    for line in (rows + cols + diags):
      if None in line:
        board_full = False

      for player in ['1','2']:
        if self.four_in_a_row(player, line):
          return player
    
    if board_full:
      return 'Tie'
    return None
  
  def choose_move(self, state, choices):
    cols = state.copy()
    rows = self.transpose_board(state)
    diags = self.get_all_diagonals(state)
    lines = cols + rows + diags
    for line in lines:
      pass
      #something
    
    random_idx = math.floor(len(choices) * random())
    return choices[random_idx]