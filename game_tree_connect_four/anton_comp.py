import random
import math
import time
import numpy as np
import copy

class Node:
  def __init__(self, state, player):
    self.state = state
    self.player = player
    self.winner = None
    self.children = []
    self.score = None
  
  def print_state(self):
    transpose_board = self.transpose_board()
    for i in range(len(transpose_board)):
      row = transpose_board[i]
      row_string = ''
      for space in row:
        if space == None:
          row_string += '_|'
        else:
          row_string += space + '|'
      print(row_string[:-1])
    print('\n')
  
  def transpose_board(self):
    return [[self.board[i][j] for i in range(7)] for j in range(6)] 


class HeuristicGameTree:
  def __init__(self, player, first, search_depth):
    self.root = Node([[None for _ in range(6)] for _ in range(7)], first)
    self.player = player
    self.first = first
    self.search_depth = search_depth
    self.node_num = 1
    self.leaf_node_num = 0
    self.state_dict = {''.join(['0' for _ in range(42)]):self.root}
    self.build_part_of_tree(self.root)

  def get_open_columns(self, state):
    open_columns = [i for i in range(7) if None in state[i]]
    return open_columns

  def get_opposite_symbol(self, symbol):
    if symbol == '1':
      return '2'
    elif symbol == '2':
      return '1'

  def state_to_string(self, state):
    #print(state)
    state_list = []
    for col in state:
      state_list += col
    str_list = ['0' if i == None else i for i in state_list]
    return ''.join(str_list)

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
  
  def transpose_board(self, state):
    return [[state[i][j] for i in range(7)] for j in range(6)] 
  
  def get_node(self, state):
    current_nodes = [self.root]
    while True:
      for node in current_nodes:
        if node.state == state:
          return node
        else:
          current_nodes += node.children
          current_nodes.remove(node)

  def build_part_of_tree(self, start_node):
    current_layer = [start_node]
    for i in range(self.search_depth):
      next_layer = []
      for node in current_layer:
        if node.winner == None:
          for col_num in self.get_open_columns(node.state):
            new_state = [[node.state[i][j] for j in range(6)] for i in range(7)]
            i = 0
            while i+1 < 6 and new_state[col_num][i+1]==None:
              i+=1
                
            new_state[col_num][i] = node.player
            
            new_string = self.state_to_string(new_state)
            if new_string in self.state_dict.keys():
              existing_node = self.state_dict[new_string]
              node.children.append(existing_node)
            else:
              new_node = Node(new_state, self.get_opposite_symbol(node.player))
              new_node.winner = self.check_for_winner(new_state)
              node.children.append(new_node)
              next_layer.append(new_node)

              self.state_dict[new_string] = new_node
              self.node_num += 1
              if new_node.winner != None:
                self.leaf_node_num += 1
                break

      current_layer = next_layer

  def check_sublist(self, A, B):
    n = len(A)
    # for i in range(len(B)-n + 1):
    #   if A == B[i:i + n]:
    #     return i
    # return None
    return any(A == B[i:i + n] for i in range(len(B)-n + 1))      

  def heuristic_function(self, state, player):
    cols = state.copy()
    rows = self.transpose_board(state)
    diags = self.get_all_diagonals(state)
    lines = rows + cols + diags
    
    score = 0
    opponent = self.get_opposite_symbol(player)
    for line in lines:
      player_connected = [[player], [player,player], [player,player,player]]
      for connected in player_connected:
        left_open = [None] + connected
        right_open = connected + [None]
        if self.check_sublist(left_open, line):
          score += 0.0625*(4**(len(connected)-1)) # 0.25*(2**(len(connected)-1))

        if self.check_sublist(right_open, line):
          score += 0.0625*(4**(len(connected)-1)) # 0.25*(2**(len(connected)-1))
        
      opponent_connected = [[opponent], [opponent, opponent], [opponent,opponent,opponent]]
      for connected in opponent_connected:
        left_open = [None] + connected
        right_open = connected + [None]
        if self.check_sublist(left_open, line):
          score -= 0.0625*(4**(len(connected)-1)) # 0.25*(2**(len(connected)-1))

        if self.check_sublist(right_open, line):
          score -= 0.0625*(4**(len(connected)-1)) # 0.25*(2**(len(connected)-1))

    return score/len(lines)
    

  def set_scores(self, node, player):
    if node.children != []:
      for child in node.children:
        self.set_scores(child, player)

      scores = [child.score for child in node.children]
      if node.player == str(self.player):
        node.score = max(scores)
      else:
        node.score = min(scores)
    else: 
      if node.winner == None:
        node.score = self.heuristic_function(node.state, player)
      elif node.winner == player:
        node.score = 1
      elif node.winner == 'Tie':
        node.score = 0
      else:
        node.score = -1


class AntonHeuristicPlayer:
  def __init__(self, search_depth = 4):
    self.symbol = None
    self.number = None
    self.first = None
    self.search_depth = search_depth
    self.game_tree = None
  
  def set_player_symbol(self, n):
    self.symbol = n
  
  def set_player_number(self, n):
    self.number = n
    self.symbol = str(n)
  # def set_first(self, first):
    self.first = '1'
    self.game_tree = HeuristicGameTree(self.number, self.first, self.search_depth)
    self.game_tree.set_scores(self.game_tree.root, self.symbol)

  def transpose(self, state):
    return [[state[i][j] for i in range(len(state))] for j in range(len(state[0]))]
  
  def choose_move(self, state, choices):
    #col_state = state
    start_time = time.time()
    col_state = self.transpose(state)
    new_state = copy.deepcopy(col_state)

    for row in range(len(col_state)):
        for column in range(len(col_state[row])):
            num = col_state[row][column]

            if num != 0:
                new_state[row][column] = str(num)

            else:
                new_state[row][column] = None

    state_string = self.game_tree.state_to_string(new_state)
    if state_string not in self.game_tree.state_dict.keys():
      self.game_tree.state_dict[state_string] = Node(new_state, self.symbol)
    state_node = self.game_tree.state_dict[state_string]

    if state_node.children == []:
      self.game_tree.build_part_of_tree(state_node)
      self.game_tree.set_scores(state_node, self.symbol)
    scores = [child.score for child in state_node.children]
    max_score = max(scores)
    max_indices = [i for i, x in enumerate(scores) if x == max_score]
    #random_index = random.choice(max_indices)
    chosen_state = state_node.children[max_indices[0]].state
    for choice in choices:
      choice_state = copy.deepcopy(new_state)#[[new_state[i][j] for j in range(6)] for i in range(7)]
      i = 0
      while i+1 < 6 and choice_state[choice][i+1]==None:
        i+=1
      choice_state[choice][i] = self.symbol

      if choice_state == chosen_state:
        #print(f"Anton took {time.time() - start_time} seconds to make his move")
        return choice