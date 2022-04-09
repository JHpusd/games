import random as r

class Player():
    def __init__(self, player_name=None):
        self.player_name = player_name
        self.player_num = None
        self.strategy = None
        self.score = 0
        self.gen = 1

    def set_num(self, num):
        self.player_num = num
        if self.player_name == None:
            self.player_name = f'Player {num}'

    def set_strat(self, strat):
        self.strategy = strat
    
    def move(self, game_state):
        return self.strategy[game_state]
    
    def copy(self):
        player_copy = Player(player_name=self.player_name)
        player_copy.set_num(self.player_num)
        player_copy.set_strat({key:self.strategy[key] for key in self.strategy})
        player_copy.gen = int(self.gen)
        return player_copy