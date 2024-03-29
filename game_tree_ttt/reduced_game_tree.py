from game_nodes import *
import copy

class ReducedGameTree():
    def __init__(self, root_state, player_num):
        self.root = GameNode(root_state, 1, player_num)
        self.player = player_num
        self.current_nodes = [self.root] # for creating the game tree
        self.terminal_nodes = 0
        self.total_nodes = 1
        self.all_nodes = {str(root_state):self.root}
    
    def create_node_children(self, node):
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
            child = GameNode(board_copy, 3-turn, self.player)
            child.previous = [node]
            children.append(child)
            self.all_nodes[str(board_copy)] = child
            self.total_nodes += 1
            if child.winner != None:
                self.terminal_nodes += 1
        node.children = children

    def create_game_tree(self): # fix current nodes stuff
        if len(self.current_nodes) == 0:
            self.current_nodes = [self.root]
            return
        all_children = []
        for node in self.current_nodes:
            self.create_node_children(node)
            all_children += node.children
        self.current_nodes = set(all_children)
        self.create_game_tree()
    
    def set_node_scores(self):
        assert len(self.root.children) != 0, "create game tree before setting scores"
        self.root.set_score()
        return
    
    def get_move_from_boards(self, base_state, new_state):
        base_state_children = self.all_nodes[str(base_state)].children
        assert new_state in [child.state for child in base_state_children]

        for i in range(len(new_state)):
            for j in range(len(new_state[0])):
                base = base_state[i][j]
                new = new_state[i][j]
                if base != new:
                    return (i,j)
    
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