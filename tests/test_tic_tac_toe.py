import sys
sys.path.append('tic_tac_toe/version_1')
from game_class import *
from player_class import *

alternate = False
num_wins = {1: 0, 2: 0}
print('100 games test')
for _ in range(100):
    players = [RandomPlayer(), RandomPlayer()]
    game = TicTacToe(players)
    game.run_to_completion()
    winner = game.winner
    if winner != 'Tie':
        if alternate:
            num_wins[3 - winner] += 1
        else:
            num_wins[winner] += 1
    alternate = not alternate
print('player 1 wins:',num_wins[1])
print('player 2 wins:',num_wins[2], '\n')

print('1000 games test')
alternate = False
num_wins = {1: 0, 2: 0}
for _ in range(1000):
    players = [RandomPlayer(), RandomPlayer()]
    game = TicTacToe(players)
    game.run_to_completion()
    winner = game.winner
    if winner != 'Tie':
        if alternate:
            num_wins[3 - winner] += 1
        else:
            num_wins[winner] += 1
    alternate = not alternate
print('player 1 wins:',num_wins[1])
print('player 2 wins:',num_wins[2])
