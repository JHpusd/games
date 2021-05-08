
class TicTacToe():
    def __init__(self, players):
        self.players = players
        self.board = [[None, None, None], [None, None, None], [None, None, None]]
        self.set_player_nums()
        self.turn = 0
        self.winner = None
    
    def set_player_nums(self):
        for i, player in enumerate(self.players):
            player.set_num(i+1)
    
    def get_rows_cols_diags(self):
        rows = [row for row in self.board]

        cols = []
        for col_index in range(len(self.board[0])):
            cols.append([row[col_index] for row in self.board])

        diag_1 = []
        top_left = (0,0)
        diag_2 = []
        top_right = (0,2)
        for i in range(len(self.board[0])):
            diag_1.append(self.board[top_left[0]+i][top_left[1]+i])
            diag_2.append(self.board[top_right[0]+i][top_right[1]-i])
        diags = [diag_1, diag_2]
        return rows + cols + diags
    
    def valid_only(self, nested_list):
        result = list(nested_list)
        for row in result:
            if row.count(None) == len(row):
                result.remove(row)
        return result
    
    def all_what_elem(self, ex_list):
        ex = ex_list[0]
        for item in ex_list:
            if item != ex:
                return False
        return ex
    
    def get_coord_options(self):
        valid_coords = []
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                if self.board[i][j] == None:
                    valid_coords.append((i,j))
        return valid_coords
    
    def flatten(self, nested_list):
        result = []
        for i in nested_list:
            result += i
        return result
    
    def check_for_winner(self):
        # rcd is rows, columns, diagonals
        rcd = self.get_rows_cols_diags()
        valid_rcd = self.valid_only(rcd)
        for item in valid_rcd:
            if self.all_what_elem(item) == 1:
                return 1
            if self.all_what_elem(item) == 2:
                return 2
        if None not in self.flatten(rcd):
            return 'Tie'
        return None
    
    def print_board(self):
        print('\n-----------')
        for row in self.board:
            for item in row[:-1]:
                print(item, end=' | ')
            print(row[-1],"|")
        print('-----------')
    
    def complete_turn(self):
        for player in self.players:
            player_num = player.player_num
            options = self.get_coord_options()
            choice = player.choose_coord(options)
            self.board[choice[0]][choice[1]] = player_num
            if self.check_for_winner() != None:
                self.winner = self.check_for_winner()
                break
        self.turn += 1
    
    def run_to_completion(self):
        while self.winner == None:
            self.complete_turn()