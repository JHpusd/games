def transpose(board):
    t_board = []
    for i in range(len(board[0])):
        t_row = []
        for arr in board:
            t_row.append(arr[i])
        t_board.append(t_row)
    return t_board

state = [
    [0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0],
    [0,0,1,2,0,0,0],
    [0,0,2,1,2,0,0],
    [0,0,1,2,1,2,0],
    [0,1,1,1,2,2,0]
]
print(transpose(state))