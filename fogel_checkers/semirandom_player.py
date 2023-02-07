import random

class SemirandomPlayer():
    def __init__(self):
        self.player_num = None
    
    def set_player_number(self, player_num):
        self.player_num = player_num
    
    def choose_move(self, board, options):
        all_translations = [move[1] for move in options]
        capt_idxs = []
        for i, translation in enumerate(all_translations):
            if abs(translation[0]) == 2:
                capt_idxs.append(i)
        if len(capt_idxs) == 0:
            return random.choice(options)
        else:
            rand_idx = random.choice(capt_idxs)
            return options[rand_idx]
