import sys
sys.path.append('past_game')
from game_tree import *
from random import random
import math

class RandomPlayer():
    def __init__(self):
        self.player_num = None
    
    def set_num(self, num):
        self.player_num = num
    
    def choose_coord(self, options):
        random_idx = math.floor(len(options) * random())
        return options[random_idx]

class MinimaxPlayer():
    def __init__(self):
        self.player_num = None
    
    def set_player_number(self, player_num):
        self.player_num = player_num
    
    def choose_move(self, game_state):
        game = GameTree(game_state, self.player_num)
        game.create_game_tree()
        game.set_node_scores()
        return game.get_best_move()

