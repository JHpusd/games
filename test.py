import sys
sys.path.append('genetic_alg_folder')
from genetic_alg import *

gen_alg = GeneticAlgorithm(8)
print(f'gen 1: {gen_alg.win_cap_loss_prev_freq(gen_alg.all_players[0])}')
gen_alg.make_n_gens(10, 'rr', 'cut', 0)
print(f'gen 11: {gen_alg.win_cap_loss_prev_freq(gen_alg.all_players[0])}')