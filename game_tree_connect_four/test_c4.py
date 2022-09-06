from connect_four import *
from input_player import *
from random_player import *

players = [InputPlayer(), RandomPlayer()]
game = ConnectFour(players)
game.run_to_completion()