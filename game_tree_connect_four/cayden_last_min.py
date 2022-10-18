import random
import copy
import math
import itertools


class CaydenLastMinPlayer:
    def __init__(self):
        self.number = None
    
    def set_player_number(self, n):
        self.number = n

    def get_diagonals(self, board):
        fdiag = [[] for _ in range(len(board) + len(board[0]) - 1)]
        bdiag = [[] for _ in range(len(fdiag))]

        for x in range(len(board[0])):
            for y in range(len(board)):
                fdiag[x + y].append(board[y][x])
                bdiag[x - y - (1 - len(board))].append(board[y][x])

        return fdiag + bdiag

    def get_columns(self, board):
        columns = []

        for column_index in range(len(board[0])):
            columns.append([row[column_index] for row in board])

        return columns

    def get_row_with_lowest_available_column(self, j, board):
        largest_row = 0

        for n in range(len(board)):
            if board[n][j] == 0:
                largest_row = n

        return largest_row

    def check_for_winner(self, board):
        rows = board
        cols = self.get_columns(board)
        diags = self.get_diagonals(board)

        str_info = []

        board_full = True

        for info in rows + cols + diags:
            if 0 in info:
                board_full = False

        for info in rows + cols + diags:
            for player_num in [1, 2]:
                if str(player_num) * 4 in "".join([str(element) for element in info]):
                    return player_num

        if board_full:
            return 'Tie'

        return None

    def check_if_list_element_in_str(self, input_list, input_string):
        for element in input_list:
            if element in input_string:
                return True

        return False

    def get_num_instances(self, input_list, input_string):
        num_instances = 0

        for element in input_list:
            if element in input_string:
                num_instances += 1

        return num_instances
    
    def choose_move(self, game_board, choices):
        win_choices = []
        block_choices = []

        for choice in choices:
            new_board = copy.deepcopy(game_board)
            i = self.get_row_with_lowest_available_column(choice, new_board)
            new_board[i][choice] = self.number

            if self.check_for_winner(new_board) == self.number:
                win_choices.append(choice)

            new_info = [new_board[i], [row[choice] for row in new_board]]
            old_info = [game_board[i], [row[choice] for row in game_board]]

            diags = self.get_diagonals(copy.deepcopy(new_board))

            for n in range(0, len(diags)):
                if diags[n] != self.get_diagonals(game_board)[n]:
                    new_info.append(diags[n])
                    old_info.append(self.get_diagonals(game_board)[n])

            perms = list(itertools.permutations(list(str(3 - self.number)*3 + str(self.number))))
            perms = [''.join(perm) for perm in perms]


            for n in range(0, len(old_info)):
                num_instances_new = self.get_num_instances(perms, "".join([str(element) for element in new_info[n]]))
                num_instances_old = self.get_num_instances(perms, "".join([str(element) for element in old_info[n]]))

                if num_instances_new > num_instances_old:
                    # print(f"block choices {choice}")
                    block_choices.append(choice)

        if len(win_choices) > 0:
            return random.choice(win_choices)

        if len(block_choices) > 0:
            return random.choice(block_choices)

        return random.choice(choices)