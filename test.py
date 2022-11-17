import random, numpy, math, copy

class Buh():
    def __init__(self, x):
        self.x = x

test = [Buh(1),Buh(2),Buh(5),Buh(6),Buh(9)]
test2 = copy.deepcopy(test)
test2[0].x = 5
print(test[0].x)
print(test2[0].x)