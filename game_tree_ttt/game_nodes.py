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

class HeuristicGameNode():
    def __init__(self, game_state, player_turn, player_num, h_func):
        self.state = game_state
        self.turn = player_turn
        self.player = player_num
        self.winner = self.check_for_winner()
        self.previous = []
        self.children = []
        self.score = None
        self.added_coord = None # for non-root nodes
        self.func = h_func
    
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
                self.score = 
            elif self.winner == 3 - self.player:
                self.score = -1
            elif self.winner == 'Tie':
                self.score = 0
            else:
                self.score = self.func(self.state, self.player)
            return

        #print([child.state for child in self.children])
        if self.turn == self.player:
            self.score = max(self.children_to_score())
        elif self.turn == 3 - self.player:
            self.score = min(self.children_to_score())