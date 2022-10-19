import copy

class HeuristicGameNode():
    def __init__(self, game_state, player_turn, player_num):
        self.state = game_state
        self.turn = player_turn
        self.player = player_num
        self.winner = self.check_for_winner()
        self.previous = []
        self.children = []
        self.score = None
    
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
    
    def get_diags(self, state=None):
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
        
        return [diag_elems, diags]
    
    def check_len_four(self, arr):
        for i,val in enumerate(arr[:-3]):
            if val == 0:
                continue
            len_four = arr[i:i+4]
            if len(set(len_four)) == 1:
                return val
    
    def get_options(self):
        col_board = self.transpose()
        return [i for i,col in enumerate(col_board) if 0 in col]
    
    def check_for_winner(self):
        rows = self.state
        cols = self.transpose()
        diags = self.get_diags()[0]
        rcd = rows + cols + diags

        for arr in rcd:
            winner = self.check_len_four(arr)
            if winner != None:
                self.winner = winner
                return winner
        if 0 not in self.flatten(rcd):
            return 'Tie'
    
    def flatten(self, nested_arrs):
        flat_arr = []
        for arr in nested_arrs:
            for item in arr:
                flat_arr.append(item)
        return flat_arr
    
    def children_to_score(self):
        if self.children == None or len(self.children) == 0:
            return None
        for child in self.children:
            child.set_score()
        return [child.score for child in self.children]
    
    def set_score(self):
        if self.children == None or len(self.children) == 0:
            if self.winner == self.player:
                self.score = 9999
            elif self.winner == 3 - self.player:
                self.score = -9999
            elif self.winner == 'Tie':
                self.score = 0
            else:
                self.score = self.heuristic_func()
            return

        #print([child.state for child in self.children])
        if self.turn == self.player:
            self.score = max(self.children_to_score())
        elif self.turn == 3 - self.player:
            self.score = min(self.children_to_score())
    
    def print_board(self):
        for i in range(len(self.state)):
            row = self.state[i]
            row_string = ''
            for space in row:
                if space == None:
                    row_string += '_|'
                else:
                    row_string += str(space) + '|'
            print(row_string[:-1])
        print('\n')
    
    # includes target coord
    def three_in_four(self, arr): # ex. 0 1 1 0 1 0 -> 1
        for i,val in enumerate(arr[:-3]):
            len_four = arr[i:i+4]
            if len_four.count(1)==3 and 0 in len_four:
                return (1, i+len_four.index(0))
            elif len_four.count(2)==3 and 0 in len_four:
                return (2, i+len_four.index(0))

    # does not include target coord
    def two_in_four(self, arr):
        for i,val in enumerate(arr[:-3]):
            len_four = arr[i:i+4]
            if len_four.count(1)==2 and len_four.count(0)==2:
                return 1
            elif len_four.count(2)==2 and len_four.count(0)==2:
                return 2

    # includes target coord(s)
    def open_ended_three(self, arr):
        for i,val in enumerate(arr[:-4]):
            len_five = arr[i:i+5]
            if len_five[1]==0:
                continue
            if len(set(len_five[1:-1]))==1 and len_five.count(0)==2:
                return (len_five[1], [i,i+4])

    def heuristic_func(self):
        # wins and ties caught by tree, no need to check here
        game_state = self.state
        rows = game_state
        cols = self.transpose(game_state)
        diags = self.get_diags()
        diag_elems = diags[0]
        diag_coords = diags[1]
        #rcd = rows + cols + diags 

        open_threes = {self.player:0, 3-self.player:0} # only in diags and rows
        threat_threes = {self.player:0, 3-self.player:0} # three where opening is movable
        # make win/loss next turn true at the end if threat_threes >= 2
        threat_coords = {self.player:[], 3-self.player:[]}
        threes = {self.player:0, 3-self.player:0}
        twos = {self.player:0, 3-self.player:0}
        advantage = 0
        if self.player == self.turn:
            advantage += 1
        elif self.player == 3-self.turn:
            advantage -= 1
        
        # if there is a win chance for turn player, score as win/loss - includes open ended
        # if there is open three, imminent loss/win 

        for i,row in enumerate(rows):
            potential = self.three_in_four(row)
            open_three = self.open_ended_three(row)
            if self.two_in_four(row) != None:
                twos[self.two_in_four(row)] += 1
            if potential != None:
                threes[potential[0]] += 1
                coord = (i,potential[1])
                if i == 5 or self.state[i+1][potential[1]] != 0: # if opening is movable
                    if potential[0] == self.turn:
                        if self.turn == self.player:
                            return 1000
                        if self.turn == 3-self.player:
                            return -1000
                    if coord not in threat_coords[potential[0]]:
                        threat_threes[potential[0]] += 1
                        threat_coords[potential[0]].append(coord)
            if open_three != None:
                open_threes[open_three[0]] += 1
                col_idxs = open_three[1]
                coords = [(i,col_idx) for col_idx in col_idxs]
                for coord in coords:
                    if i == 5 or self.state[coord[0]+1][coord[1]] != 0:
                        if coord not in threat_coords[open_three[0]]:
                            threat_threes[open_three[0]] += 1
                            threat_coords[open_three[0]].append(coord)
        
        for i,col in enumerate(cols):
            potential = self.three_in_four(col)
            if self.two_in_four(col) != None:
                twos[self.two_in_four(col)] += 1
            if potential != None:
                threes[potential[0]] += 1
                coord = (potential[1],i)
                if potential[0] == self.turn:
                    if self.turn == self.player:
                        return 1000
                    if self.turn == 3-self.player:
                        return -1000
                if coord not in threat_coords[potential[0]]:
                    threat_threes[potential[0]] += 1
                    threat_coords[potential[0]].append(coord)
        
        for i,diag in enumerate(diag_elems):
            potential = self.three_in_four(diag)
            open_three = self.open_ended_three(diag)
            if self.two_in_four(diag):
                twos[self.two_in_four(diag)] += 1
            if potential != None:
                threes[potential[0]] += 1
                coord = diag_coords[i][potential[1]]
                if coord[0] == 5 or self.state[coord[0]+1][coord[1]] != 0:
                    if potential == self.turn:
                        if self.turn == self.player:
                            return 1000
                        if self.turn == 3-self.player:
                            return -1000
                    if coord not in threat_coords[potential[0]]:
                        threat_threes[potential[0]] += 1
                        threat_coords[potential[0]].append(coord)
            if open_three != None:
                open_threes[open_three[0]] += 1
                coords = [diag_coords[i][col_idx] for col_idx in open_three[1]]
                for coord in coords:
                    if coord[0] == 5 or self.state[coord[0]+1][coord[1]] != 0:
                        if coord not in threat_coords[potential[0]]:
                            threat_threes[potential[0]] += 1
                            threat_coords[potential[0]].append(threat_coords)

        if threat_threes[self.player] >= 2:
            return 1000
        if threat_threes[3-self.player] >= 2:
            return -1000
        
        advantage += twos[self.player]-twos[3-self.player]
        advantage += 3*(threes[self.player]-threes[3-self.player])
        advantage += 6*(open_threes[self.player]-open_threes[3-self.player])
        return advantage


class HeuristicGameTree():
    def __init__(self, root_state, player_num, ply):
        self.root = HeuristicGameNode(root_state, 1, player_num)
        self.player = player_num
        self.current_nodes = [self.root] # for creating the game tree
        self.terminal_nodes = 0
        self.total_nodes = 1
        self.all_nodes = {str(root_state):self.root}
        self.ply = ply
    
    def new_board(self, board, player_num, move_index):
        col_board = self.transpose(board)
        col = col_board[move_index]
        i_r = col[::-1].index(0)
        col[len(col)-1-i_r] = player_num
        return self.transpose(col_board)
    
    def create_node_children(self, node): # make this work for c4
        if node.winner != None or len(node.children) != 0:
            return
        board = node.state
        turn = node.turn
        children = []
        options = node.get_options()
        for option in options:
            board_copy = copy.deepcopy(board)
            board_copy = self.new_board(board_copy, turn, option)
            if str(board_copy) in list(self.all_nodes.keys()):
                children.append(self.all_nodes[str(board_copy)])
                self.all_nodes[str(board_copy)].previous.append(node)
                continue
            child = HeuristicGameNode(board_copy, 3-turn, self.player)
            child.previous = [node]
            children.append(child)
            self.all_nodes[str(board_copy)] = child
            self.total_nodes += 1
            if child.winner != None:
                self.terminal_nodes += 1
        node.children = children
    
    def prune(self): # done after new root is set by player
        current = [self.root]
        next_layer = []
        for _ in range(self.ply - 2):
            for node in current:
                next_layer += node.children
            current = set(next_layer)
            next_layer = []
        self.current_nodes = current

    def init_create_game_tree(self):
        for i in range(self.ply):
            if len(self.current_nodes) == 0:
                self.current_nodes = [self.root]
                return
            all_children = []
            for node in self.current_nodes:
                self.create_node_children(node)
                all_children += node.children
            self.current_nodes = set(all_children)
            #print(f'layer {i+1} has {len(self.current_nodes)} nodes')
    
    def extend_game_tree(self): # only run after pruning
        for _ in range(2):
            all_children = []
            for node in self.current_nodes:
                self.create_node_children(node)
                all_children += node.children
            self.current_nodes = set(all_children)
        #print(f'extended layer has {len(self.current_nodes)} nodes')
    
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
                return i
    
    def get_best_move(self):
        base_state = self.root.state
        scores = [node.score for node in self.root.children]
        max_index = scores.index(max(scores))
        #print(f'max score index: {max_index}')
        best_move_node = self.root.children[max_index]
        new_state = best_move_node.state
        return self.get_move_from_boards(base_state, new_state)

    def flatten(self, input_list):
        result = []
        for collection in input_list:
            result += collection
        return result

class HeuristicPlayer():
    def __init__(self, ply):
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
