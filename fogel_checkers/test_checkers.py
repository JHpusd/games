from checkers import *
from input_player import *
from semirandom_player import *
from random_player import *
from test_player import *

board = [
    [0,2,0,0,0,0,0,0],
    [2,0,2,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,2,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,2,0,0,0,0,0],
    [0,1,0,0,0,0,0,0],
    [1,0,1,0,1,0,0,0]
]

p1 = InputPlayer()
p2 = SemirandomPlayer()
players = [p1, p2]
game = Checkers(players)
game.board = board
game.run_turn()
#game.run_to_completion()
#print(game.winner)