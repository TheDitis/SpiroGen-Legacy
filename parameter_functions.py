from matplotlib import cm
import numpy as np

def arc(x: int, b: int) -> int:
    return b - x**2


l = [arc(x, 100) for x in range(-10, 11)]
cmap = cm.get_cmap('viridis')




class V(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        if not isinstance(other, V):
            raise TypeError()
        x = self.x + other.x
        y = self.y + other.y
        return V(x, y)

    def __repr__(self):
        return super().__repr__() + str((self.x, self.y))

    def __str__(self):
        return f'Vector (x={self.x}, y={self.y})'

    def __and__(self, other):
        if np.dot((self.x, self.y), (other.x, other.y)):
            return True
        else:
            return False

class Modifier:
    def __init__(self, params):
        pass

    def __call__(self, vector):
        vector.add


class Grid:
    def __init__(self, n):
        self.grid = np.arange(n, n)

    def __iter__(self, i):
        pass

check = V(2, 5)
print(check)