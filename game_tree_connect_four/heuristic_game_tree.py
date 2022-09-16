from game_nodes import *
import copy

class HeuristicGameTree():
    def __init__(self, root_state, player_num, h_func, ply):
        self.root = HeuristicGameNode(root_state, 1, player_num, h_func)
        self.player = player_num
        self.current_nodes = [self.root] # for creating the game tree
        self.terminal_nodes = 0
        self.total_nodes = 1
        self.all_nodes = {str(root_state):self.root}
        self.func = h_func
        self.ply = ply
    
    def create_node_children(self, node): # make this work for c4
        if node.winner != None or len(node.children) != 0:
            return
        board = node.state
        turn = node.turn
        children = []
        options = [(i,j) for i in range(len(board)) for j in range(len(board)) if board[i][j] == None]
        for option in options:
            board_copy = copy.deepcopy(board)
            board_copy[option[0]][option[1]] = turn
            if str(board_copy) in list(self.all_nodes.keys()):
                children.append(self.all_nodes[str(board_copy)])
                self.all_nodes[str(board_copy)].previous.append(node)
                continue
            child = HeuristicGameNode(board_copy, 3-turn, self.player, self.func)
            child.previous = [node]
            children.append(child)
            self.all_nodes[str(board_copy)] = child
            self.total_nodes += 1
            if child.winner != None:
                self.terminal_nodes += 1
        node.children = children
    
    def prune(self): # done after new root is set by player
        current = [self.root]
        next_layer = self.root.children
        for _ in range(self.ply - 3):
            current = next_layer
            next_layer = []
            for node in current:
                next_layer += node.children
        self.current_nodes = next_layer

    def init_create_game_tree(self):
        for _ in range(self.ply):
            if len(self.current_nodes) == 0:
                self.current_nodes = [self.root]
                return
            all_children = []
            for node in self.current_nodes:
                self.create_node_children(node)
                all_children += node.children
    
    def extend_game_tree(self): # only run after pruning
        all_children = []
        for node in self.current_nodes:
            self.create_node_children(node)
            all_children += node.children
        self.current_nodes = set(all_children)
    
    def set_node_scores(self):
        assert len(self.root.children) != 0, "create game tree before setting scores"
        self.root.set_score()
    
    def transpose(self, board):
        t_board = []
        for i in range(len(board[0])):
            t_row = []
            for arr in board:
                t_row.append(arr[i])
            t_board.append(t_row)
        return t_board

    def get_move_from_boards(self, base_state, new_state):
        base_state_children = self.all_nodes[str(base_state)].children
        assert new_state in [child.state for child in base_state_children]

        base_cols = self.transpose(base_state)
        new_cols = self.transpose(new_state)
        for i in range(len(base_cols)):
            if base_cols[i] != new_cols[i]:
                return i+1
    
    def get_best_move(self):
        base_state = self.root.state
        scores = [node.score for node in self.root.children]
        max_index = scores.index(max(scores))
        best_move_node = self.root.children[max_index]
        new_state = best_move_node.state
        return self.get_move_from_boards(base_state, new_state)

    def flatten(self, input_list):
        result = []
        for collection in input_list:
            result += collection
        return result