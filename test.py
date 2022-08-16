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
parents = [1,2,3,4]
children = [[1,2,3,4,5],[2,6,7,8,9],[1,3,7,10,11],[9,10,20,21,22]]

def repeats_with_parents(parents, children):
    for i in range(len(parents)):
        

test = set([1,2,3])
test2 = set([3,4,5])
print(test.intersection(test2))