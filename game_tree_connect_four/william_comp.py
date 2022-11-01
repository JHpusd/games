import sys
from copy import deepcopy


class WilliamHeuristicPlayer:
    def __init__(self, ply_num=5):
        self.number = None
        self.ply_num = ply_num


    def set_player_number(self, n):
        self.number = n
        self.tree = HeuristicTree(self.number)
        self.tree.construct_tree(self.tree.root.state, self.ply_num)
        self.tree.set_node_scores()

    def update_board(self, move, board):
        board = deepcopy(board)
        cols = self.get_cols(board)
        chosen_col = [*cols[move]]

        col_idx = len(chosen_col)-1 - list(reversed(chosen_col)).index(0)
        board[col_idx][move] = self.number
        return board

    def get_cols(self, board):
        cols = []

        for col_idx in range(len(board[0])):
            cols.append([row[col_idx] for row in board])

        return cols
    
    def convert_board(self, board):
        board = [[str(i) for i in row] for row in deepcopy(board)]
        new_board = []
        for row in board:
            new_board.append(''.join(row))
        return new_board

    def choose_move(self, board, possible_moves):    
        self.tree.construct_tree(self.convert_board(board.copy()), self.ply_num)
        self.tree.set_node_scores()
        best_move, best_move_idx = self.tree.list_to_string(self.convert_board(self.update_board(possible_moves[0], board))), possible_moves[0]

        for move in possible_moves:
            temp_board = self.tree.list_to_string(self.convert_board(self.update_board(move, board)))

            if self.tree.states[temp_board].score > self.tree.states[best_move].score:
                best_move, best_move_idx = temp_board, move

        return best_move_idx


class Node():
    def __init__(self, state, player):
        self.state = state
        self.turn = self.set_turn()
        self.player = player
        self.winner = self.check_winner()
        self.children = []
        self.parent = None
        self.score = None
    

    def set_turn(self):
        p1_count = 0
        p2_count = 0
        for row in self.state:
            p1_count += row.count('1')
            p2_count += row.count('2')
        if p1_count == p2_count:
            return 1
        else:
            return 2

    def set_score(self):
        state = self.string_to_list(self.state)
        if len(self.children) == 0:  
            if self.winner == self.player:
                self.score = 99999999
            elif self.winner == 3 - self.player:
                self.score = -99999999
            elif self.winner == 'tie':
                self.score = 0
            else:         
                row = self.three_in_list(state)
                col = self.three_in_list([''.join(i) for i in zip(*state)])
                diags = self.three_in_list(self.get_diags(state))
                
                total_threes = {i: row.get(i, 0) + col.get(i, 0) + diags.get(i, 0) for i in set(row).union(col).union(diags)}
                three_score = total_threes[self.player]-total_threes[3-self.player]
                
                row = self.two_in_list(state)
                col = self.two_in_list([''.join(i) for i in zip(*state)])
                diags = self.two_in_list(self.get_diags(state))

                total_twos = {i: row.get(i, 0) + col.get(i, 0) + diags.get(i, 0) for i in set(row).union(col).union(diags)}
                two_score = total_twos[self.player]-total_twos[3-self.player]
                
                self.score = 200*three_score+40*two_score

                if total_threes[self.player] > 0 and total_threes[3-self.player] == 0:
                    self.score = 99999
                elif total_threes[self.player] == 0 and total_threes[3-self.player] > 0:
                    self.score = -99999
            return

        if self.turn == self.player:
            self.score = max(self.get_children_scores())
        elif self.turn == 3 - self.player:
            self.score = min(self.get_children_scores())

    def get_children_scores(self):
        if len(self.children) == 0:
            return
        for child in self.children:
            child.set_score()
        return [child.score for child in self.children]

    def check_winner(self):
        state = self.string_to_list(self.state)
        if not any('0' in row for row in state):
            self.winner = 'tie'
        
        rows = self.four_in_list(state)
        if rows:
            self.winner = rows

        cols = self.four_in_list([''.join(i) for i in zip(*state)])
        if cols:
            self.winner = cols

        diag = self.four_in_list(self.get_diags(state))
        if diag:
            self.winner = diag
    
    def get_diags(self, state):
        fdiag = ['' for _ in range(len(state) + len(state[0]) - 1)]
        bdiag = ['' for _ in range(len(fdiag))]
        for x in range(len(state[0])):
            for y in range(len(state)):
                fdiag[x + y] += state[y][x]
                bdiag[x - y - (1 - len(state))] += state[y][x]
        return fdiag + bdiag
    
    def four_in_list(self, lst):
        for string in lst:
            for i in range(0, len(string)-3):
                if string[i] == string[i+1] == string[i+2] == string[i+3] != '0':
                    return string[i]
        return False
    
    def three_in_list(self, lst):
        totals = {1:0, 2:0}
        for string in lst:
            for i in range(0, len(string)-3):
                temp_str = string[i:i+4]
                str_set = set(temp_str)

                if temp_str.count('0') == 1 and len(str_set) == 2:
                    str_set.remove('0')
                    totals[int(list(str_set)[0])] += 1
        return totals

    def two_in_list(self, lst):
        totals = {1:0, 2:0}
        for string in lst:
            for i in range(0, len(string)-3):
                temp_str = string[i:i+4]
                str_set = set(temp_str)

                if temp_str.count('0') == 2 and len(str_set) == 2:
                    str_set.remove('0')
                    totals[int(list(str_set)[0])] += 1
        return totals
    
    def list_to_string(self, lst):
        temp_string = ''
        for s in lst:
            temp_string += s
        return temp_string

    def string_to_list(self, s):
        return [s[i:i+7] for i in range(0, len(s), 7)]
    
    def print_state(self, state):
        for line in state:
            print(' '.join(line))


class HeuristicTree():
    def __init__(self, player):
        self.root = Node('0'*42, player)
        self.player = player
        self.nodes = [self.root]
        self.leaf_nodes = []
        self.states = {self.root.state:self.root}


    def construct_tree(self, starting_node_state, n):
        starting_node_state = self.list_to_string(starting_node_state)
        try:
            starting_node = self.states[starting_node_state]
        except:
            starting_node = Node(starting_node_state, self.player)
            self.nodes.append(starting_node)
            self.states[starting_node_state] = starting_node
        
        self.root = starting_node

        ending_depth = self.calc_game_depth(starting_node.state) + n
        queue = [starting_node]
        while len(queue) != 0:
            current_node = queue[0]
            if self.calc_game_depth(current_node.state) >= ending_depth:
                queue.remove(current_node)
                continue
            if current_node.winner is None:
                moves = self.find_open_spaces(self.string_to_list(current_node.state))
                for move in moves:
                    state = current_node.state
                    new_state = self.update_board(state, move, current_node.turn)
                    if new_state in self.states:
                        new_node = self.states[new_state]
                    else:
                        new_node = Node(new_state, self.player)
                        self.nodes.append(new_node)
                        self.states[new_state] = new_node
                        queue.append(new_node)
                        
                    current_node.children.append(new_node)
                    new_node.parent = current_node
            else:
                self.leaf_nodes.append(current_node)
            queue.remove(current_node)

    def calc_game_depth(self, state):
        total = 0
        for row in state:
            total += row.count('0')
        return 42-total

    def set_node_scores(self):
        assert len(self.root.children) != 0, "create game tree before setting scores"
        self.root.set_score()
    
    def find_open_spaces(self, board):
        moves = []
        t_board = [''.join(i) for i in zip(*board)]
        for i, col in enumerate(t_board):
            if '0' in col:
                moves.append(i)
        return moves

    def update_board(self, board, index, value):
        board = self.string_to_list(board)
        cols = [''.join(i) for i in zip(*board)]
        chosen_col = [*cols[index]]

        col_idx = len(chosen_col)-1 - list(reversed(chosen_col)).index('0')
        row = board[col_idx]
        board[col_idx] = row[:index] + str(value) + row[index+1:]
        return self.list_to_string(board)
    
    def list_to_string(self, lst):
        temp_string = ''
        for s in lst:
            temp_string += s
        return temp_string

    def string_to_list(self, s):
        return [s[i:i+7] for i in range(0, len(s), 7)]