import sys
from nn_player import *
from np_player import *
sys.path.append('game_tree_ttt')
from tic_tac_toe import *
from input_player import *

players = [NearPerfectPlayer(), InputPlayer()]
game = TicTacToe(players)
game.run_to_completion()
'''
winners = {'1':0, '2':0, 'Tie':0}
for _ in range(32):
    game = TicTacToe(players)
    game.run_to_completion()
    winners[str(game.winner)] += 1
print(winners)
'''