import random

class MaiaLastMinPlayer :
    def __init__(self) :
        self.number = None
  
    def set_player_number(self, n) :
        self.number = n

    def find_row(self, board, col) :
        for row in range(5,-1,-1) :
            if board[row][col] == '0' :
                return (row, col)

    def choose_move(self, num_board, choices) :
        board = self.make_string(num_board)
        good, bad = self.size(board)
        choices_ = [self.find_row(board, col) for col in choices]
        good_m = [move for move in good if move in choices]
        bad_m = [move for move in bad if move in choices]
        if good_m != []:
            return good_m[0]
        if bad_m != [] :
            return bad_m[0]
        return random.choice(choices)

    def size(self, board) :
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
        
        thing = [rows, cols, l_dias, r_dias]
        thing_m = [rows_m, cols_m, l_dias_m, r_dias_m]
        good = []
        bad = []
        win = ''.join([str(self.number) for _ in range(3)])
        lose = ''.join([str((self.number % 2) + 1) for _ in range(3)])
        for way_i in range(4) :
            for index in range(len(thing[way_i])) :
                if win in thing[way_i][index] :
                    good.extend(thing_m[way_i][index])
                elif lose in thing[way_i][index] :
                    bad.extend(thing_m[way_i][index])
        return good, bad

    def make_string(self, board) :
        return [''.join(str(_) for _ in row) for row in board]