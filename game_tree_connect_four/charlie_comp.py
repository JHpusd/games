import copy, random

# Node class

class CharlieNode():
    
    def __init__(self, state, player_turn, number, depth):
        
        self.state = state
        self.player_turn = player_turn
        self.number = number
        self.depth = depth

        self.winner = check_for_winner(self.state)
        self.parents = []
        self.children = []
        self.score = None
    
    def set_score(self):
        
        if self.children == None or len(self.children) == 0:
        
            self.winner = check_for_winner(self.state)

            if self.winner:

                if self.winner == self.number:
                    self.score = 1
                elif self.winner == 3 - self.number:
                    self.score = -1
                elif self.winner == 'tie':
                    self.score = 0
            
            else:
            
                score = 0
                combinations = get_combinations(self.state)

                for row in combinations:
                    if row.count(self.number) == 3 and row.count(None) == 1:
                        score += 1
                    if row.count(3 - self.number) == 3 and row.count(None) == 1:
                        score -= 1
                
                self.score = score / len(combinations)

                if self.score > 0:
                    self.winner = self.number
                elif self.score < 0:
                    self.winner = 3 - self.number
                elif self.score == 0:
                    self.winner = 'tie'

        else:
            
            for child in self.children:
                child.set_score()
            
            child_scores = [child.score for child in self.children]

            if self.player_turn == self.number:
                self.score = max(child_scores)
            elif self.player_turn == 3 - self.number:
                self.score = min(child_scores)

# Game Tree

class CharlieGameTree():
    
    def __init__(self, root_state, number, ply):
        self.root = CharlieNode(root_state, 1, number, 0)
        self.number = number
        self.current_nodes = [self.root]
        self.all_nodes = {str(self.root.state):self.root}
        self.ply = ply
    
    def create_node_children(self, node):

        if (node.winner == None or node.depth + 1 == self.ply) and len(node.children) == 0:
        
            children = []

            for move in get_moves(node.state):

                state_copy = copy.deepcopy(node.state)
                update_state(state_copy, move, node.player_turn)

                if str(state_copy) not in list(self.all_nodes.keys()):
                    self.all_nodes[str(state_copy)] = CharlieNode(state_copy, 3 - node.player_turn, self.number, node.depth + 1)
                
                child = self.all_nodes[str(state_copy)]
                child.parents.append(node)
                children.append(child)

            node.children = children
        
        for child in node.children:
            child.depth = node.depth + 1

    def build_tree(self):
        
        if len(self.current_nodes) == 0 or self.current_nodes[0].depth == self.ply:
            return
        
        all_children = []
        for node in self.current_nodes:
            self.create_node_children(node)
            all_children += node.children
        
        self.current_nodes = all_children
        self.build_tree()

# last minute player

class CharlieLMP:
    
    def __init__(self):
        self.number = None
  
    def set_number(self, n):
        self.number = n

    def choose_move(self, state, moves):
        
        for move in moves:

            capture_win_state = copy.deepcopy(state)
            block_loss_state = copy.deepcopy(state)

            for i in range(5, -1, -1):
                if state[i][move] == None:
                    capture_win_state[i][move] = self.number
                    block_loss_state[i][move] = 3 - self.number
                    break

            if check_for_winner(capture_win_state) or check_for_winner(block_loss_state):
                return move

        return random.choice(moves)

    def update_state(self, state):
        pass

# heuristic player

class CharlieHeuristicPlayer():
    
    def __init__(self):
        self.number = None
        self.ply = 4
    
    def set_player_number(self, number):
        self.number = number
        self.game = CharlieGameTree([[None for _ in range(7)] for _ in range(6)], self.number, self.ply)
        self.game.build_tree()
        self.game.root.set_score()

    def choose_move(self, state, moves):
        
        for node in self.game.root.children:
            if node.score == max(node.score for node in self.game.root.children):  
                
                for move in get_moves(self.game.root.state):
                    for i in range(5, -1, -1):
                        if self.game.root.state[i][move] != node.state[i][move]:
                            return move
        
    def update_state(self, state):

        for child in self.game.root.children:
            if child.state == state:

                self.game.root = child
                self.game.root.depth = 0
                
                self.game.number = self.number
                self.game.current_nodes = [self.game.root]
                self.game.all_nodes = {str(state):self.game.root}
                
                self.game.build_tree()
                self.game.root.set_score()
                
                break

# helper functions

def get_combinations(state):
    
    four_in_a_row = []

    for i in range(6):
        for j in range(4):
            row = [state[i][j + k] for k in range(4)]
            four_in_a_row.append(row)

    for i in range(3):
        for j in range(7):
            column = [state[i + k][j] for k in range(4)]
            four_in_a_row.append(column)
    
    for i in range(3):
        for j in range(4):
            forward_diag = [state[i + k][j + k] for k in range(4)]
            four_in_a_row.append(forward_diag)
    
    for i in range(3):
        for j in range(3, 7):
            backward_diag = [state[i + k][j - k] for k in range(4)]
            four_in_a_row.append(backward_diag)
    
    return four_in_a_row

def check_for_winner(state):

    board_full = True
    for row in get_combinations(state):
        
        if None in row:
            board_full = False

        if len(set(row)) == 1 and row[0] != None:
            return row[0]
    
    return 'tie' if board_full else None

def print_board(state):
    print('')
    for row in state:
        row_string = ''
        for space in row:
            if space == None:
                row_string += '_ '
            else:
                row_string += str(space) + ' '
        print(row_string[:-1])
    print('')

def get_moves(state):

    moves = []

    for row in state:
        for i, space in enumerate(row):
            if space == None:
                moves.append(i)
    
    return list(set(moves))

def update_state(state, move, number):

    for i in range(5, -1, -1):
        if state[i][move] == None:
            state[i][move] = number
            return