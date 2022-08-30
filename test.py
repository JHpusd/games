def transpose(col_board):
    board = []
    for i in range(6):
        row = []
        for col in col_board:
            row.append(col[i])
        board.append(row)
    return board

def log_board(col_board):
        board = transpose(col_board)
        for i in range(len(board)):
            row = board[i]
            row_string = ''
            for space in row:
                if space == None:
                    row_string += '_|'
                else:
                    row_string += str(space) + '|'
            print(row_string[:-1])
        print('\n')

def possible_moves(col_board):
    return [i for i,col in enumerate(col_board) if col.count(0)>0]

col_board = [[0,0,0,0,0,1],[0,0,0,0,0,0],[0,0,0,0,0,2],[0,0,0,0,0,0,],[0,0,0,0,0,0,],[0,0,0,0,0,0],[0,0,0,0,0,0]]
print(possible_moves(col_board))