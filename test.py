test = 'abcdefghi'
test_split = list(test)
result = []
for i in range(len(test)):
    char = test[i]

board = []
for i in [0, 3, 6]:
    board.append([test[n] for n in [i, i+1, i+2]])
print(board)