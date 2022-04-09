from tic_tac_toe import *
from gene_players import *
from genetic_alg import *
from itertools import combinations, product
import random as r
import matplotlib.pyplot as plt

gens = list(range(2,26))
pop_size = 32
fitness = 'rr' # rr or b (bracket)
selection = 'cut' # cut or stoch or tourney
mut_rate = 0.001

vs_gen_1 = []
vs_prev_gen = []

gen_alg = GeneticAlgorithm(pop_size)
gen_1 = gen_alg.copy(gen_alg.all_players)
prev_gen = gen_alg.copy(gen_alg.all_players)

for gen in gens:
    while gen_alg.generation != gen:
        prev_gen = gen_alg.copy(gen_alg.all_players)
        gen_alg.make_new_gen(fitness, selection, mut_rate)
    new_gen = gen_alg.all_players
    vs_gen_1_wins = 0
    vs_prev_gen_wins = 0

    for _ in range(50):
        matchup_1 = [r.choice(new_gen), r.choice(gen_1)]
        matchup_2 = [r.choice(new_gen), r.choice(prev_gen)]
        r.shuffle(matchup_1)
        r.shuffle(matchup_2)

        game_1 = TicTacToeGene(matchup_1)
        game_2 = TicTacToeGene(matchup_2)
        game_1.run_to_completion()
        game_2.run_to_completion()
        if game_1.winner != 'Tie' and game_1.players[game_1.winner-1].gen == gen:
            vs_gen_1_wins += 1
        if game_2.winner != 'Tie' and game_2.players[game_2.winner-1].gen == gen:
            vs_prev_gen_wins += 1
    
    vs_gen_1.append(vs_gen_1_wins/50)
    vs_prev_gen.append(vs_prev_gen_wins/50)

plt.style.use('bmh')
plt.plot(gens, vs_gen_1, label='vs 1st gen')
plt.plot(gens, vs_prev_gen, label='vs prev gen')
plt.xlabel('# generations')
plt.legend(loc='best')
plt.savefig('test.png')

'''
plot_1 = []
plot_2 = []
plot_3 = []
plot_4 = []

gen_1 = gen_alg.copy(gen_alg.all_players)
prev_gen = gen_alg.copy(gen_alg.all_players)
for gen in gens:
    while gen_alg.generation != gen:
        prev_gen = gen_alg.copy(gen_alg.all_players)
        gen_alg.make_new_gen('rr', 'cut', 0)
    all_players = gen_alg.copy(gen_alg.all_players)
    gen_alg.round_robin(all_players)
    gen_n = gen_alg.copy(all_players[:5])
    gen_n_2 = gen_alg.copy(gen_n)

    gen_alg.fight(gen_1, gen_n)
    gen_alg.fight(prev_gen, gen_n_2)
    plot_1.append(sum([p.score for p in gen_n])/5)
    plot_2.append(sum([p.score for p in gen_n_2])/5)

plt.style.use('bmh')

plt.plot(gens, plot_1, label='vs 1st gen')
plt.plot(gens, plot_2, label='vs prev gen')
plt.xlabel('# generations')
plt.legend(loc='best')
plt.savefig('plots_1_and_2.png')


for gen in gens:
    while gen_alg.generation != gen:
        gen_alg.make_new_gen('rr', 'cut', 0)
    all_players = gen_alg.copy(gen_alg.all_players)
    gen_alg.round_robin(all_players)
    wc_lp = gen_alg.wc_lp_for_all(all_players[:5])
    plot_3.append(wc_lp['win_cap'])
    plot_4.append(wc_lp['loss_prev'])

plt.style.use('bmh')
plt.plot(gens, plot_3, label='win capture freq')
plt.plot(gens, plot_4, label='loss prevention freq')
plt.xlabel('# generations')
plt.legend(loc='best')
plt.savefig('plots_3_and_4.png')

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

