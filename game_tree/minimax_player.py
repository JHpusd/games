import sys
sys.path.append('games-cohort-2/tic-tac-toe')
from game_tree import *

class MinimaxPlayer():
    def __init__(self):
        self.number = None
        self.symbol = None
    
    def set_player_symbol(self, symbol):
        self.symbol = symbol
    
    def set_player_number(self, player_num):
        self.number = player_num
        self.game = GameTree([[None for _ in range(3)] for _ in range(3)], self.number)
        self.game.create_game_tree()
        self.game.set_node_scores()
    
    def update_board(self, game_state):
        if self.game.root.state != game_state:
            for child in self.game.root.children:
                if child.state == game_state:
                    self.game.root = child
    
    def choose_move(self, game_state):
        return self.game.get_best_move()