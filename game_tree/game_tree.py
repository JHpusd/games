import copy, time

class GameNode():
    def __init__(self, game_state, player_turn, player_num):
        self.state = game_state
        self.turn = player_turn
        self.player = player_num
        self.winner = self.check_for_winner()
        self.previous = None
        self.children = None
        self.score = None
        self.added_coord = None # for non-root nodes
    
    def get_row_col_diag(self):
        rows = list(self.state)
        cols = [[self.state[i][j] for i in range(3)] for j in range(3)]
        diag_1 = [self.state[i][i] for i in range(3)]
        diag_2 = [self.state[i][2-i] for i in range(3)]
        diags = [diag_1, diag_2]
        return rows + cols + diags
    
    def check_for_winner(self):
        rcd = self.get_row_col_diag()
        valid_rcd = [item for item in rcd if None not in item]
        for item in valid_rcd:
            if len(set(item)) == 1:
                return item[0]
        if valid_rcd == rcd:
            return "Tie"
        return None
    
    def children_to_score(self):
        if self.children == None:
            return None
        for child in self.children:
            child.set_score()
        return [child.score for child in self.children]
    
    def set_score(self):
        if self.children == None:
            if self.winner == self.player:
                self.score = 1
            elif self.winner == 3 - self.player:
                self.score = -1
            elif self.winner == 'Tie':
                self.score = 0
            return

        if self.turn == self.player:
            self.score = max(self.children_to_score())
        elif self.turn == 3 - self.player:
            self.score = min(self.children_to_score())

class CanonGameTree():
    def __init__(self, root_state, player_num):
        self.root = GameNode(root_state, 1, player_num)
        self.player = player_num
        self.current_nodes = [self.root] # for creating the game tree
        self.total_nodes = 1
        self.terminal_nodes = 0
    
    def create_node_children(self, node):
        if node.winner != None or node.children != None:
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
            if node.children != None:
                all_children += node.children
                self.total_nodes += len(node.children)
            else:
                self.terminal_nodes += 1
        self.current_nodes = all_children
        self.create_game_tree()
    
    def set_node_scores(self):
        assert self.root.children != None, "create game tree before setting scores"
        self.root.set_score()
        return
    
    def get_best_move(self):
        scores = [node.score for node in self.root.children]
        max_index = scores.index(max(scores))
        best_result = self.root.children[max_index]
        return best_result.added_coord

class ReducedGameTree():
    def __init__(self, root_state, player_num):
        self.root = GameNode(root_state, 1, player_num)
        self.player = player_num
        self.current_nodes = [self.root] # for creating the game tree
        self.terminal_nodes = 0
        self.all_nodes = {str(root_state):self.root}
    
    def create_node_children(self, node):
        if node.winner != None or node.children != None:
            return
        board = node.state
        turn = node.turn
        children = []
        options = [(i,j) for i in range(len(board)) for j in range(len(board)) if board[i][j] == None]
        for option in options:
            board_copy = copy.deepcopy(board)
            board_copy[option[0]][option[1]] = turn
            if str(board_copy) in list(self.all_nodes.keys()):
                self.all_nodes[str(board_copy)].previous.append(node)
                continue
            child = GameNode(board_copy, 3-turn, self.player)
            child.added_coord = option
            child.previous = [node]
            children.append(child)
            self.all_nodes[str(board_copy)] = child
        node.children = children

    def create_game_tree(self):
        if len(self.current_nodes) == 0:
            self.current_nodes = [self.root]
            return
        all_children = []
        for node in self.current_nodes:
            child_boards = self.create_node_children(node)
            if node.children != None:
                all_children += node.children
            else:
                self.terminal_nodes += 1
        self.current_nodes = all_children
        self.create_game_tree()
    
    def set_node_scores(self):
        assert self.root.children != None, "create game tree before setting scores"
        self.root.set_score()
        return
    
    def get_best_move(self):
        scores = [node.score for node in self.root.children]
        max_index = scores.index(max(scores))
        best_result = self.root.children[max_index]
        return best_result.added_coord

def flatten(input_list):
    result = []
    for collection in input_list:
        result += collection
    return result
'''
root_state = [[None for _ in range(3)] for _ in range(3)]

print('starting canonical game tree test')
start = time.time()
cgt = CanonGameTree(root_state, 1)
cgt.create_game_tree()
print(cgt.terminal_nodes)
end = time.time()
print(f'finished canonical game tree test, time: {end-start}')

print('starting reduced game tree test')
start = time.time()
rgt = ReducedGameTree(root_state, 1)
rgt.create_game_tree()
print(len(list(rgt.all_nodes.keys())))
end = time.time()
print(f'finished reduced game tree test, time: {end-start}')
'''