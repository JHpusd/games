from random import random

class TicTacToe:
  def __init__(self, players):
    self.players = players
    # self.set_player_symbols()
    self.set_player_numbers()
    # self.determine_player_order()
    self.board = [[None for _ in range(3)] for _ in range(3)]
    self.round =  1
    self.winner = None
  '''
  def set_player_symbols(self): 
    self.players[0].set_player_symbol('X')
    self.players[1].set_player_symbol('O')
  '''
  def set_player_numbers(self): 
    self.players[0].set_player_number(1)
    self.players[1].set_player_number(2)
  '''
  def determine_player_order(self):
    rand = round(random())
    if rand == 1:
      self.players = self.players[::-1]
  '''
  def get_possible_moves(self):
    possible_moves = [(i,j) for i in range(3) for j in range(3) if self.board[i][j] == None]
    return possible_moves

  def complete_round(self):
    for player in self.players:
      player_move = player.choose_move(self.board)
      self.board[player_move[0]][player_move[1]] = player.number
      self.update_player_boards()
      if self.check_for_winner() != None:
        self.winner = self.check_for_winner()
        break
    self.round += 1

  def run_to_completion(self):
    while self.winner == None:
      self.complete_round()

  def check_for_winner(self):
    rows = self.board.copy()
    cols = [[self.board[i][j] for i in range(3)] for j in range(3)]
    diags = [[self.board[i][i] for i in range(3)],
             [self.board[i][2-i] for i in range(3)]]

    board_full = True
    for row in rows + cols + diags:
      if None in row:
        board_full = False

      for player in self.players:
        if row == [player.number for _ in range(3)]:
          return player.number
    
    if board_full:
      return 'Tie'
    return None

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

  def update_player_boards(self):
    for player in self.players:
        player.update_board(self.board)