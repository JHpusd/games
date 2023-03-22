from tree_nodes import *
from score_nn import *
import copy

class ReducedGameTree():
    def __init__(self, root_state, player_num, scoring_nn, ply):
        self.root = TreeNode(root_state, 1, player_num, scoring_nn)
        self.player = player_num
        self.net = scoring_nn
        self.ply = ply
        self.current_nodes = [self.root] # for creating the game tree
        self.terminal_nodes = 0
        self.total_nodes = 1
        self.all_nodes = {str(root_state):self.root}
    
    def print_board(self, board):
        print("\n   0 1 2 3 4 5 6 7")
        for i in range(8):
            row_to_print = f"{i} "
            for j in range(8):
                elem = board[i][j]
                if elem == 0:  row_to_print += "⬜" if ((i + j) % 2 == 0) else "  "
                if elem == 1:  row_to_print += "🔵"
                if elem == 2:  row_to_print += "🔴"
                if elem == -1: row_to_print += "💙"
                if elem == -2: row_to_print += "❤️ "
            print(row_to_print)
    
    def arr_add(self, arr_1, arr_2):
        return [arr_1[i] + arr_2[i] for i in range(len(arr_1))]

    def nested_list_in_list(self, parent_list, nested_list):
        for l in parent_list:
            if all(x == y for x, y in zip(l, nested_list)):
                return True
        return False

    def add_moves_to_check(self, current_piece, current_coords, captured_coords, moves_to_check):
        
        direction = 1 - 2*(current_piece % 2)

        moves_to_check.append([current_coords, [direction, -1], captured_coords])
        moves_to_check.append([current_coords, [direction, 1], captured_coords])

        if current_piece < 0:
            moves_to_check.append([current_coords, [-direction, -1], captured_coords])
            moves_to_check.append([current_coords, [-direction, 1], captured_coords])
        
        return moves_to_check
    
    def find_translation(self, coord1, coord2):
        return [coord1[0] - coord2[0], coord1[1] - coord2[1]]
    
    def get_all_moves(self, player, state=None):
        player_num = player
        if type(player) != int:
            player_num = player.player_num
        
        if state == None: state = self.board

        possible_moves = []

        # loop through all coordinates

        for i in range(8):
            for j in range(8):

                current_coords = [i, j]
                current_piece = state[i][j]

                # check if there is a piece on the current coord

                if abs(current_piece) == player_num:

                    # get moves that the piece might be able to do

                    moves_to_check = self.add_moves_to_check(current_piece, current_coords, [], [])

                    while len(moves_to_check) > 0:

                        # check first move in moves_to_check

                        move_to_check = moves_to_check.pop(0) # moves_to_check is a queue
                        coord, translation_to_check, captured_coords = move_to_check

                        new_i, new_j = self.arr_add(coord, translation_to_check)
                        if new_i < 0 or new_i > 7 or new_j < 0 or new_j > 7: continue
                        new_piece = state[new_i][new_j]

                        # check if the new spot is empty

                        if abs(new_piece) == 0 and captured_coords == []:
                            possible_moves.append(move_to_check)
                    
                        # check if the opponent is in the new spot

                        elif abs(new_piece) == 3 - player_num:
                            
                            # if so, and if the next next spot is empty, add that spot to moves_to_check

                            next_translation = [2*t for t in translation_to_check]
                            new_new_i, new_new_j = self.arr_add(coord, next_translation)
                            if new_new_i < 0 or new_new_i > 7 or new_new_j < 0 or new_new_j > 7: continue
                            new_new_piece = state[new_new_i][new_new_j]

                            if abs(new_new_piece) == 0 and not self.nested_list_in_list(captured_coords, [new_i, new_j]):

                                # add capture to possible moves

                                previous_translation = self.find_translation(coord, current_coords)
                                new_translation = self.arr_add(previous_translation, next_translation)
                                new_captured_coords = captured_coords + [[new_i, new_j]]
                                possible_moves.append([current_coords, new_translation, new_captured_coords])

                                # add potential to combo captures

                                next_next_coords = self.arr_add(current_coords, new_translation)
                                moves_to_check = self.add_moves_to_check(current_piece, next_next_coords, new_captured_coords, moves_to_check)

                                # then, it'll loop back to the start of moves_to_check
        
        return possible_moves
    
    def coord_val(self, board, coord):
        if coord[0] < 0 or coord[1] < 0:
            return None
        try:
            return board[coord[0]][coord[1]]
        except:
            return None
    
    def del_captured_pieces(self, board, capt_move):
        for capt_coord in capt_move[2]:
            board[capt_coord[0]][capt_coord[1]] = 0

    def check_promotions(self, board):
        top_row = board[0]
        bottom_row = board[7]
        for i, item in enumerate(top_row):
            if item == 1:
                board[0][i] = -1
        for i, item in enumerate(bottom_row):
            if item == 2:
                board[7][i] = -2
    
    def make_move(self, board, move):
        new_board = copy.deepcopy(board)
        self.del_captured_pieces(new_board, move)

        coord = move[0]
        coord_val = self.coord_val(board, coord)
        new_coord = self.arr_add(coord,move[1])
        new_board[new_coord[0]][new_coord[1]] = coord_val
        new_board[coord[0]][coord[1]] = 0
        self.check_promotions(new_board)
        return new_board
    
    def create_node_children(self, node):
        if node.winner != None or len(node.children) != 0:
            return
        board = node.board
        turn = node.turn
        children = []
        options = self.get_all_moves(turn, board)
        for option in options:
            new_board = self.make_move(board, option)
            if str(new_board) in list(self.all_nodes.keys()):
                children.append(self.all_nodes[str(new_board)])
                self.all_nodes[str(new_board)].previous.append(node)
                continue
            child = TreeNode(new_board, 3-turn, self.player, self.net)
            child.previous = [node]
            children.append(child)
            self.all_nodes[str(new_board)] = child
            self.total_nodes += 1
            if child.winner != None:
                self.terminal_nodes += 1
        node.children = children

    def init_create_game_tree(self): 
        for _ in range(self.ply):
            if len(self.current_nodes) == 0:
                self.current_nodes = [self.root]
                return
            all_children = []
            for node in self.current_nodes:
                self.create_node_children(node)
                all_children += node.children
            self.current_nodes = set(all_children)
    
    def set_node_scores(self):
        assert len(self.root.children) != 0, "create game tree before setting scores"
        self.root.set_score()
        return
    
    def get_move_from_boards(self, base_state, new_state): # FIX FOR C4
        base_state_children = self.all_nodes[str(base_state)].children
        assert new_state in [child.board for child in base_state_children]

        for i in range(len(new_state)):
            for j in range(len(new_state[0])):
                base = base_state[i][j]
                new = new_state[i][j]
                if base != new:
                    return (i,j)
    
    def get_best_move(self):
        base_state = self.root.board
        scores = [node.score for node in self.root.children]
        max_index = scores.index(max(scores))
        best_move_node = self.root.children[max_index]
        new_state = best_move_node.board
        return self.get_move_from_boards(base_state, new_state)

    def flatten(self, input_list):
        result = []
        for collection in input_list:
            result += collection
        return result

test_board = [
    [0,2,0,2,0,2,0,2],
    [2,0,2,0,2,0,2,0],
    [0,2,0,2,0,2,0,2],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [1,0,1,0,1,0,1,0],
    [0,1,0,1,0,1,0,1],
    [1,0,1,0,1,0,1,0],
]

net = ScoringNeuralNet()
test = ReducedGameTree(test_board, 1, net)
test.create_node_children(test.root)
for child in test.root.children:
    test.create_node_children(child)
print(len(test.all_nodes))
