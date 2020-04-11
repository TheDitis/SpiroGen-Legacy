from Pattern_old import Pattern
import turtle

default_color_list = [
    'red', 'crimson', 'orangered', 'darkorange', 'orange', 'gold',
    'yellow', 'greenyellow', 'lawngreen', 'limegreen', 'springgreen',
    'mediumspringgreen', 'aquamarine', 'turquoise', 'aqua',
    'deepskyblue', 'dodgerblue', 'mediumslateblue', 'mediumpurple',
    'blueviolet', 'darkviolet', 'purple', 'mediumvioletred'
]


class RadialAngularPattern(Pattern):

    def __init__(self, size, angles=[[125, 3]], turncycle=0, jank=None,
                 colors=default_color_list, pensize=1, position=[0, 0], showcenter=False, penup=False):
        self._size = size
        self._turns = angles
        self._turncycle = turncycle
        self._jank = jank
        self._position = position
        self._colors = colors
        self._turnlist = []
        if isinstance(angles, int):
            self._turns = [[angles]]
            angles = [[angles]]
        if isinstance(angles[0], int):
            self._turns = [angles]
        self.goto(penup=True)
        self._startpos = turtle.pos()
        self._list = self.draw(penup=True)
        super().__init__(self._list, self._colors, pensize, self._startpos)

        ## leaving out auto-centering for now
        # self.list = self.center(showcenter=showcenter)
        # super().__init__(self.list, self._colors, pensize, self._startpos)
        # if showcenter:
        #     self.dot((0, 0), 5)

    @property
    def size(self):
        return self._size

    @property
    def turns(self):
        return self._turns

    @property
    def turncycle(self):
        return self._turncycle

    @property
    def jank(self):
        return self._jank

    @turncycle.setter
    def turncycle(self, value):
        pass

    def draw(self, penup=False):
        turtle.pendown()
        if penup:
            turtle.penup()
            turtle.speed(10)
            turtle.tracer(1000, 1)
        turtle.begin_poly()
        if len(self._turns) == 1:
            self.oneangle()
        elif len(self._turns) == 2:
            self.twoangle()
        elif len(self._turns) == 3:
            self.threeangle()
        elif len(self._turns) == 4:
            self.fourangle()
        turtle.end_poly()
        lst = turtle.get_poly()
        lst = [tuple(xy) for xy in lst]
        if penup:
            turtle.speed(100)
            turtle.tracer(10000, 1)
        return lst

    def oneangle(self):

        for k in range(10000):

            self.colorcycle(k)

            self.anglego(0)
            if self.checkplace():
                turtle.dot(1)
                turtle.goto(self._startpos)
                turtle.hideturtle()
                break

    def twoangle(self):

        for k in range(10000):

            self.colorcycle(k)

            self.anglego(0)
            if self._turncycle == 1 or self._turncycle == 5:
                self.anglego(0)

            self.anglego(1)
            if self._turncycle == 2 or self._turncycle == 5:
                self.anglego(1)

            if self._jank is not None:
                turtle.forward(self._jank)

            if self.checkplace():
                turtle.dot(1)
                turtle.goto(self._startpos)
                turtle.hideturtle()
                break

    def threeangle(self):

        for k in range(10000):

            self.colorcycle(k)

            self.anglego(0)
            if self._turncycle == 1 or self._turncycle == 5:
                self.anglego(0)

            self.anglego(1)
            if self._turncycle == 2 or self._turncycle == 5 or self._turncycle == 6:
                self.anglego(1)

            self.anglego(2)
            if self._turncycle == 3 or self._turncycle == 6:
                self.anglego(2)

            if self._jank is not None:
                turtle.forward(self._jank)

            if self.checkplace():
                turtle.dot(1)
                turtle.goto(self._startpos)
                turtle.hideturtle()
                break

    def fourangle(self):

        for k in range(10000):

            self.colorcycle(k)

            self.anglego(0)
            if self._turncycle == 1 or self._turncycle == 5 or self._turncycle == 8:
                self.anglego(0)

            self.anglego(1)
            if self._turncycle == 2 or self._turncycle == 5 or self._turncycle == 6 or self._turncycle == 8 or self._turncycle == 9:
                self.anglego(1)

            self.anglego(2)
            if self._turncycle == 3 or self._turncycle == 6 or self._turncycle == 7 or self._turncycle == 8 or self._turncycle == 9:
                self.anglego(2)

            self.anglego(3)
            if self._turncycle == 4 or self._turncycle == 7 or self._turncycle == 9:
                self.anglego(3)

            if self._jank is not None:
                turtle.forward(self._jank)

            if self.checkplace():
                turtle.dot(1)
                turtle.goto(self._startpos)
                turtle.hideturtle()
                break

    def anglego(self, n):
        turtle.forward(self._size)
        self.turn(*self._turns[n])

    def checkplace(self):

        sx, sy = round(self._startpos[0]), round(self._startpos[1])
        current = turtle.pos()
        x, y = round(current[0]), round(current[1])
        if sx == x and sy == y:
            return True
        else:
            return False

    def capturepath(self, penup=True):
        if penup:
            turtle.penup()
            turtle.tracer(1000, 1)
            turtle.speed(10)
        # self.goto(penup=penup)
        turtle.begin_poly()
        if len(self._turns) == 1:
            self.oneangle()
        elif len(self._turns) == 2:
            self.twoangle()
        elif len(self._turns) == 3:
            self.threeangle()
        elif len(self._turns) == 4:
            self.fourangle()
        turtle.end_poly()
        lst = turtle.get_poly()
        lst = [tuple(xy) for xy in lst]
        turtle.pendown()
        if penup:
            turtle.tracer(1000, 1)
            turtle.speed(10)
        return lst

    ## Probably leaving this off for now
    # def center(self, showcenter=False):
    #     precenter = Analyze(self.list, self._ldepth).center(show=showcenter)
    #     newlist = [(xy[0] - precenter[0], xy[1] - precenter[1]) for xy in self.list]
    #     # self._startpos = (self.position[0] - precenter[0], self.position[1] - precenter[1])
    #     return newlist