import random as r

test = [1,2,3,4,5]
x = r.choices(test, weights=(0.1,0.2,0.3,0.2,0.1), k=1)
print(x[0])