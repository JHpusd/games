import random, copy

class NearPerfectPlayer():
    def __init__(self):
        self.number = None
    
    def set_player_number(self, num):
        self.number = num
    
    def update_board(self, game_state):
        pass
    
    def get_row_col_diag(self, game_state):
        rows = list(game_state)
        cols = [[game_state[i][j] for i in range(3)] for j in range(3)]
        diag_1 = [game_state[i][i] for i in range(3)]
        diag_2 = [game_state[i][2-i] for i in range(3)]
        diags = [diag_1, diag_2]
        return (rows, cols, diags)
    
    def two_in_three(self, arr):
        if arr.count(None) != 1:
            return (False, None)
        if arr.count(1) == 2:
            return (True, 1)
        if arr.count(2) == 2:
            return (True, 2)
    
    def check_for_winner(self, game_state):
        rcd = self.get_row_col_diag(game_state)
        for item in rcd[0]+rcd[1]+rcd[2]:
            if None in item:
                continue
            if item.count(item[0]) == 3:
                return item[0]
    
    def insert_move(self, game_state, coord, player_num):
        state_copy = copy.deepcopy(game_state)
        state_copy[coord[0]][coord[1]] = player_num
        return state_copy
    
    def choose_move(self, game_state):
        choices = [(i,j) for i in range(len(game_state)) for j in range(len(game_state)) if game_state[i][j]==None]
        rng = random.randint(1,10)
        if rng == 1:
            print('RANDOM')
            return random.choice(choices)
        
        for choice in choices:
            new_state = self.insert_move(game_state, choice, self.number)
            if self.check_for_winner(new_state) == self.number:
                print('winner')
                return choice
        for choice in choices:
            new_state = self.insert_move(game_state, choice, 3-self.number)
            if self.check_for_winner(new_state) == 3-self.number:
                print('prevent loss')
                return choice
        rcd = self.get_row_col_diag(game_state)
        for i,row in enumerate(rcd[0]):
            if row.count(None) == 2 and row.count(3-self.number) == 1:
                print('row')
                return (i,random.choice([n for n,item in enumerate(row) if item == None]))
        for i,col in enumerate(rcd[1]):
            if col.count(None) == 2 and col.count(3-self.number) == 1:
                print('col')
                return (random.choice([n for n,item in enumerate(col) if item == None]),i)
        diag_1 = [(0,0), (1,1), (2,2)]
        diag_2 = [(0,2), (1,1), (2,0)]
        for i,diag in enumerate(rcd[2]):
            if diag.count(None) == 2 and diag.count(3-self.number) == 1:
                print('diag')
                if i == 0:
                    return diag_1[random.choice([n for n,item in enumerate(diag) if item==None])]
                return diag_2[random.choice([n for n,item in enumerate(diag) if item==None])]
        
        print('RANDOM')
        return random.choice(choices)
    
    def report_winner(self, winner_num, board):
        pass
