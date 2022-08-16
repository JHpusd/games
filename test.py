import sys
sys.path.append('genetic_alg_folder')
from genetic_alg import *
from tic_tac_toe import *
import random as r
'''
gen_alg = GeneticAlgorithm(32)
gen_1 = gen_alg.copy(gen_alg.all_players)
prev_gen = gen_alg.copy(gen_1)
gens = [2,3,4,5,10,15,20]
vs_gen_1_score = []

for gen in gens:
    while gen_alg.generation != gen:
        prev_gen = gen_alg.copy(gen_alg.all_players)
        gen_alg.make_new_gen('rr', 'cut', 0)
    new_gen = gen_alg.copy(gen_alg.all_players)
    gen_alg.round_robin(new_gen)
    new_gen = new_gen[:5]

    gen_alg.fight(gen_1, new_gen)
    vs_gen_1_score.append(sum([p.score for p in new_gen]))
print(vs_gen_1_score)
'''
test = [1,None,0]
print(max(test))