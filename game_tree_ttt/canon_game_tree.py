from game_nodes import *

class CanonGameTree():
    def __init__(self, root_state, player_num):
        self.root = GameNode(root_state, 1, player_num)
        self.player = player_num
        self.current_nodes = [self.root] # for creating the game tree
        self.total_nodes = 1
        self.terminal_nodes = 0
    
    def create_node_children(self, node):
        if node.winner != None or len(node.children) != 0:
            return
        board = node.state
        turn = node.turn
        children = []
        child_boards = []
        options = [(i,j) for i in range(len(board)) for j in range(len(board)) if board[i][j] == None]
        for option in options:
            board_copy = copy.deepcopy(board)
            board_copy[option[0]][option[1]] = turn
            child_boards.append(board_copy)
            child = GameNode(board_copy, 3-turn, self.player)
            child.added_coord = option
            child.previous = [node]
            children.append(child)
        node.children = children
        return board_copy

    def create_game_tree(self):
        if len(self.current_nodes) == 0:
            self.current_nodes = [self.root]
            return
        all_children = []
        for node in self.current_nodes:
            child_boards = self.create_node_children(node)
            if len(node.children) != 0:
                all_children += node.children
                self.total_nodes += len(node.children)
            else:
                self.terminal_nodes += 1
        self.current_nodes = all_children
        self.create_game_tree()
    
    def set_node_scores(self):
        assert len(self.root.children) != 0, "create game tree before setting scores"
        self.root.set_score()
        return
    
    def get_best_move(self):
        scores = [node.score for node in self.root.children]
        max_index = scores.index(max(scores))
        best_result = self.root.children[max_index]
        return best_result.added_coord
