from nn_player import *
from np_player import *
import sys
sys.path.append('game_tree_ttt')
from tic_tac_toe import *

class EvolvingNetPlayers():
    def __init__(self, init_players):
        self.num_players = init_players
        self.players = []
        self.gen_num = 0
        self.prev_gen_scores = []
    
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
            for _ in range(32):
                game = TicTacToe(players)
                game.run_to_completion()
                if game.winner == 1:
                    player.score += 1
                elif game.winner == 2:
                    player.score -= 10
    
    def get_top_half(self):
        if len(self.players) == 0:
            self.init_first_gen()
        self.run_games()
        self.players.sort(key=lambda p: p.score, reverse=True)
        self.prev_gen_scores = [p.score for p in self.players]
        return self.players[:int(self.num_players/2)]
    
    def reset_scores(self, players):
        for player in players:
            player.score = 0
    
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

enp = EvolvingNetPlayers(50)
enp.init_first_gen()
print('initialized first gen')
enp.make_new_gen()
print(sum(enp.prev_gen_scores)/len(enp.prev_gen_scores))
enp.make_new_gen()
print(sum(enp.prev_gen_scores)/len(enp.prev_gen_scores))
enp.make_new_gen()
print(sum(enp.prev_gen_scores)/len(enp.prev_gen_scores))