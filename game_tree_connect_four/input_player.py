
class InputPlayer():
    def __init__(self):
        self.number = None
    
    def set_player_number(self, num):
        self.number = num
    
    def choose_move(self, board, choices):
        self.print_board(board)
        print(f'Your turn, you are player {self.number}')
        print('Input column number of desired move (starting from 1)')
        
        inp = int(input(''))-1
        if inp not in choices:
            print('Invalid move')
            self.choose_move(board, choices)
        print('\n')
        return inp
    
    def print_board(self, board):
        for i in range(len(board)):
            row = board[i]
            row_string = ''
            for space in row:
                if space == 0:
                    row_string += '_|'
                else:
                    row_string += str(space) + '|'
            print(row_string[:-1])

    def report_winner(self, winner, board):
        self.print_board(board)
        if winner == self.number:
            print('You won')
        elif winner == 3-self.number:
            print('You lost')
        else:
            print('Tie')