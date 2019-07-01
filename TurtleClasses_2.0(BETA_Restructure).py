import turtle
import numpy as np
from matplotlib.colors import rgb2hex as pltcolors

color_list = [
        'red', 'crimson', 'orangered', 'darkorange', 'orange', 'gold',
        'yellow', 'greenyellow', 'lawngreen', 'limegreen', 'springgreen',
        'mediumspringgreen', 'aquamarine', 'turquoise', 'aqua',
        'deepskyblue', 'dodgerblue', 'mediumslateblue', 'mediumpurple',
        'blueviolet', 'darkviolet', 'purple', 'mediumvioletred'
    ]


class TransformationMixin:
    def __init__(self, lower_structure):
        self._lower_structure = lower_structure
        self._turt = Turt('asdf')
        self._color_sheme = ('asdf')

    def draw(self, thing):
        self._turt.pendown()
        self._turt(thing)
        self._turt.penup()

    def oscillate(self):


class ConcentricTransform(TransformationMixin):
    def __init__(self, shape, size_gen, center_gen):
        super().__init__(shape)
        self._size_gen = size_gen
        self._center_gen = center_gen

class RadialTransform(TransformationMixin):
    def __init__(self, petal, axes, angle_gen):
        super().__init__(petal)


class PatternMixin:
    def __init__(self):
        pass

class FlowerPattern(PatternMixin):
    def __init__(self, petal_width, petal_angle_gen):
        super().__init__()
        self._shape = Circle(radius)
        self._pattern = RadialTransform(self._shape, petal_angle)
        self._design = GridTransform(self._pattern, dist=10, edge='center')

def torus_transform(pattern, ax1_radius, ax2_radius):
    pass

class SpaceTransform(TransformationMixin, DrawMixin):
    pass

class SphericalTransform(SpaceTransform):
    pass

class TorusTransform(SpaceTransform):
    pass

def draw(pattern)

class PatternMixin

class Turt:

    def __init__(self, color='green', size=1, speed=10, xy=[0, 0], heading=0):
        self._color = color
        self._size = size
        self._speed = speed
        self._heading = heading
        self.turtle = turtle.Turtle()
        self.turtle.color('magenta')
        if isinstance(self._color, str):
            self.turtle.color(self._color)
        self.turtle.pensize(self._size)
        self.turtle.speed(self._speed)
        self.turtle.penup()
        self.turtle.goto(xy[0], xy[1])
        self.turtle.seth(self._heading)
        self._xy = self.turtle.pos()
        self.turtle.pendown()

    @property
    def color(self):
        print("color getter method called")
        return self._color

    @property
    def pensize(self):
        return self._size

    @property
    def speed(self):
        return self._speed

    @property
    def heading(self):
        return self._heading

    @property
    def position(self):
        return self._xy

    @color.setter
    def color(self, col):
        # print("color setter method called")
        self._color = col
        self.turtle.color(self._color)

    @pensize.setter
    def pensize(self, size):
        print("getter method called")
        self._size = size
        self.turtle.pensize(self._size)

    @speed.setter
    def speed(self, spd):
        self._speed = spd
        self.turtle.speed(self._speed)

    @heading.setter
    def heading(self, dir):
        self._heading = dir
        self.turtle.seth(self._heading)

    @position.setter
    def position(self, xy):
        self.turtle.penup()
        self._xy = xy
        self.turtle.goto(xy[0], xy[1])
        self.turtle.pendown()

    def color_gen(self, i):
        if isinstance(self._color, str):
            color_list = [self._color]
        else:
            color_list = [x for x in self._color]
        ind = (i + 1) % len(color_list)
        return color_list[ind]

    def forward(self, dist):
        self.turtle.forward(dist)

    def up(self, dist):
        self.turtle.seth(90)
        self.turtle.forward(dist)


class ColorCycle:
    def __init__(self, colorlist, turt):
        self._colorlist = colorlist
        self._turt = turt

    def colorsetter(self, ind):
        length = len(self._colorlist)
        modind = ind % length
        print('colorsetter called')
        print(modind)
        self._turt.color = self._colorlist[modind]
        return self._colorlist[modind]


class Forward:
    def __init__(self, turt, fwd):
        self._turt = turt
        self._fwd = fwd
        self._turt.turtle.forward(self._fwd)


class Turn:
    def __init__(self, turt, angle, curve=None, curvesize=5):
        self._turt = turt
        self._angle = angle
        self._curve = curve
        self._curvesize = curvesize

    def go(self):
        if self._curve is None:
            self._turt.turtle.right(self._angle)
        else:
            reps = round(abs(self._angle) / 10)
            turn = abs(self._angle) / reps
            for j in range(reps):
                self._turt.turtle.forward(self._curvesize)
                if self._angle < 0:
                    self._turt.turtle.left(turn)
                else:
                    self._turt.turtle.right(turn)

        # if curve is None:
        #     self._turt.turtle.right(angle)
        # else:
        #     reps = round(abs(angle) / 10)
        #     turn = abs(angle) / reps
        #     for j in range(reps):
        #         self._turt.turtle.forward(curvesize)
        #         if angle < 0:
        #             self._turt.turtle.left(turn)
        #         else:
        #             self._turt.turtle.right(turn)


class SpiralPattern:

    def __init__(self, turt, size, angle1, angle2=None, angle3=None, angle4=None, turncycle=0, jank=None, colors=None):

        self._turt = turt
        self._size = size
        self._angle1 = angle1
        self._angle2 = angle2
        self._angle3 = angle3
        self._angle4 = angle4
        self._turncycle = turncycle
        self._jank = jank
        self._colorlist = colors
        if isinstance(self._colorlist, list):
            self._color = colors[0]
        elif isinstance(self._colorlist, str):
            self._color = colors
        self._turnlist = [self._angle1, self._angle2, self._angle3, self._angle4]
        self._nTurns = [t for t in self._turnlist if t is not None]
        self._turt.position = [-(size / 2), (size / 2)]
        self._startpos = self._turt.position

    def go(self):
        if len(self._nTurns) == 1:
            self.oneangle()
        elif len(self._nTurns) == 2:
            self.twoangle()
        elif len(self._nTurns) == 3:
            self.threeangle()
        elif len(self._nTurns) == 4:
            self.fourangle()

    def oneangle(self):

        for k in range(100):

            ColorCycle(self._colorlist, self._turt).colorsetter(k)

            self.anglego(0)
            if self.checkplace():
                self._turt.position = self._startpos
                break

    def twoangle(self):

        for k in range(100):

            ColorCycle(self._colorlist, self._turt).colorsetter(k)

            self.anglego(0)
            if self._turncycle == 1 or self._turncycle == 5:
                self.anglego(0)

            self.anglego(1)
            if self._turncycle == 2 or self._turncycle == 5:
                self.anglego(1)

            if self._jank is not None:
                Forward(self._turt, self._jank)

            if self.checkplace():
                self._turt.position = self._startpos
                break

    def threeangle(self):

        for k in range(100):

            ColorCycle(self._colorlist, self._turt).colorsetter(k)

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
                Forward(self._turt, self._jank)

            if self.checkplace():
                self._turt.position = self._startpos
                break

    def fourangle(self):

        for k in range(100):

            ColorCycle(self._colorlist, self._turt).colorsetter(k)

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
                Forward(self._turt, self._jank)

            if self.checkplace():
                self._turt.position = self._startpos
                break

    def anglego(self, n):
        Forward(self._turt, self._size)
        self._nTurns[n].go()

    def checkplace(self):
        sx, sy = round(self._startpos[0]), round(self._startpos[1])
        current = self._turt.turtle.pos()
        x, y = round(current[0]), round(current[1])
        if sx == x and sy == y:
            return True
        else:
            return False

    def center(self):
        pass

    # def colorsetter(self, ind):
    #     length = len(self._colorlist)
    #     modind = ind % length
    #     print('colorsetter called')
    #     print(modind)
    #     self._turt.color = self._colorlist[modind]


speed = 10
turtle.bgcolor('black')
jimmothy = Turt()
turtle.tracer(speed, 1)
jimmothy.turtle.hideturtle()


angle1 = 125
size = 240

turn1 = Turn(jimmothy, angle=125, curve=10, curvesize=3)
turn2 = Turn(jimmothy, angle=-(360 - 125), curve=10, curvesize=3)
turn3 = Turn(jimmothy, angle=160, curve=10, curvesize=3)
turn4 = Turn(jimmothy, angle=45, curve=10, curvesize=3)

simplespiral = SpiralPattern(jimmothy, size, turn1, turn2, turncycle=0, colors=color_list)
simplespiral.go()




# for i in range(100):
#     Forward(jimmothy, 120)
#     turn1.go()
#     Forward(jimmothy, 120)
#     turn1.go()
#     Forward(jimmothy, 120)
#     turn2.go()



turtle.exitonclick()