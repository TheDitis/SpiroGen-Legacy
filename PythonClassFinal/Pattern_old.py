import turtle


class Pattern:

    def __init__(self, lst,  colors='white', pensize=1,
                 position=[0, 0]):
        self._list = lst
        self._position = position
        if isinstance(colors, str):
            colors = [colors]
        self._colors = colors
        self._ldepth = self.set_depth()
        turtle.pensize(pensize)

    def __repr__(self):
        lst = list(self._list)
        return lst

    def __str__(self):
        return str(self._list)

    def __getitem__(self, index):
        return self._list[index]

    def __setitem__(self, index, value):
        self._list[index] = value

    def __len__(self):
        return len(self._list)

    def drawpath(self, penup=False):
        self.goto(self._list[0], penup=True)
        turtle.setheading(0)
        ldepth = self._ldepth
        if penup is False:
            turtle.pendown()
        if ldepth == 1:
            self.simpledraw()
            self.dot(turtle.pos(), 1)
        elif ldepth == 2:
            self.lvl2draw()
        elif ldepth == 3:
            self.lvl2()

    def capture_path(self, penup=True):
        self.goto(penup=penup)
        ldepth = self._ldepth
        if penup:
            turtle.penup()
        turtle.begin_poly()
        if ldepth == 1:
            self.simpledraw
        if ldepth == 2:
            self.lvl2draw
        if ldepth == 3:
            self.lvl2
        turtle.end_poly()
        lst = turtle.get_poly()
        lst = [tuple(xy) for xy in lst]
        return lst

    def set_depth(self):
        if isinstance(self._list[0], tuple) \
                and isinstance(self._list[0][0], (int, float)):
            return 1
        elif isinstance(self._list[0], list):
            if isinstance(self._list[0][0], list):
                return 3
            else:
                return 2

    def simpledraw(self):
        # print('lvl1')
        for ind in range(len(self._list)):
            self.colorcycle(ind)
            turtle.goto(self._list[ind])

    def lvl2draw(self):
        # print('lvl2')
        for lst in self._list:
            for ind in range(len(lst)):
                self.colorcycle(ind)
                turtle.goto(lst[ind])

    def lvl3draw(self):
        # print('lvl3')
        for group in self._list:
            for lst in group:
                for ind in range(len(lst)):
                    self.colorcycle(ind)
                    turtle.goto(lst[ind])

    def goto(self, coord=None, penup=False):
        if penup:
            turtle.penup()
        else:
            turtle.pendown()
        if coord is None:
            turtle.goto(self._position)
        else:
            turtle.goto(coord)
        turtle.pendown()

    def colorcycle(self, ind):
        length = len(self._colors)
        modind = ind % length
        turtle.color(self._colors[modind])
        return self._colors[modind]

    # @staticmethod
    def dot(self, point, size=10):
        turtle.color('white')
        turtle.penup()
        self.goto(point, penup=True)
        turtle.pendown()
        turtle.dot(size)

    @staticmethod
    def turn(angle, curve=0):
        if curve is None or curve == 0:
            if angle < 0:
                turtle.left(abs(angle))
            else:
                turtle.right(angle)
        else:
            reps = round(abs(angle) / 10)
            turn = abs(angle) / reps
            for j in range(reps):
                turtle.forward(curve)
                if angle < 0:
                    turtle.left(turn)
                else:
                    turtle.right(turn)