from checkers import *

class TreeNode():
    def __init__(self, board, player_turn, player_num, scoring_nn):
        # board should NOT be adjusted by player
        self.board = board
        self.turn = player_turn
        self.player = player_num
        self.net = scoring_nn
        self.winner = self.check_for_winner()
        self.previous = []
        self.children = []
        self.score = None

    def arr_add(self, arr_1, arr_2):
        return [arr_1[i] + arr_2[i] for i in range(len(arr_1))]

    def add_moves_to_check(self, current_piece, current_coords, captured_coords, moves_to_check):
        
        direction = 1 - 2*(current_piece % 2)

        moves_to_check.append([current_coords, [direction, -1], captured_coords])
        moves_to_check.append([current_coords, [direction, 1], captured_coords])

        if current_piece < 0:
            moves_to_check.append([current_coords, [-direction, -1], captured_coords])
            moves_to_check.append([current_coords, [-direction, 1], captured_coords])
        
        return moves_to_check
    
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
    
    def nested_list_in_list(self, parent_list, nested_list):
        for l in parent_list:
            if all(x == y for x, y in zip(l, nested_list)):
                return True
        return False
    
    def find_translation(self, coord1, coord2):
        return [coord1[0] - coord2[0], coord1[1] - coord2[1]]
    
    def check_for_winner(self):
        if len(self.get_all_moves(self.player, self.board)) == 0:
            return -1
        if len(self.get_all_moves(3-self.player, self.board)) == 0:
            return 1
    
    def children_to_score(self):
        if self.children == None or len(self.children) == 0:
            return None
        for child in self.children:
            child.set_score()
        return [child.score for child in self.children]
    
    def adjust_vals(self, arr):
        for i,item in enumerate(arr):
            if item == self.player:
                arr[i] = 1
            if item == -self.player:
                arr[i] = 2
            if item == 3-self.player:
                arr[i] = -1
            if item == self.player-3:
                arr[i] = -2
        return arr
    
    def set_score(self):
        if len(self.children) == 0 or self.children == None:
            if self.winner == 1:
                self.score = 1
            elif self.winner == -1:
                self.score = -1
            elif self.winner == 'Tie':
                self.score = 0
            else:
                adjusted_arr = []
                for i,row in enumerate(self.board):
                    if i%2 == 0: # odds
                        odds = [row[j] for j in range(len(row)) if j%2 == 1]
                        adjusted_arr += odds

                    else: # evens
                        evens = [row[j] for j in range(len(row)) if j*2 == 0]
                        adjusted_arr += evens

                self.score = self.net.score_board(adjusted_arr)
            return

        #print([child.state for child in self.children])
        if self.turn == self.player:
            self.score = max(self.children_to_score())
        elif self.turn == 3 - self.player:
            self.score = min(self.children_to_score())

'''test_board = [
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,2,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,0,2,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
]

test = TreeNode(test_board,2,2,123)
test.set_score()
print(test.score)'''