from checkers import *
from input_player import *
from random_player import *
from test_player import *

p1 = InputPlayer()
p2 = RandomPlayer()
players = [p1, p2]
game = Checkers(players)
game.run_to_completion()
print(game.winner)