import math as m

board = [[1, 2, 0], [0, 1, 2], [0, 0, 0]]
state = '120012000'
choice = 3
print(int(m.floor(choice/3)))
print(int(choice % 3))