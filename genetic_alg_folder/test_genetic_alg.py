from tic_tac_toe import *
from gene_players import *
from genetic_alg import *
import random as r

gen_alg = GeneticAlgorithm(25, 5)
gen_1 = list(gen_alg.all_players)
gen_alg.make_n_gens(20)
gen_21 = list(gen_alg.all_players)
gen_alg.make_n_gens(20)
gen_41 = list(gen_alg.all_players)

scores = {'gen_1':0, 'gen_21':0}
for _ in range(50):
    player_1 = r.choice(gen_1)
    player_2 = r.choice(gen_21)
    game = TicTacToeGene([player_1, player_2])
    game.run_to_completion()
    if game.winner == 1:
        scores['gen_1'] += 1
    if game.winner == 2:
        scores['gen_21'] += 1

for _ in range(50):
    player_1 = r.choice(gen_21)
    player_2 = r.choice(gen_1)
    game = TicTacToeGene([player_1, player_2])
    game.run_to_completion()
    if game.winner == 1:
        scores['gen_21'] += 1
    if game.winner == 2:
        scores['gen_1'] += 1

print(scores)

# gen 1 vs gen 21: 39 - 46 and 25 - 58 and 37 - 51
# gen 1 vs gen 41: 42 - 44 and 34 - 54 and 41 - 46
# gen 21 vs gen 41: 38 - 47 and 39 - 57 and 20 - 78
# gen 1 vs gen 71: 39 - 51
