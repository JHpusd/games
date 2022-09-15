from heuristic_game_tree import *

class HeuristicPlayer():
    def __init__(self, h_func, ply):
        self.number = None
        self.func = h_func
        self.ply = ply
    
    def set_player_number(self, player_num):
        self.number = player_num
        self.tree = HeuristicGameTree([[None for _ in range(3)] for _ in range(3)], self.number, self.func, self.ply)
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