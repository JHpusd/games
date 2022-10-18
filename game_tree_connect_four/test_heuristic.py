from heuristic_game_tree import *
from heuristic_player import *
from input_player import *
from random_player import *
from last_min_player import *
from anton_last_min import *
from cayden_last_min import *
from charlie_last_min import *
from maia_last_min import *
from connect_four import *

players = [LastMinPlayer(), MaiaLastMinPlayer()]
game = ConnectFour(players)
game.run_to_completion()
print(game.winner)

'''
wins = {'lastmin':0, 'heuristic':0}
game_count = 1
for _ in range(5):
    players = [LastMinPlayer(), HeuristicPlayer(4)]
    game = ConnectFour(players)
    game.run_to_completion()
    if game.winner == 1:
        wins['lastmin'] += 1
    if game.winner == 2:
        wins['heuristic'] += 1
    print(f'finished game {game_count}')
    game_count += 1

for _ in range(5):
    players = [HeuristicPlayer(4), LastMinPlayer()]
    game = ConnectFour(players)
    game.run_to_completion()
    if game.winner == 1:
        wins['heuristic'] += 1
    if game.winner == 2:
        wins['lastmin'] += 1
    print(f'finished game {game_count}')
    game_count += 1
print(wins)
'''