import sys
sys.path.append('genetic_alg_folder')
from genetic_alg import *

gen_alg = GeneticAlgorithm(8)

state_1 = '111020002'
print(gen_alg.winnable(state_1))