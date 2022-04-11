import sys
sys.path.append('genetic_alg_folder')
from genetic_alg import *

gen_alg = GeneticAlgorithm(8)
gen_1 = gen_alg.copy(gen_alg.all_players)
print(gen_1[0].gen)
gen_alg.make_n_gens(10, 'rr', 'cut', 0.001)
gen_n = gen_alg.copy(gen_alg.all_players)
print(gen_n[0].gen)