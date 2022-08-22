from game_tree import *
from minimax_player import *
from random_player import *
from top_left_player import *
from input_player import *
from tic_tac_toe import *
'''
wins = {'minimax':0, 'random':0, 'tie':0}
print('starting first 50')
for _ in range(50):
    players = [MinimaxPlayer(), RandomPlayer()]
    game = TicTacToe(players)
    game.run_to_completion()
    print(game.winner)
    if game.winner == 'Tie':
        wins['tie'] += 1
    elif game.winner == 1:
        wins['minimax'] += 1
    elif game.winner == 2:
        wins['random'] += 1
print('first 50 finished')
for _ in range(50):
    players = [RandomPlayer(), MinimaxPlayer()]
    game = TicTacToe(players)
    game.run_to_completion()
    print(game.winner)
    if game.winner == 'Tie':
        wins['tie'] += 1
    elif game.winner == 2:
        wins['minimax'] += 1
    elif game.winner == 1:
        wins['random'] += 1
'''
players = [InputPlayer(), MinimaxPlayer()]
game = TicTacToe(players, 'minimax_v_input.txt')
game.run_to_completion()