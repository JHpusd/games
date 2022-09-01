def transpose(board):
    t_board = []
    for i in range(len(board[0])):
        t_row = []
        for arr in col_board:
            t_row.append(arr[i])
        t_board.append(t_row)
    return t_board

def print_board(board):
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
    
def arr_add(arr_1, arr_2):
    assert len(arr_1) == len(arr_2), 'different len arrays'
    result = []
    for i in range(len(arr_1)):
        result.append(arr_1[i] + arr_2[i])
    return result

def get_diags():
    coords = [[0,0],[5,0]]
    diags = []
    for coord in coords:
        tb_based_diags = []
        dummy = list(coord)
        for _ in range(7):
            coord_diags = []
            options = [[1,1], [1,-1],[-1,1],[-1,-1]]
            for option in options:
                diag_indices = []
                while dummy[0]>=0 and dummy[0]<6 and dummy[1]>=0 and dummy[1]<7:
                    diag_indices.append(dummy)
                    dummy = arr_add(dummy, option)
                if len(diag_indices) > 3:
                    coord_diags.append(diag_indices)
                dummy = list(coord)
            coord[1] += 1
            dummy = list(coord)
            tb_based_diags += coord_diags
        diags += tb_based_diags
    return diags

def get_diags_2():
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
                dummy = arr_add(dummy, option)
            if len(diag) > 3:
                coord_diags.append(diag)
            dummy = list(coord)
        dummy = list(coord)
        diags += coord_diags
    return diags
    
def elem_from_coords(coords, board):
    elems = []
    for coord in coords:
        elems.append(board[coord[0]][coord[1]])
    return elems

def possible_moves(col_board):
    return [i for i,col in enumerate(col_board) if col.count(0)>0]

col_board = [[0,0,0,0,0,1],[0,0,0,0,0,0],[0,0,0,0,0,2],[0,0,0,0,0,0,],[0,0,0,0,0,0,],[0,0,0,0,0,0],[0,0,0,0,0,0]]
board = transpose(col_board)

board = [[1,2,3,4,5,6,7],[8,9,10,11,12,13,14],[15,16,17,18,19,20,21],[21,22,23,24,25,26,27,28],[29,30,31,32,33,34,35],[36,37,38,39,40,41,42]]

print_board(board)
print(elem_from_coords([[0,0],[0,1],[0,2]],board))