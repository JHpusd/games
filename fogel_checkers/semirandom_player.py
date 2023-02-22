import random

class SemirandomPlayer():
    def __init__(self):
        self.player_num = None
    
    def set_player_number(self, player_num):
        self.player_num = player_num
    
    def choose_move(self, board, options):
        captures = [move for move in options if len(moves[2])>0]
        if len(captures) == 0:
            return random.choice(options)
        return random.choice(captures)
