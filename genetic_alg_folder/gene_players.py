import random as r

class Player():
    def __init__(self, player_name=None):
        self.player_name = player_name
        self.player_num = None
        self.strategy = None
        self.score = 0

    def set_num(self, num):
        self.player_num = num
        if self.player_name == None:
            self.player_name = f'Player {num}'

    def set_strat(self, strat):
        self.strategy = strat
    
    def move(self, game_state):
        return self.strategy[game_state]