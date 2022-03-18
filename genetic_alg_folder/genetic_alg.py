from gene_players import *
from tic_tac_toe import *
import random as r
from itertools import combinations, product
import operator as op
import math
from functools import reduce

def ncr(n, r):
    r = min(r, n-r)
    numer = reduce(op.mul, range(n, n-r, -1), 1)
    denom = reduce(op.mul, range(1, r+1), 1)
    return numer // denom

class GeneticAlgorithm():
    def __init__(self, num_strats, num_survivors):
        self.num_strats = num_strats
        self.top_n = num_survivors
        self.all_players = [Player() for _ in range(num_strats)]
        self.generation = 1
        self.strat_base = self.gen_strat_base()
        self.init_set_up_players()
    
    def gen_strat_base(self):
        all_states = []
        base = '000000000'
        for a in range(3):
            base = self.assign(base, 0, a)
            for b in range(3):
                base = self.assign(base, 1, b)
                for c in range(3):
                    base = self.assign(base, 2, c)
                    for d in range(3):
                        base = self.assign(base, 3, d)
                        for e in range(3):
                            base = self.assign(base, 4, e)
                            for f in range(3):
                                base = self.assign(base, 5, f)
                                for g in range(3):
                                    base = self.assign(base, 6, g)
                                    for h in range(3):
                                        base = self.assign(base, 7, h)
                                        for i in range(3):
                                            base = self.assign(base, 8, i)
                                            ones = base.count('1')
                                            twos = base.count('2')
                                            if '0' in base and abs(ones - twos) < 2:
                                                all_states.append(base)
        return {state:None for state in all_states}

    def assign(self, base, i, val):
        if type(val) != str:
            val = str(val)
        vals = list(base)
        vals[i] = val
        return ''.join(vals)
    
    def init_set_up_players(self):
        for i, player in enumerate(self.all_players):
            player.set_num(i)
            player.set_strat(self.create_strat())

    def valid_indices(self, state_str):
        vals = list(state_str)
        result = []
        for i in range(len(vals)):
            if vals[i] == '0':
                result.append(i)
        return result
    
    def create_strat(self):
        strat_base = dict(self.strat_base)
        for key in strat_base:
            options = self.valid_indices(key)
            strat_base[key] = r.choice(options)
        return strat_base
    
    def run_competition(self, player_pair):
        game = TicTacToeGene(player_pair)
        game.run_to_completion()
        if game.winner != 'Tie':
            player_pair[game.winner-1].score += 1
            player_pair[2-game.winner].score -= 1

        player_pair = player_pair[::-1]
        game = TicTacToeGene(player_pair)
        game.run_to_completion()
        if game.winner != 'Tie':
            player_pair[game.winner-1].score += 1
            player_pair[2-game.winner].score -= 1
    
    def run_all_comps(self):
        comp_pairs = list(combinations(self.all_players, 2))
        for pair in comp_pairs:
            self.run_competition(pair)
    
    def strat_selection(self):
        self.run_all_comps()
        func = lambda player: player.score
        self.all_players.sort(key=func, reverse=True)
        self.all_players = self.all_players[:self.top_n]

    def mate(self, player_pair):
        new_player = Player()
        new_strat = {}
        strat_1 = player_pair[0].strategy
        strat_2 = player_pair[1].strategy
        for key in strat_1:
            options = [strat_1[key], strat_2[key]]
            new_strat[key] = r.choice(options)
        new_player.set_strat(new_strat)
        return new_player
    
    def make_new_gen(self):
        self.strat_selection()
        mate_pairs = list(combinations(self.all_players, 2))
        while len(self.all_players) != self.num_strats:
            for pair in mate_pairs:
                if len(self.all_players) == self.num_strats:
                    break
                new_player = self.mate(pair)
                self.all_players.append(new_player)
        self.generation += 1
    
    def make_n_gens(self, n):
        for _ in range(n):
            self.make_new_gen()
    
    def fight(self, group_1, group_2):
        pairs = list(product(group_1, group_2))
        for pair in pairs:
            self.run_competition(pair)
    
    def copy(self, group): # scores are not copied over
        return [player.copy() for player in group]
