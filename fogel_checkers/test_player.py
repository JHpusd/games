class TestPlayer():
    def __init__(self):
        self.player_num = None
    
    def set_player_number(self, player_num):
        self.player_num = player_num
    
    def choose_move(self, board, options):
        return options[0]
