import sys
from nn_player import *
sys.path.append('game_tree_ttt')
from tic_tac_toe import *

players = [NeuralNetPlayer(), NeuralNetPlayer()]
game = TicTacToe(players)
game.run_to_completion()
print(game.winner)