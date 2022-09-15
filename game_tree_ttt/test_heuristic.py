from game_nodes import *
from heuristic_game_tree import *
from heuristic_player import *
from input_player import *
from minimax_player import *
from random_player import *
from tic_tac_toe import *

def heuristic_func(game_state, player_num, turn):
    rows = game_state
    cols = [[game_state[i][j] for i in range(3)] for j in range(3)]
    diags = [[game_state[i][i] for i in range(3)],[game_state[i][2-i] for i in range(3)]]
    rcd = rows + cols + diags

    # winner/tie case is covered in node class
    self_advantage = 0
    if player_num==turn:
        self_advantage += 1
    else:
        self_advantage -= 1
    two_counts = {player_num:0, 3-player_num:0}

    for item in rcd:
        # 2 in a row for player that is to play - win for turn player
        if None in item and item.count(turn)==2:
            if player_num==turn:
                return 1
            return -1
        # 2 2s in a row - win for player that has 2 2s
        if two_counts[player_num]==2:
            return 1
        if two_counts[3-player_num]==2:
            return -1
        if None in item and item.count(player_num)==2:
            two_counts[player_num] += 1
        elif None in item and item.count(3-player_num)==2:
            two_counts[3-player_num] += 1

    two_total = two_counts[player_num]-two_counts[3-player_num]
    return self_advantage + two_total

# minimax vs heuristic player
wins = {'2 ply':0, '9 ply':0, 'tie':0}
for _ in range(10):
    players = [HeuristicPlayer(heuristic_func,2), HeuristicPlayer(heuristic_func,9)]
    game = TicTacToe(players, '2ply_v_9ply.txt')
    game.run_to_completion()
    if game.winner == 1:
        wins['2 ply'] += 1
    elif game.winner == 2:
        wins['9 ply'] += 1
    else:
        wins['tie'] += 1
    print(game.winner)
for _ in range(10):
    players = [HeuristicPlayer(heuristic_func, 9), HeuristicPlayer(heuristic_func,2)]
    game = TicTacToe(players, '9ply_v_2ply.txt')
    game.run_to_completion()
    if game.winner == 2:
        wins['2 ply'] += 1
    elif game.winner == 1:
        wins['9 ply'] += 1
    else:
        wins['tie'] += 1
    print(game.winner)
print(wins)