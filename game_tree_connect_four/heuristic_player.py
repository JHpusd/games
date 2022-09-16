from heuristic_game_tree import *

def heuristic_func(game_state, player_num, turn):
    return 1

class HeuristicPlayer():
    def __init__(self, ply, h_func=heuristic_func):
        self.number = None
        self.func = h_func
        self.ply = ply
    
    def set_player_number(self, player_num):
        init_state = [[0 for _ in range(7)] for _ in range(6)]
        self.number = player_num
        self.tree = HeuristicGameTree(init_state, self.number, self.func, self.ply)
        self.tree.init_create_game_tree()
        self.tree.set_node_scores() # creates tree
    
    def update_board(self, game_state):
        if self.tree.root.state != game_state:
            for child in self.tree.root.children:
                if child.state == game_state:
                    self.tree.root = child
                    return
    
    def choose_move(self, game_state):
        self.tree.extend_game_tree()
        self.tree.set_node_scores()
        return self.tree.get_best_move()
    
    def report_winner(self, winner_num,board):
        pass