import random, math

class LastMinPlayer():
    def __init__(self):
        self.number = None
    
    def set_player_number(self, num):
        self.number = num
    
    def transpose(self, board):
        t_board = []
        for i in range(len(board[0])):
            t_row = []
            for arr in board:
                t_row.append(arr[i])
            t_board.append(t_row)
        return t_board
    
    def arr_add(self, arr_1, arr_2):
        assert len(arr_1) == len(arr_2), 'different len arrays'
        result = []
        for i in range(len(arr_1)):
            result.append(arr_1[i] + arr_2[i])
        return result
    
    def coords_to_elem(self, coords, board):
        if type(coords)!=list:
            coords = [coords]
        elems = []
        for coord in coords:
            elems.append(board[coord[0]][coord[1]])
        return elems
    
    def get_diags(self, board):
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
                    dummy = self.arr_add(dummy, option)
                if len(diag) > 3:
                    coord_diags.append(diag)
                dummy = list(coord)
            dummy = list(coord)
            diags += coord_diags
        
        diag_elems = []
        for diag in diags:
            diag_elems.append(self.coords_to_elem(diag, board))
        
        return [diag_elems, diags]
    
    def three_in_four(self, arr): # ex. 0 1 1 0 1 0 -> 1
        for i,val in enumerate(arr[:-3]):
            len_four = arr[i:i+4]
            if len_four.count(1)==3 and 0 in len_four:
                return (1, i+len_four.index(0))
            elif len_four.count(2)==3 and 0 in len_four:
                return (2, i+len_four.index(0))
    
    def open_ended_three(self, arr):
        for i,val in enumerate(arr[:-4]):
            len_five = arr[i:i+5]
            if len_five[1]==0:
                continue
            if len(set(len_five[1:-1]))==1 and len_five.count(0)==2:
                return (len_five[1],[i,i+4])
    
    def choose_move(self, board, choices):
        rows = board
        cols = self.transpose(board)
        diags = self.get_diags(board)
        diag_elems = diags[0]
        diag_coords = diags[1]
        loss_prevent = None

        for i,row in enumerate(rows):
            potential = self.three_in_four(row)
            open_three = self.open_ended_three(row)
            if potential != None:
                target_coord = (i,potential[1])
                if i == 5 or board[i+1][potential[1]] != 0:
                    if potential[0] != self.number:
                        loss_prevent = potential[1]
                    else:
                        return potential[1]
            if open_three != None:
                col_idxs = open_three[1]
                target_coords = [(i,col_idx) for col_idx in col_idxs]
                if i == 5 and open_three[0] == self.number:
                    return open_three[1][0]
                elif i == 5 and open_three[0] == 3-self.number:
                    continue
                for coord in target_coords:
                    if board[coord[0]+1][coord[1]] != 0:
                        if open_three[0] == self.number:
                            return coord[1]
        
        for i,col in enumerate(cols):
            potential = self.three_in_four(col)
            if potential != None:
                if potential[0] != self.number:
                    loss_prevent = i
                else:
                    return i
        
        for i,diag in enumerate(diag_elems):
            potential = self.three_in_four(diag)
            open_three = self.open_ended_three(diag)
            if potential != None:
                coord = diag_coords[i][potential[1]]

                if coord[0] == 5 or board[coord[0]+1][coord[1]] != 0:
                    if potential != self.number:
                        loss_prevent = coord[1]
                    else:
                        return coord[1]
            if open_three != None:
                coords = [diag_coords[i][col_idx] for col_idx in open_three[1]]
                for coord in coords:
                    if coord[0] == 5 and open_three[0] == self.number:
                        return coord[1]
                    elif coord[0] == 5 and open_three[0] != self.number:
                        loss_prevent = coord[1]
                    elif board[coord[0]+1][coord[1]] != 0:
                        if open_three[0] == self.number:
                            return coord[1]

        if loss_prevent == None:
            return random.choice(choices)
        return loss_prevent

    def report_winner(self, winner, board):
        pass
'''
state = [
    [0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0],
    [0,0,1,2,0,0,0],
    [0,0,2,1,2,0,0],
    [0,0,1,2,1,2,0],
    [0,1,1,1,2,2,0]
]
player = LastMinPlayer()
player.set_player_number(2)
print(player.choose_move(state, [0,1,2,3,4,5,6]))
'''