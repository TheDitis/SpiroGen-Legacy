import turtle
import random
import itertools
import numpy as np
from math import *
from matplotlib.colors import rgb2hex as pltcolors




color_list = [
    'red', 'crimson', 'orangered', 'darkorange', 'orange', 'gold',
    'yellow', 'greenyellow', 'lawngreen', 'limegreen', 'springgreen',
    'mediumspringgreen', 'aquamarine', 'turquoise', 'aqua',
    'deepskyblue', 'dodgerblue', 'mediumslateblue', 'mediumpurple',
    'blueviolet', 'darkviolet', 'purple', 'mediumvioletred'
]


def setup(genspeed=1, backgroundcolor='black', hide=False):
    turtle.setup(1920, 1200)  # Laptop screen
    # turtle.setup(3840, 2200)     # 4K screen
    turtle.color('white')
    turtle.tracer(genspeed, 1)
    turtle.speed(speed)
    turtle.bgcolor(backgroundcolor)
    turtle.pensize(1)
    if hide:
        turtle.hideturtle()


class Analyze:
    def __init__(self, funclist=[[]], ldepth=1):
        # if not isinstance(funclist[0], list):
        #     funclist = [funclist]
        self.funclist = funclist
        self.coordlist = []
        self.ldepth = ldepth

    # def crosspoint(self, xtolerance=0.2, ytolerance=10, show=False):
    #     biglist = self.funclist
    #     listnum = len(biglist)
    #     listsize = len(biglist[0])
    #     ypoints = []
    #     points = []
    #
    #     for n in range(listnum):
    #         for i in range(listsize):
    #             ind = n + 1
    #             if n == listnum - 1:
    #                 ind = 0
    #             if abs(biglist[n][i][0] - biglist[ind][i][0]) < xtolerance:
    #                 ypoints.append(biglist[n][i])
    #
    #     for n in range(len(ypoints)):
    #         ind = n + 1
    #         if n == len(ypoints) - 1:
    #             ind = 0
    #         if abs(ypoints[n][1] - ypoints[ind][1]) < ytolerance:
    #             points.append(ypoints[n])
    #     self.coordlist = points
    #     avg = self.avgcoord(points)
    #     if show is True:
    #         self.drawdots(points)
    #         self.drawdots(avg)
    #     if len(points) == 0:
    #         print('No crosspoint canidates were found. Returning None')
    #     return points, avg

    def center(self, show=False):

        avgs = []
        if self.ldepth == 1:
            for i in self.funclist:
                avgs.append(self.avgcoord([i]))
            center = self.avgcoord(avgs)
        elif self.ldepth >= 2:
            print('ldepth greater than 1 not set in centering method within analyze class')
        if show is True:
            self.drawdots(center)
        return center

    # def center2(self, show=False):
    #     fulllist = []
    #     for i in self.funclist:
    #         fulllist = fulllist + i
    #     center = self.avgcoord(fulllist)
    #     if show is True:
    #         self.drawdots(center)
    #     return center
    #
    # def distancelist(self):
    #     coords = self.funclist
    #     distlist = []
    #     xydistlist = []
    #     for i in range(len(coords)):
    #         i2 = ((i + 1) % len(coords))
    #         dist, xdist, ydist = self.distance(coords[i], coords[i2], seperate=True)
    #         # xdist = round(coords[i][0] - coords[i2][0], 6)
    #         # ydist = round(coords[i][1] - coords[i2][1], 6)
    #         # dist = round(sqrt((xdist ** 2) + (ydist ** 2)), 2)
    #         distlist.append(dist)
    #         xydistlist.append((xdist, ydist))
    #     return distlist, xydistlist
    #
    @staticmethod
    def drawdots(points, size=10):
        turtle.color('white')
        if isinstance(points, tuple):
            points = [points]
        if isinstance(points, list):
            startpos = turtle.pos()
            for i in points:
                turtle.penup()
                turtle.goto(i)
                turtle.pendown()
                turtle.dot(size)
            turtle.penup()
            turtle.goto(startpos)
        turtle.pendown()
    #
    #
    # @staticmethod
    # def Oavgcoord(coords):
    #     # print(coords)
    #     xs, ys = [xy[0] for xy in coords], [xy[1] for xy in coords]
    #     if len(xs) and len(ys) > 0:
    #         xavg, yavg = sum(xs)/len(xs), sum(ys)/len(ys)
    #         avgcoord = (xavg, yavg)
    #         return avgcoord
    #     else:
    #         return None

    def avgcoord(self, coords):
        if self.ldepth == 1:
            xs, ys = [xy[0] for xy in coords], [xy[1] for xy in coords]
            if len(xs) and len(ys) > 0:
                xavg, yavg = sum(xs) / len(xs), sum(ys) / len(ys)
                avgcoord = (xavg, yavg)
                return avgcoord
            else:
                return None
        # elif self.ldepth == 2:
        #     for point in coords:
        #         xs, ys = [xy[0] for xy in point], [xy[1] for xy in point]
        #         if len(xs) and len(ys) > 0:
        #             xavg, yavg = sum(xs) / len(xs), sum(ys) / len(ys)
        #             avgcoord = (xavg, yavg)
        #             return avgcoord
        #         else:
        #             return None


    @staticmethod
    def distance(a, b, seperate=False):
        xdist = round(a[0] - b[0], 6)
        ydist = round(a[1] - b[1], 6)
        dist = round(sqrt((xdist ** 2) + (ydist ** 2)), 2)
        if seperate is True:
            return dist, xdist, ydist
        else:
            return dist


class ColorScheme:

    def __init__(self, colordict, ncolors=50, symetrical=False):
        self.ncolors = ncolors
        self._symetrical = symetrical
        if symetrical is True:
            self.ncolors = ncolors // 2
        self.keylist = ['r', 'g', 'b']
        self.colors = colordict
        self.check_inputs()
        self.rlist = self.colors['r']
        self.glist = self.colors['g']
        self.blist = self.colors['b']
        self.rgbdivs = {}
        self.roundto = 3
        self.set_transition_divisions()
        self.fades = self.set_fades()
        self.rgbcolors = self.join_colors()
        self.rgb0to1 = self.scale0to1(self.rgbcolors)
        self.hex = []
        self.hexconvert()
        if symetrical is True:
            self.rgb0to1 = self.rgb0to1 + self.rgb0to1[::-1]
            self.rgb0to1 = self.rgb0to1 + self.rgb0to1[::-1]
            self.hex = self.hex + self.hex[::-1]

    def __repr__(self):
        hexlist = self.hex
        return hexlist

    def __str__(self):
        return str(self.colors)

    def __getitem__(self, index):
        return self.hex[index]

    def __setitem__(self, index, value):
        self.hex[index] = value

    def __len__(self):
        return len(self.hex)

    def setup(self):
        self.check_inputs()
        self.rlist = self.colors['r']
        self.glist = self.colors['g']
        self.blist = self.colors['b']
        self.rgbdivs = {}
        self.roundto = 3
        self.set_transition_divisions()
        self.fades = self.set_fades()
        self.rgbcolors = self.join_colors()
        self.rgb0to1 = self.scale0to1(self.rgbcolors)
        self.hex = []
        self.hexconvert()
        if self._symetrical is True:
            self.rgb0to1 = self.rgb0to1 + self.rgb0to1[::-1]
            self.rgb0to1 = self.rgb0to1 + self.rgb0to1[::-1]
            self.hex = self.hex + self.hex[::-1]

    def check_inputs(self):
        for k in self.keylist:
            color = self.colors[k]
            if not isinstance(color, list):
                print('Inputs must be in the form of a list')
            if isinstance(color[0], list):
                for l in range(len(color)):
                    if len(color[l]) == 1:
                        self.colors[k][l] = [color[l][0], color[l][0]]
                        print('Revising short list', self.colors[k][l])
                    if len(color[l]) > 2:
                        print('Color value lists can have no more than '
                              '2 numbers')
                        print(color[l], 'needs to be revised')
                        raise ValueError
                self.convert2list()

    def convert2list(self):
        for k in self.keylist:
            newlist = []
            color = self.colors[k]
            for i in range(len(color)):
                if i < len(color) - 1:
                    newlist.append(color[i][0])
                elif i == len(color) - 1:
                    newlist.append(color[i][0])
                    newlist.append(color[i][1])
            self.colors[k] = newlist

    def set_transition_divisions(self):
        rlen = len(self.rlist) - 1
        glen = len(self.glist) - 1
        blen = len(self.blist) - 1
        rdivs = [self.ncolors // rlen] * rlen
        gdivs = [self.ncolors // glen] * glen
        bdivs = [self.ncolors // blen] * blen
        rgbdivs = {'r': rdivs, 'g': gdivs, 'b': bdivs}
        # Adding or subtracting from sections for divisibility
        for k in self.keylist:
            if sum(rgbdivs[k]) != self.ncolors:
                diff = self.ncolors - sum(rgbdivs[k])
                if diff < 0:
                    f = -1
                elif diff > 0:
                    f = 1
                for l in range(diff):
                    rgbdivs[k][-(l + 1)] += f
        self.rgbdivs = rgbdivs

    def set_fades(self):
        rgbdivs = self.rgbdivs
        fades = {'r': [], 'g': [], 'b': []}
        # rdivs, gdivs, bdivs = rgbdivs['r'], rgbdivs['g'], rgbdivs['b'],
        decimal = self.roundto
        for k in self.keylist:
            clist = self.colors[k]
            for i in range(len(clist) - 1):
                first, last = clist[i], clist[i + 1]
                section = np.linspace(first, last, rgbdivs[k][i])
                section = (np.around(section, decimal)).tolist()
                fades[k] = fades[k] + section
        return fades

    def join_colors(self):
        rgb = [(c[0], c[1], c[2]) for c in
               zip(self.fades['r'], self.fades['g'], self.fades['b'])]
        return rgb

    def scale0to1(self, rgblist):
        newlist = []
        roundto = self.roundto
        for col in rgblist:
            scaledval = [round(i / 255, roundto) for i in col]

            newlist.append(scaledval)
        return newlist

    def hexconvert(self):
        for i in self.rgb0to1:
            hexcol = pltcolors(i)
            self.hex.append(hexcol)

    def shiftlightness(self, delta):
        newcolors = {'r': [], 'g': [], 'b': []}
        for k in self.keylist:
            for val in self.colors[k]:
                newval = val + delta
                if newval > 255:
                    newval = 255
                elif newval < 0:
                    newval = 0
                newcolors[k].append(newval)
        self.colors = newcolors
        self.hexconvert()
        self.setup()

    def ramplightness(self, amt, direction=0, goto_percentage=100):
        if goto_percentage > 100 or goto_percentage < 0:
            print('goto_percentage must be an integer between 0 and 100')
        if direction != 0 and direction != 1:
            print('direction must be 0 (altering beginning of list '
                  'more than end, or 1 for the opposite.')
            raise ValueError
        goto = goto_percentage
        for k in self.keylist:
            colorvals = self.colors[k]
            scope = (len(colorvals) * goto) // 100
            sublist = np.linspace(amt, 0, scope)
            if True:
                for ind in range(len(colorvals)):
                    ind2 = ind
                    if direction == 1:
                        ind = -(ind + 1)
                    if ind2 < len(sublist):
                        self.colors[k][ind] += sublist[ind2]
                        if self.colors[k][ind] < 0:
                            self.colors[k][ind] = 0
                        elif self.colors[k][ind] > 255:
                            self.colors[k][ind] = 255
        self.hexconvert()
        self.setup()


class Pattern:

    def __init__(self, lst,  colors, pensize=1, position=[0, 0]):
        self.list = lst
        self.position = position
        self.colors = colors
        self.ldepth = self.set_depth()
        turtle.pensize(pensize)

    def __repr__(self):
        lst = list(self.list)
        return lst

    def __str__(self):
        return str(self.list)

    def __getitem__(self, index):
        return self.list[index]

    def __setitem__(self, index, value):
        self.list[index] = value

    def __len__(self):
        return len(self.list)

    def drawpath(self, penup=False):
        self.goto(penup=True)
        turtle.setheading(0)
        ldepth = self.ldepth
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
        ldepth = self.ldepth
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

    def Oset_depth(self):
        if isinstance(self.list[0], tuple) and isinstance(self.list[0][0], (int, float)):
            self.ldepth = 1
        elif isinstance(self.list[0], list):
            self.ldepth = 2
            if isinstance(self.list[0][0], list):
                self.ldepth = 3

    def set_depth(self):
        if isinstance(self.list[0], tuple) and isinstance(self.list[0][0], (int, float)):
            return 1
        elif isinstance(self.list[0], list):
            if isinstance(self.list[0][0], list):
                return 3
            else:
                return 2

    def simpledraw(self):
        print('lvl1')
        for ind in range(len(self.list)):
            self.colorcycle(ind)
            turtle.goto(self.list[ind])

    def lvl2draw(self):
        print('lvl2')
        for lst in self.list:
            for ind in range(len(lst)):
                self.colorcycle(ind)
                turtle.goto(lst[ind])

    def lvl3draw(self):
        print('lvl3')
        for group in self.list:
            for lst in group:
                for ind in range(len(lst)):
                    self.colorcycle(ind)
                    turtle.goto(lst[ind])

    def goto(self, coord=None, penup=False):
        turtle.pendown()
        if penup:
            turtle.penup()
        if coord is None:
            turtle.goto(self.position)
        else:
            turtle.goto(coord)
        turtle.pendown()

    def colorcycle(self, ind):
        length = len(self.colors)
        modind = ind % length
        turtle.color(self.colors[modind])
        return self.colors[modind]

    @staticmethod
    def dot(point, size=10):
        turtle.color('white')
        turtle.penup()
        turtle.goto(point)
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


class RadialAngularPattern(Pattern):

    def __init__(self, size, angles=[[125, 3]], turncycle=0, jank=None,
                 colors=color_list, pensize=1, position=[0, 0], showcenter=False, penup=False):
        self._size = size
        self._turns = angles
        self._turncycle = turncycle
        self._jank = jank
        self.position = position
        self.colors = colors
        self._turnlist = []
        if isinstance(angles, int):
            self._turns = [[angles]]
            angles = [[angles]]
        if isinstance(angles[0], int):
            self._turns = [angles]
        self.goto(penup=True)
        self._startpos = turtle.pos()
        self.list = self.draw(penup=True)
        super().__init__(self.list, self.colors, pensize, self._startpos)
        self.center = self.center(showcenter=showcenter)
        self.list = self.draw(penup=penup)
        super().__init__(self.list, self.colors, pensize, self._startpos)


    def draw(self, penup=False):
        turtle.pendown()
        if penup:
            turtle.penup()
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
            turtle.tracer(drawspeed, 1)
            turtle.speed(speed)
        return lst

    def center(self, showcenter=True):
        precenter = Analyze(self.list, self.ldepth).center(show=True)
        return precenter




# class ORadialAngularPattern(Pattern):
#
#     def __init__(self, size, angles=[[125, 3]], turncycle=0, jank=None,
#                  colors=color_list, pensize=1, position=[0, 0], showcenter=False):
#         self._size = size
#         self._angles = angles
#         self._turncycle = turncycle
#         self._jank = jank
#         self.position = position
#         if isinstance(colors, str):
#             colors = [colors]
#         self.colors = colors
#         self._turnlist = []
#         if isinstance(angles, int):
#             self._angles = [[angles]]
#             angles = [[angles]]
#         if isinstance(angles[0], int):
#             self._angles = [angles]
#         for i in range(len(self._angles)):
#             self.create_turns(i)
#         self._turns = [t for t in self._turnlist if t is not None]
#
#         self._startpos = turtle.pos()
#         self.goto()
#         self.list = self.capturepath()
#         self.centeredlist = []
#         # self.center(showcenter=showcenter)
#         self.list = self.capturepath()
#         super().__init__(self.list, self.colors, pensize, self._startpos)
#
#     # def create_turns(self, n):
#     #     tparams = self._angles[n]
#     #     if isinstance(tparams, float):
#     #         tparams = [tparams]
#     #     if n == 0:
#     #         self._turnlist.append(tparams)
#     #     elif n == 1:
#     #         self._turnlist.append(tparams)
#     #     elif n == 2:
#     #         self._turnlist.append(tparams)
#     #     elif n == 3:
#     #         self._turnlist.append(tparams)
#
#     def draw(self, capture=True):
#         turtle.begin_poly()
#         if len(self._turns) == 1:
#             self.oneangle()
#         elif len(self._turns) == 2:
#             self.twoangle()
#         elif len(self._turns) == 3:
#             self.threeangle()
#         elif len(self._turns) == 4:
#             self.fourangle()
#         turtle.end_poly()
#         lst = turtle.get_poly()
#         lst = [tuple(xy) for xy in lst]
#         return lst
#
#     def oneangle(self):
#
#         for k in range(10000):
#
#             self.colorcycle(k)
#
#             self.anglego(0)
#             if self.checkplace():
#                 turtle.goto(self._startpos)
#                 break
#
#     def twoangle(self):
#
#         for k in range(10000):
#
#             self.colorcycle(k)
#
#             self.anglego(0)
#             if self._turncycle == 1 or self._turncycle == 5:
#                 self.anglego(0)
#
#             self.anglego(1)
#             if self._turncycle == 2 or self._turncycle == 5:
#                 self.anglego(1)
#
#             if self._jank is not None:
#                 turtle.forward(self._jank)
#
#             if self.checkplace():
#                 turtle.goto(self._startpos)
#                 break
#
#     def threeangle(self):
#
#         for k in range(10000):
#
#             self.colorcycle(k)
#
#             self.anglego(0)
#             if self._turncycle == 1 or self._turncycle == 5:
#                 self.anglego(0)
#
#             self.anglego(1)
#             if self._turncycle == 2 or self._turncycle == 5 or self._turncycle == 6:
#                 self.anglego(1)
#
#             self.anglego(2)
#             if self._turncycle == 3 or self._turncycle == 6:
#                 self.anglego(2)
#
#             if self._jank is not None:
#                 turtle.forward(self._jank)
#
#             if self.checkplace():
#                 turtle.goto(self._startpos)
#                 break
#
#     def fourangle(self):
#
#         for k in range(10000):
#
#             self.colorcycle(k)
#
#             self.anglego(0)
#             if self._turncycle == 1 or self._turncycle == 5 or self._turncycle == 8:
#                 self.anglego(0)
#
#             self.anglego(1)
#             if self._turncycle == 2 or self._turncycle == 5 or self._turncycle == 6 or self._turncycle == 8 or self._turncycle == 9:
#                 self.anglego(1)
#
#             self.anglego(2)
#             if self._turncycle == 3 or self._turncycle == 6 or self._turncycle == 7 or self._turncycle == 8 or self._turncycle == 9:
#                 self.anglego(2)
#
#             self.anglego(3)
#             if self._turncycle == 4 or self._turncycle == 7 or self._turncycle == 9:
#                 self.anglego(3)
#
#             if self._jank is not None:
#                 turtle.forward(self._jank)
#
#             if self.checkplace():
#                 turtle.goto(self._startpos)
#                 break
#
#     def anglego(self, n):
#         turtle.forward(self._size)
#         self.turn(*self._turns[n])
#
#     def checkplace(self):
#         sx, sy = round(self._startpos[0]), round(self._startpos[1])
#         current = turtle.pos()
#         x, y = round(current[0]), round(current[1])
#         if sx == x and sy == y:
#             return True
#         else:
#             return False
#
#     # def goto(self, coord=None, penup=False):
#     #     turtle.penup()
#     #     if coord is None:
#     #         turtle.goto(self._startpos)
#     #     else:
#     #         turtle.goto(coord)
#     #     if penup is False:
#     #         turtle.pendown()
#
#     # def center(self, showcenter=False):
#     #     precenter = Analyze(self.list).center(show=showcenter)
#     #     dist, xdist, ydist = Analyze().distance(self.position, precenter, seperate=True)
#     #     # print('dist:', dist)
#     #     newstart = (self.position[0] - precenter[0], self.position[1] - precenter[1])
#     #     turtle.penup()
#     #     # self.dot(newstart)
#     #     self.goto(newstart)
#     #     # print('newstart:', newstart)
#     #     self._startpos = turtle.pos()
#
#     def capturepath(self, penup=True):
#         if penup:
#             turtle.penup()
#             turtle.tracer(1000, 1)
#             turtle.speed(10)
#         # self.goto(penup=penup)
#         turtle.begin_poly()
#         if len(self._turns) == 1:
#             self.oneangle()
#         elif len(self._turns) == 2:
#             self.twoangle()
#         elif len(self._turns) == 3:
#             self.threeangle()
#         elif len(self._turns) == 4:
#             self.fourangle()
#         turtle.end_poly()
#         lst = turtle.get_poly()
#         lst = [tuple(xy) for xy in lst]
#         turtle.pendown()
#         if penup:
#             turtle.tracer(drawspeed, 1)
#             turtle.speed(speed)
#         return lst


rainbow = {'r': [[255, 255], [255, 255], [255, 220], [220,  75], [75,    3], [3,     3], [3,    30], [30,  125], [125, 220], [220, 255]],
           'g': [[0,   150], [150, 255], [255, 255], [255, 255], [255, 255], [255, 145], [145,   3], [3,     3], [3,     3], [3,     0]],
           'b': [[0,     0], [0,     0], [0,     3], [3,     3], [3,   240], [240, 255], [255, 255], [255, 255], [255, 255], [255,   0]]}

try1 = {'r': [0, 255], 'g': [0, 255], 'b': [0, 255]}


rainbow1 = ColorScheme(rainbow, 600)
try1 = ColorScheme(try1, 1000)

speed = 1
drawspeed = 10

setup(drawspeed)

ra1 = RadialAngularPattern(150, [[110, 2], [150, 2], [90], [80]], jank=200, turncycle=5, pensize=1, showcenter=True, colors=rainbow1, position=[200, 200], penup=False)
ra1.drawpath()
# Transform(ra1).addpoints(100, 300)
# print(ra1)
# ra1.drawpath()
# turtle.forward(50)


turtle.exitonclick()