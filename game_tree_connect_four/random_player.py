import random, math

class RandomPlayer():
    def __init__(self):
        self.number = None
    
    def set_player_number(self, num):
        self.number = num
    
    def choose_move(self, board, choices):
        return random.choice(choices)

    def report_winner(self, winner, board):
        pass