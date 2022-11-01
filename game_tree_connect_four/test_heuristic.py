from heuristic_game_tree import *
from heuristic_player import *
from input_player import *
from random_player import *
from last_min_player import *
from anton_comp import *
from cayden_comp import *
from charlie_comp import *
from maia_comp import *
from william_comp import *
from connect_four import *


wins = {'william':0, 'maia':0}
game_count = 1
for _ in range(2):
    players = [WilliamHeuristicPlayer(), MaiaHeuristicPlayer()]
    game = ConnectFour(players)
    game.run_to_completion()
    if game.winner == 1:
        wins['william'] += 1
    if game.winner == 2:
        wins['maia'] += 1
    print(f'finished game {game_count}')
    game_count += 1

for _ in range(2):
    players = [MaiaHeuristicPlayer(), WilliamHeuristicPlayer()]
    game = ConnectFour(players)
    game.run_to_completion()
    if game.winner == 1:
        wins['maia'] += 1
    if game.winner == 2:
        wins['william'] += 1
    print(f'finished game {game_count}')
    game_count += 1
print(wins)
