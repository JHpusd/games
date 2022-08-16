from game_tree import *
from minimax_player import *
from random_player import *
from tic_tac_toe import *

players = [MinimaxPlayer(), RandomPlayer()]
game = TicTacToe(players, 'minimax_v_random.txt')
game.run_to_completion()