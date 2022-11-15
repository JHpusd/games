import sys
from nn_player import *
from np_player import *
sys.path.append('game_tree_ttt')
from tic_tac_toe import *

players = [NeuralNetPlayer(), NearPerfectPlayer()]
game = TicTacToe(players)
game.run_to_completion()
print(game.winner)