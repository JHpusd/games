class MaiaHeuristicPlayer :
    def __init__(self) :
        self.number = None
        self.strat = HeuristicStrat()
    
    def set_player_number(self, n) :
        self.number = n
        self.strat.set_player_number(n)
    
    def choose_move(self, board, choices) :
        board = self.make_string(board)
        return self.strat.choose_move(board, choices)

    def make_string(self, board) :
        return [''.join([str(_) for _ in row]) for row in board]

    def transpose(self, board) :
        return [[board[row][col] for row in range(len(board))] for col in range(len(board[0]))]

    def transpose_str(self, board) :
        return [''.join([board[row][col] for row in range(len(board))] for col in range(len(board[0])))]


class HeuristicStrat :
    def __init__(self) :
        self.num = None
        self.tree = None
        self.layers = 6
  
    def set_player_number(self, n) :
        self.num = n
        self.tree = Con4Tree(n, self.layers)

    def choose_move(self, board, choices) :
        self.tree.prune_tree(board)
        best = (None, -1)

        for col in choices :
            update = board.copy()
            choice = self.find_row(board, col)
            update[choice[0]] = board[choice[0]][:choice[1]] + str(self.num) + board[choice[0]][choice[1]+1:]
            flatdate = self.tree.flaten_board(update)
            if self.tree.nodes[flatdate].score >= best[1] :
                best = (choice[1], self.tree.nodes[flatdate].score)
        return best[0]

    def find_row(self, board, col) :
        for row in range(5,-1,-1) :
            if board[row][col] == '0' :
                return (row, col)

class Node :
    def __init__(self, parent, player, game_state) :
        self.children = []
        self.player = player
        self.parent = [parent]
        self.score = None
        self.winner = self.check_for_winner(game_state)
    
    def check_for_winner(self, board) :
        rows = [board[row] for row in range(6)] #row
        cols = [''.join([board[row][col] for row in range(6)]) for col in range(7)]
        l_dias = []
        r_dias = []
        diagonals = [(3,0),(4,0),(5,0),(5,1),(5,2),(5,3)]
        for (row, col) in diagonals :
            i=0
            l_dia = []
            r_dia = []
            while row-i >=0 and col+i <= 6 :
                l_dia.append(board[row-i][col+i])
                r_dia.append(board[row-i][6-col-i])
                i+= 1
            l_dias.append(l_dia)
            r_dias.append(r_dia)
        
        thing = rows + cols + l_dias + r_dias

        tie = []

        for stuff in thing :
            tie.append('0' in stuff)
            if stuff.count('0') > len(stuff) - 4 :
                continue
            if '1111' in stuff :
                return 1
            elif '2222' in stuff :
                return 2

        if True not in tie:
            return 'Tie'

class Con4Tree :
    def __init__(self, max_plr, num_layers) :
        self.root = None
        self.layer_num = num_layers
        self.heuristic = self.heuristic_funct
        self.max_plr = max_plr
        self.leaf_nodes = [] 
        self.nodes = {}

    def heuristic_funct(self, board) :
        moves = self.get_possible_moves(self.flaten_board(board))
        rows = [board[row] for row in range(6)] #row
        rows_m = [[(row, col) for col in range (7)] for row in range(6)]
        cols = [''.join([board[row][col] for row in range(6)]) for col in range(7)]
        cols_m = [[(row,col) for row in range(6)] for col in range(7)]
        l_dias = []
        r_dias = []
        l_dias_m = []
        r_dias_m = []
        diagonals = [(3,0),(4,0),(5,0),(5,1),(5,2),(5,3)]
        for (row, col) in diagonals :
            i=0
            l_dia = []
            r_dia = []
            l_dia_m = []
            r_dia_m = []
            while row-i >=0 and col+i <= 6 :
                l_dia.append(board[row-i][col+i])
                r_dia.append(board[row-i][6-col-i])
                l_dia_m.append((row-1,col+i))
                r_dia_m.append((row-i,6-col-i))
                i+= 1
            l_dias.append(''.join(l_dia))
            r_dias.append(''.join(r_dia))
            l_dias_m.append(l_dia_m)
            r_dias_m.append(r_dia_m)
        
        thing = rows + cols + l_dias + r_dias
        thing_m = rows_m + cols_m + l_dias_m + r_dias_m

        good = 0
        bad = 0
        nmy = (self.max_plr % 2) + 1
        win = ''.join([str(self.max_plr) for _ in range(3)])
        lose = ''.join([str(nmy) for _ in range(3)])
        lose_2 = f"{nmy}0{nmy}{nmy}"
        lose_3 = f"{nmy}{nmy}0{nmy}"
        for index in range(len(thing)) :
            if set(thing_m[index]).isdisjoint(set(moves)):
                continue
            if win in thing[index] :
                good += 1
            elif lose in thing[index] or lose_2 in thing[index] or lose_3 in thing[index]:
                bad += 1
        return (good-bad)/len(thing)
    
    def find_turn(self, board) : 
        if board.count('1') == board.count('2') :
            return 1
        else :
            return 2

    def get_possible_moves(self, game_state) :
        if self.nodes[game_state].winner != None :
            return [[]]

        board = self.inflate_board(game_state)
        
        possible_moves = []
        
        cols = [[(row,col) for row in range(5,-1,-1)] for col in range(7)]
        for col in cols :
            for (row, col) in col :
                if board[row][col] == '0' :
                    possible_moves.append((row,col))
                    break
        return possible_moves     
    
    def create_nodes(self, start_board) :
        prev_choices = [start_board]
        curr_plr = self.find_turn(start_board)
        layer = 0
        while layer < self.layer_num and prev_choices != [] :
            choice = prev_choices[0]
            if self.find_turn(choice) != curr_plr :
                layer += 1
                curr_plr = self.find_turn(choice)
            if layer == self.layer_num :
                break
            prev_choices.remove(choice)

            possible_choices = self.get_possible_moves(choice)
            if [] in possible_choices :
                self.leaf_nodes.append(choice)
                continue

            if choice in self.nodes :
                prev_choices.extend(self.nodes[choice].children)
                if self.nodes[choice].children != [] :
                    continue

            update = []
            for (row, col) in possible_choices :
                new = self.inflate_board(choice)
                new[row] = new[row][:col] + str(curr_plr) + new[row][col+1:]
                update.append(new)

            for board in update :
                move = self.flaten_board(board)
                if move in self.nodes.keys() :
                    self.nodes[move].parent.append(choice)
                else :
                    prev_choices.append(move)
                    self.nodes[move] = Node(choice, (curr_plr%2) +1, board)
            
        self.leaf_nodes.extend(prev_choices)
        if len(set(self.leaf_nodes)) != len(self.leaf_nodes) :
            print("ERROR")

    def assign_values(self) :
        unassigned = self.leaf_nodes.copy()
        index = 0

        while len(unassigned) >= 1  :
            if index == len(unassigned) and unassigned != [] :
                index = 0

            node = self.nodes[unassigned[index]]
            unassigned.extend([parent for parent in node.parent if self.nodes[parent].score != 'root' and parent not in unassigned])

            child_scores = [self.nodes[child].score for child in node.children]
            if None in child_scores :
                index += 1
                continue
            
            if child_scores == [] :
                self.find_score(unassigned[index], node)
            elif node.player == self.max_plr :
                node.score = max(child_scores)
            else :
                node.score = min(child_scores)
            unassigned.pop(index)
    
    def find_score(self, board, node) :
        if node.winner != None :
            if node.winner == 'Tie' :
                node.score = 0
            elif node.winner == self.max_plr :
                node.score = 1
            else :
                node.score = -1
            return
        
        node.score = self.heuristic(self.inflate_board(board))

    def prune_tree(self, new_board) :
        self.leaf_nodes = []
        #print(board)
        self.root = self.flaten_board(new_board)
        if self.root not in self.nodes.keys() :
            self.nodes = {self.root: Node(None, self.find_turn(self.root), new_board)}
        self.nodes[self.root].score = 'root'
        self.create_nodes(self.root)
        self.assign_values()

    def flaten_board(self, board) :
        return ''.join(board)

    def inflate_board(self, board) :
        return [board[index:index+7] for index in range(0,41,7)]