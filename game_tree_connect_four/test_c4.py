from connect_four import *
from input_player import *
from random_player import *
from heuristic_player import *

players = [InputPlayer(), HeuristicPlayer()]
game = ConnectFour(players)
game.run_to_completion()