from nn_player import *
from np_player import *
import sys, pickle, copy
import random as r
import matplotlib.pyplot as plt
sys.path.append('game_tree_ttt')
from tic_tac_toe import *

class EvolvingNetPlayers():
    def __init__(self, init_players, num_games=32):
        self.num_players = init_players
        self.players = []
        self.gen_num = 0
        self.prev_gen_payoffs = []
        self.num_games = num_games
    
    def init_first_gen(self):
        self.players = [NeuralNetPlayer() for _ in range(self.num_players)]
        for player in self.players:
            player.initialize_net()
        self.gen_num += 1
    
    def run_games(self, players=None):
        if players == None:
            players = self.players
        for player in self.players:
            players = [player, NearPerfectPlayer()]
            for _ in range(self.num_games):
                game = TicTacToe(players)
                game.run_to_completion()
                if game.winner == 1:
                    player.payoff_score += 1
                elif game.winner == 2:
                    player.payoff_score -= 10

    def run_second_eval(self, players=None):
        if players == None:
            players = self.players
        for i,player in enumerate(self.players):
            other_player_idx = [idx for idx in range(len(self.players)) if idx!=i]
            for _ in range(10):
                rand_idx = r.choice(other_player_idx)
                rand_player = self.players[rand_idx]
                if player.payoff_score > rand_player.payoff_score:
                    player.eval_score += 1
    
    def get_top_half(self):
        if len(self.players) == 0:
            self.init_first_gen()
        self.run_games()
        self.run_second_eval()
        self.players.sort(key=lambda p: p.eval_score, reverse=True)
        self.prev_gen_payoffs = [p.payoff_score for p in self.players]
        return self.players[:int(self.num_players/2)]

    def reset_scores(self, players):
        for player in players:
            player.payoff_score = 0
            player.eval_score = 0
    
    def make_new_gen(self):
        top_half = self.get_top_half()
        new_players = [player.replicate() for player in top_half]
        new_gen = top_half + new_players
        self.reset_scores(new_gen)
        self.players = new_gen
        assert len(self.players) == self.num_players, "len error making new gen"
        self.gen_num += 1

    def progress_n_gens(self, n):
        for _ in range(n):
            self.make_new_gen()
    
    def get_net_info(self, player):
        return {'net_obj': player.net, 'net_info':player.net.__dict__}
    
    def gen_copy(self):
        return copy.deepcopy(self.players)

gens = [i for i in range(100)]
max_payoffs = [0 for _ in range(100)]

file = open('nn_players.pickle', 'wb')
for i in range(2): # make 20
    enp = EvolvingNetPlayers(50)
    enp.init_first_gen()
    print(f'trial {i+1}')
    print('initialized first gen')
    for gen_id in range(2): # make 100 or 50
        enp.make_new_gen()
        max_payoff = max(enp.prev_gen_payoffs)
        print(f'trial {i+1} gen {enp.gen_num-1} max payoff: {max_payoff}')
        max_payoffs[gen_id] += max_payoff/20
    enp.get_top_half() # should score newest gen
    pickle.dump(enp.gen_copy(), file)
file.close()
print('finished trials, making plot')

# final gen players stored iteratively, load iteratively
# with open/read, while true, get that gen players, stop if eof error

plt.style.use('bmh')
plt.plot(gens, max_payoffs)
plt.xlabel('gen #')
plt.ylabel('avg max payoff')
plt.savefig('evolving_fogel_nn_players.png')
print('finished plotting')

# use pickle to save final gens over each of the 20 trials

'''
enp.make_new_gen()
print(sum(enp.prev_gen_payoffs)/len(enp.prev_gen_payoffs))
enp.make_new_gen()
print(sum(enp.prev_gen_payoffs)/len(enp.prev_gen_payoffs))
enp.make_new_gen()
print(sum(enp.prev_gen_payoffs)/len(enp.prev_gen_payoffs))
'''
# run for 800 gens, make curve
# make method that gets max total payoff player from gen
# get player info for best player