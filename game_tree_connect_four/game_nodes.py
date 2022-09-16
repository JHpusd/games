
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
    
    def transpose(self, board=None):
        if board == None:
            board = self.state
        t_board = []
        for i in range(len(board[0])):
            t_row = []
            for arr in board:
                t_row.append(arr[i])
            t_board.append(t_row)
        return t_board
    
    def arr_add(self, arr_1, arr_2):
        assert len(arr_1) == len(arr_2), 'different len arrays'
        result = []
        for i in range(len(arr_1)):
            result.append(arr_1[i] + arr_2[i])
        return result
    
    def coords_to_elem(self, coords):
        if type(coords)!=list:
            coords = [coords]
        elems = []
        for coord in coords:
            elems.append(self.state[coord[0]][coord[1]])
        return elems
    
    def get_diags(self):
        coords = [[0,i] for i in range(7)]+[[5,2],[5,3],[5,4]]
        diags = []
        for coord in coords:
            coord_diags = []
            dummy = list(coord)
            options = [[1,1], [1,-1],[-1,1],[-1,-1]]
            for option in options:
                diag = []
                while dummy[0]>=0 and dummy[0]<6 and dummy[1]>=0 and dummy[1]<7:
                    diag.append(dummy)
                    dummy = self.arr_add(dummy, option)
                if len(diag) > 3:
                    coord_diags.append(diag)
                dummy = list(coord)
            dummy = list(coord)
            diags += coord_diags
        
        diag_elems = []
        for diag in diags:
            diag_elems.append(self.coords_to_elem(diag))
        
        return diag_elems
    
    def check_len_four(self, arr):
        for i,val in enumerate(arr[:-3]):
            if val == 0:
                continue
            len_four = arr[i:i+4]
            if len(set(len_four)) == 1:
                return val
    
    def check_for_winner(self):
        rows = self.state
        cols = self.transpose()
        diags = self.get_diags()
        rcd = rows + cols + diags

        for arr in rcd:
            winner = self.check_len_four(arr)
            if winner != None:
                self.winner = winner
                return winner
        if 0 not in [item for item in arr for arr in rcd]:
            return 'Tie'
    
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
            else:
                self.score = self.func(self.state, self.player, self.turn)
            return

        #print([child.state for child in self.children])
        if self.turn == self.player:
            self.score = max(self.children_to_score())
        elif self.turn == 3 - self.player:
            self.score = min(self.children_to_score())