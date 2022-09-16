from heuristic_game_tree import *
from heuristic_player import *
from input_player import *
from random_player import *
from connect_four import *

players = [InputPlayer(), HeuristicPlayer(4)]
game = ConnectFour(players)
game.run_to_completion()
print(game.winner)