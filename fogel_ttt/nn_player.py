from fogel_nn import *
import math, pickle, copy

class NeuralNetPlayer():
    def __init__(self, net=None):
        self.number = None
        if net != None:
            self.net = net
        else:
            self.net = FogelEvolvingNet()
        self.payoff_score = 0
        self.eval_score = 0
    
    def set_player_number(self, num):
        self.number = num
    
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
    
    def initialize_net(self):
        self.net.initialize()
    
    def replicate(self):
        new_net = self.net.replicate()
        return NeuralNetPlayer(new_net)
    
    def report_winner(self, winner_num, board):
        pass