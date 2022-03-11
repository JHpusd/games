class PlaceHolder():
    def __init__(self, x):
        self.x = x

a = PlaceHolder(1)
b = PlaceHolder(2)
c = PlaceHolder(3)

test = [b,a,c]
func = lambda i: i.x
test.sort(key=func, reverse=True)
print([item.x for item in test])