class InputPlayer():
    def __init__(self):
        self.player_num = None
        self.player_color = None
    
    def set_player_number(self, player_num):
        self.player_num = player_num
        if self.player_num == 1:
            self.player_color = 'blue'
        elif self.player_num == 2:
            self.player_color = 'red'
    
    def choose_move(self, board, options):
        if len(options) == 1 and options[0][1][0] == 0:
            return options[0]
        print(f'\nYou are player {self.player_num} ({self.player_color})')
        self.print_board(board)
        self.print_options(options)
        move = self.get_valid_input(options)
        return move
        
    def get_valid_input(self, options):
        move_idx = int(input('Input the provided index of the move you wish to play:\n'))
        if move_idx < 0 or move_idx > len(options)-1:
            print('Invalid move, try again')
            return self.get_valid_input(options)
        return options[move_idx]

    def print_board(self, state):
        print("\n  0 1 2 3 4 5 6 7")
        for i in range(8):
            row_to_print = f"{i} "
            for j in range(8):
                elem = state[i][j]
                if elem == 0:  row_to_print += "⬜" if ((i + j) % 2 == 0) else "  "
                if elem == 1:  row_to_print += "🔵"
                if elem == 2:  row_to_print += "🔴"
                if elem == -1: row_to_print += "💙"
                if elem == -2: row_to_print += "❤️ "
            print(row_to_print)
        
    def arr_add(self, arr_1, arr_2):
        if len(arr_1) != len(arr_2):
            print('error in arr_add - input player')
            return
        return [arr_1[i]+arr_2[i] for i in range(len(arr_1))]
    
    def print_options(self, options):
        print('\nPossible moves:')
        for i, move in enumerate(options):
            coord = tuple(move[0])
            translation = move[1]
            new_coord = tuple(self.arr_add(coord, translation))
            if abs(translation[0]) != 2:
                print(f'{i}: {coord} -> {new_coord}')
            else:
                print(f'{i}: {coord} -> {new_coord} (capture)')