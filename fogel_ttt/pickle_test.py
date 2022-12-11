from nn_player import *
from np_player import *
import sys, pickle, copy
import random as r
import matplotlib.pyplot as plt
sys.path.append('game_tree_ttt')
from tic_tac_toe import *

final_gen_players = []
with open('nn_players.pickle', 'rb') as f:
    while True:
        try:
            final_gen_players.append(pickle.load(f))
        except EOFError:
            break
print(len(final_gen_players))
print(len(final_gen_players[0]))
print(final_gen_players[0][0])