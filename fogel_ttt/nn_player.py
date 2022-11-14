from fogel_nn import *
import math

class NeuralNetPlayer():
    def __init__(self):
        self.number = None
        self.net = FogelEvolvingNet()
    
    def set_player_number(self, num):
        self.number = num # should always be player 1 for now
        self.net.initialize()
    
    def update_board(self, game_state):
        pass

    def idx_to_coord(self, idx):
        row = math.floor(idx/3)
        col = idx % 3
        return (row,col)
    
    def choose_move(self, game_state):
        flat_state = []
        for row in game_state:
            for item in row:
                if item == None:
                    flat_state.append(0)
                if item == self.number:
                    flat_state.append(1)
                if item == 3 - self.number:
                    flat_state.append(-1)
        outputs = self.net.input_array(flat_state)
        out_vals = list(outputs)
        max_idx = outputs.index(max(outputs))
        while flat_state[max_idx] != 0:
            out_vals.remove(max(out_vals))
            max_idx = outputs.index(max(out_vals))
        
        return self.idx_to_coord(max_idx)
    
    def report_winner(self, winner_num, board):
        pass
