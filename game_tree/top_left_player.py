from random import random
import math

class TopLeftPlayer:
  def __init__(self):
    self.symbol = None
    self.number = None
  
  def set_player_symbol(self, n):
    self.symbol = n
  
  def set_player_number(self, n):
    self.number = n

  def update_board(self, game_state):
      pass
  
  def choose_move(self, game_state):
    choices = [(i,j) for i in range(len(game_state)) for j in range(len(game_state)) if game_state[i][j]==None]
    top_left = choices[0]
    min_val = choices[0][0] + choices[0][1]
    for choice in choices[1:]:
        if choice[0] + choice[1] < min_val:
            top_left = choice
            min_val = choice[0] + choice[1]
    return top_left
  
  def report_winner(self, winner_num,board):
    pass