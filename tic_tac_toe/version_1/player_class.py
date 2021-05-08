from random import random
import math

class RandomPlayer():
    def __init__(self):
        self.player_num = None
    
    def set_num(self, num):
        self.player_num = num
    
    def choose_coord(self, options):
        random_idx = math.floor(len(options) * random())
        return options[random_idx]
