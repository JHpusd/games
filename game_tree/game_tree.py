import copy, time

class GameNode():
    def __init__(self, game_state, player_turn, player_num):
        self.state = game_state
        self.turn = player_turn
        self.player = player_num
        self.winner = self.check_for_winner()
        self.previous = []
        self.children = []
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
        if self.children == None or len(self.children) == 0:
            return None
        for child in self.children:
            child.set_score()
        return [child.score for child in self.children]
    
    def set_score(self):
        if self.children == None or len(self.children) == 0:
            if self.winner == self.player:
                self.score = 1
            elif self.winner == 3 - self.player:
                self.score = -1
            elif self.winner == 'Tie':
                self.score = 0
            return

        #print([child.state for child in self.children])
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

class ReducedGameTree():
    def __init__(self, root_state, player_num):
        self.root = GameNode(root_state, 1, player_num)
        self.player = player_num
        self.current_nodes = [self.root] # for creating the game tree
        self.terminal_nodes = 0
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
        node.children = children

    def create_game_tree(self):
        if len(self.current_nodes) == 0:
            self.current_nodes = [self.root]w
            return
        all_children = []
        for node in self.current_nodes:
            child_boards = self.create_node_children(node)
            if len(node.children) != 0:
                all_children += node.children
            else:
                self.terminal_nodes += 1
        self.current_nodes = all_children
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

'''
root_state = [[None for _ in range(3)] for _ in range(3)]

print('starting canonical game tree test')
start = time.time()
cgt = CanonGameTree(root_state, 1)
cgt.create_game_tree()
print(cgt.terminal_nodes)
end = time.time()
print(f'finished canonical game tree test, time: {end-start}')

rgt = ReducedGameTree(root_state, 1)
rgt.create_game_tree()
print(len(list(rgt.all_nodes.keys())))

item = [[1, 2, 1], [2, None, 1], [2, 1, 2]]
new_item = [[1, 2, 1], [2, 1, 1], [2, 1, 2]]
node = rgt.all_nodes[str(item)]
print(rgt.get_move_from_boards(item, new_item))
'''