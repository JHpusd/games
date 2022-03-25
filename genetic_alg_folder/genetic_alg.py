from gene_players import *
from tic_tac_toe import *
import random as r
from itertools import combinations, product
import math

class GeneticAlgorithm():
    # N/4 strats go on to next gen
    # num_strats is always power of 2 now, minimum of 4
    # mating is random pairs with mutation rate
    # (round robin, bracket competitions) x (hard cutoff, stochastic, tournament selection)
    def __init__(self, num_strats):
        self.num_strats = num_strats
        self.top_n = num_strats/4 # should always be an int
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

    def copy(self, group): # scores are not copied over
        return [player.copy() for player in group]
    
    def fight(self, group_1, group_2):
        pairs = list(product(group_1, group_2))
        for pair in pairs:
            self.run_competition(pair)
    
    def round_robin(self, players):
        comp_pairs = list(combinations(players, 2))
        for pair in comp_pairs:
            self.run_competition(pair)
        players.sort(key=lambda x: x.score, reverse=True)
    
    def comp_pairs(self, players):
        if len(players) < 2:
            return []
        pairs = []
        players_copy = list(players)
        while len(players_copy) > 0:
            p1 = r.choice(players_copy)
            players_copy.remove(p1)
            p2 = r.choice(players_copy)
            players_copy.remove(p2)
            pairs.append((p1, p2))
        return pairs

    def bracket_comps(self, players):
        comps = self.comp_pairs(players)
        winners = [] # winners continue
        while len(comps) >= 1:
            for pair in comps:
                p1 = pair[0]
                p2 = pair[1]
                self.run_competition(pair)
                if p1.score > p2.score:
                    winners.append(p1)
                if p2.score > p1.score:
                    winners.append(p2)
                else:
                    i = r.choice([0,1])
                    winners.append(pair[i])
            comps = self.comp_pairs(winners)
            winners = []
        players.sort(key=lambda x: x.score, reverse=True)
    
    def hard_cut(self, players):
        top_n = int(len(players)/4)
        players.sort(key=lambda x: x.score, reverse=True)
        return players[:top_n]
    
    def subset(self, input_set, num):
        set_copy = list(input_set)
        result = []
        for _ in range(num):
            item = r.choice(set_copy)
            result.append(item)
            set_copy.remove(item)
        return result
    
    def stochastic(self, players):
        players_copy = list(players)
        top_n = int(len(players_copy)/4)
        result = []
        for _ in range(top_n):
            r_subset = self.subset(players_copy, len(players)/8)
            scores = [player.score for player in r_subset]
            i = scores.index(max(scores))
            result.append(r_subset[i])
            players_copy.remove(r_subset[i])
        return result
    
    def tournament(self, rr_or_b, players): # scoring and selection
        # rr is round robin, b is bracket
        players_copy = list(players)
        top_n = int(len(players_copy)/4)
        result = []
        for _ in range(top_n):
            r_subset = self.subset(players_copy, len(players)/8)
            if rr_or_b == 'rr':
                self.round_robin(r_subset)
            elif rr_or_b == 'b':
                self.bracket_comp(r_subset)
            else:
                print('bruh moment')
            result.append(r_subset[0])
        return result
    
    def mate(self, player_pair, mutat_rate):
        new_player = Player()
        new_strat = {}
        strat_1 = dict(player_pair[0].strategy)
        strat_2 = dict(player_pair[1].strategy)
        for key in strat_1:
            i = r.choice(self.valid_indices(key))
            options = [strat_1[key], strat_2[key], i]
            new_strat[key] = r.choices(options, weights=((1-mutat_rate)/2, (1-mutat_rate)/2, mutat_rate))[0]
        new_player.set_strat(new_strat)
        return new_player
    
    def make_new_gen(self, comp_method, select_method, mutat_rate):
        # rr or b for comp_method
        # cut, stoch, or tourney for select_method
        if select_method == 'tourney':
            self.all_players = self.tournament(comp_method, self.all_players)
        else:
            if comp_method == 'rr':
                self.round_robin(self.all_players)
            elif comp_method == 'b':
                self.bracket_comps(self.all_players)
            if select_method == 'cut':
                self.all_players = self.hard_cut(self.all_players)
            elif select_method == 'stoch':
                self.all_players = self.stochastic(self.all_players)
        
        while len(self.all_players) < self.num_strats:
            new_player = self.mate(r.sample(self.all_players, 2), mutat_rate)
            self.all_players.append(new_player)
        self.generation += 1
    
    def make_n_gens(self, n, comp_method, select_method, mutat_rate):
        for _ in range(n):
            self.make_new_gen(comp_method, select_method, mutat_rate)