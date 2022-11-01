from heuristic_game_tree import *

class HeuristicPlayer():
    def __init__(self, ply=4):
        self.number = None
        self.ply = ply
    
    def transpose(self, board):
        t_board = []
        for i in range(len(board[0])):
            t_row = []
            for arr in board:
                t_row.append(arr[i])
            t_board.append(t_row)
        return t_board
    
    def set_player_number(self, player_num):
        init_state = [[0 for _ in range(7)] for _ in range(6)]
        self.number = player_num
        self.tree = HeuristicGameTree(init_state, self.number, self.ply)
        self.tree.init_create_game_tree()
        self.tree.set_node_scores() # creates tree
    '''
    def update_board(self, game_state):
        if self.tree.root.state != game_state:
            for child in self.tree.root.children:
                if child.state == game_state:
                    self.tree.root = child
                    self.tree.prune()
                    self.tree.extend_game_tree()
                    return
    '''
    def choose_move(self, game_state, choices):
        # for anton's game
        # game_state = self.transpose(game_state)
        self.tree.root = self.tree.all_nodes[str(game_state)]
        self.tree.prune()
        self.tree.extend_game_tree()
        self.tree.set_node_scores()
        return self.tree.get_best_move()
    
    def report_winner(self, winner_num,board):
        pass
