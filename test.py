import sys
sys.path.append('genetic_alg_folder')
from genetic_alg import *
from tic_tac_toe import *
import random as r

gen_alg = GeneticAlgorithm(8)
gen_1 = gen_alg.copy(gen_alg.all_players)
gen_alg.make_n_gens(10, 'rr', 'cut', 0.001)
gen_11 = gen_alg.copy(gen_alg.all_players)

comp_pair = [r.choice(gen_1), r.choice(gen_11)]
r.shuffle(comp_pair)
game = TicTacToeGene(comp_pair)
game.run_to_completion()
print(game.winner)
print([player.gen for player in comp_pair])
print(game.players[game.winner - 1].gen)