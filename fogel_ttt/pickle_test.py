from nn_player import *
from np_player import *
import sys, pickle, copy
import random as r
import matplotlib.pyplot as plt
sys.path.append('game_tree_ttt')
from tic_tac_toe import *
from input_player import *
from random_player import *

final_gen_players = []
with open('nn_players.pickle', 'rb') as f:
    while True:
        try:
            final_gen_players.append(pickle.load(f))
        except EOFError:
            break

print('finished getting players')

nn_player = final_gen_players[10][5]
wins = {'nn_player':0,'other':0}
for _ in range(32):
    players1 = [nn_player, NearPerfectPlayer()]
    players2 = [nn_player, RandomPlayer()]
    game = TicTacToe(players2)
    game.run_to_completion()
    if game.winner == 1:
        wins['nn_player'] += 1
    if game.winner == 2:
        wins['other'] += 1
print(wins)