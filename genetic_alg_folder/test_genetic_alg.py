from tic_tac_toe import *
from gene_players import *
from genetic_alg import *
from itertools import combinations, product
import random as r
import matplotlib.pyplot as plt

gen_alg = GeneticAlgorithm(25)
gens = [1,2,3,5,10,15,20,30,50,75,100,150]

plot_1 = []
plot_2 = []

def win_cap_freq(player_group)
plot_3 = []
plot_4 = []

gen_1 = gen_alg.copy(gen_alg.all_players)
#prev_gen = gen_alg.copy(gen_alg.all_players)
for gen in gens:
    while gen_alg.generation != gen:
        #prev_gen = gen_alg.copy(gen_alg.all_players)
        gen_alg.make_new_gen('rr', 'cut', 0)
    gen_alg.all_players.sort(key=lambda x: x.score, reverse=True)
    gen_n = gen_alg.copy(gen_alg.all_players[:5])
    gen_n_2 = gen_alg.copy(gen_alg.all_players)

    gen_alg.fight(gen_1, gen_n)
    #plot_1.append(sum([p.score for p in gen_n])/5)
'''
plt.style.use('bmh')
plt.figure(0)
plt.plot(gens, plot_1)
plt.xlabel('# generations')
plt.ylabel('avg score against 1st gen')
plt.savefig('plot_1.png')
'''
plt.figure(1)
plt.plot(gens, plot_2)
plt.savefig('plot_2.png')

'''
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
'''