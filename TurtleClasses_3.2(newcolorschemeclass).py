import turtle
import random
import itertools
import numpy as np
from math import *
from matplotlib.colors import rgb2hex as pltcolors


# TODO: Point cloud generator
# TODO: Imporve centering function
# TODO: ColorScheme shifting tool

color_list = [
    'red', 'crimson', 'orangered', 'darkorange', 'orange', 'gold',
    'yellow', 'greenyellow', 'lawngreen', 'limegreen', 'springgreen',
    'mediumspringgreen', 'aquamarine', 'turquoise', 'aqua',
    'deepskyblue', 'dodgerblue', 'mediumslateblue', 'mediumpurple',
    'blueviolet', 'darkviolet', 'purple', 'mediumvioletred'
]


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


class ColorCycle:
    def __init__(self, colorlist):
        self._color = colorlist

    def colorsetter(self, ind):
        length = len(self._color)
        modind = ind % length
        turtle.color(self._color[modind])
        return self._color[modind]


class Turn:

    def __init__(self, angle, curve=None, curvesize=5):
        self._angle = angle
        self._curve = curve
        self._curvesize = curvesize

    def go(self):
        if self._curve is None or self._curve == 0:
            turtle.right(self._angle)
        else:
            reps = round(abs(self._angle) / 10)
            turn = abs(self._angle) / reps
            for j in range(reps):
                turtle.forward(self._curvesize)
                if self._angle < 0:
                    turtle.left(turn)
                else:
                    turtle.right(turn)


class Transform:
    def __init__(self, func):
        self.func = func
        if isinstance(func, (list, tuple)):
            inputxy = func
            self.inputxy = func
        else:
            inputxy = func.list
            self.inputxy = func.list
        if not isinstance(inputxy[0], list):
            inputxy = [list(lst) for lst in inputxy]
            self.inputxy = inputxy
        self._input = inputxy
        self.xlist = [i[0] for i in inputxy]
        self.ylist = [i[1] for i in inputxy]
        self.list = [c for c in zip(self.xlist, self.ylist)]
        self.cartesianlist = [self.pol2cart(pc[0], pc[1]) for pc in inputxy]
        self.polarlist = [self.cart2pol(xy[0], xy[1]) for xy in inputxy]

    @staticmethod
    def cart2pol(x, y):
        radius = np.sqrt(x ** 2 + y ** 2)
        theta = np.arctan2(y, x)
        return radius, theta

    @staticmethod
    def pol2cart(radius, theta):
        x = radius * np.cos(theta)
        y = radius * np.sin(theta)
        return x, y

    def xscale(self, scaleamt):
        self.xlist = map(lambda x: x * scaleamt, self.xlist)
        self.list = [c for c in zip(self.xlist, self.ylist)]
        if isinstance(self.func, (list, tuple)):
            return self.list
        else:
            self.func.list = self.list

    def yscale(self, scaleamt):
        self.ylist = map(lambda y: y * scaleamt, self.ylist)
        self.list = [c for c in zip(self.xlist, self.ylist)]
        if isinstance(self.func, (list, tuple)):
            return self.list
        else:
            self.func.list = self.list

    def xshift(self, shiftamt):
        self.xlist = map(lambda x: x + shiftamt, self.xlist)
        self.list = [c for c in zip(self.xlist, self.ylist)]
        if isinstance(self.func, (list, tuple)):
            return self.list
        else:
            self.func.list = self.list

    def yshift(self, shiftamt):
        self.ylist = map(lambda y: y + shiftamt, self.ylist)
        self.list = [c for c in zip(self.xlist, self.ylist)]
        if isinstance(self.func, (list, tuple)):
            return self.list
        else:
            self.func.list = self.list

    def origin_rotate(self, angle):
        rads = angle * (pi / 180)
        newxlist = [(x * cos(rads)) - (y * sin(rads)) for x, y in self.list]
        newylist = [(y * cos(rads)) + (x * sin(rads)) for x, y in self.list]
        newlist = [xy for xy in zip(newxlist, newylist)]
        if isinstance(self.func, (list, tuple)):
            return newlist
        else:
            self.func.list = newlist

    def radian_rotate(self, angle):
        rads = angle * (pi / 180)
        radiuspolar = [c[0] for c in self.polarlist]
        thetapolar = [c[1] for c in self.polarlist]
        newthetalist = [i + rads for i in thetapolar]
        newpollist = [rp for rp in zip(radiuspolar, newthetalist)]
        newlist = [self.pol2cart(rp[0], rp[1]) for rp in newpollist]
        if isinstance(self.func, (list, tuple)):
            return newlist
        else:
            self.func.list = newlist

    def rotate(self, angle, center=[0, 0]):
        rads = angle * (pi / 180)
        x0, y0 = center[0], center[1]
        # ((x - x0) * cos(rads) + (y - y0) * sin(rads) + x0) # x
        # (−(x − x0) * sin(rads) + (y − y0) * cos(rads) + y0) # y
        newxlist = [((x - x0) * cos(rads) + (y - y0) * sin(rads) + x0) for x, y
                    in self.list]
        newylist = [(-(x - x0) * sin(rads) + (y - y0) * cos(rads) + y0) for x, y
                    in self.list]
        newlist = [xy for xy in zip(newxlist, newylist)]
        if isinstance(self.func, (list, tuple)):
            return newlist
        else:
            self.func.list = newlist

    def reflectx(self):
        newylist = [(y * -1) for y in self.ylist]
        newlist = [c for c in zip(self.xlist, newylist)]
        if isinstance(self.func, (list, tuple)):
            return newlist
        else:
            self.func.list = newlist

    def reflecty(self):
        newxlist = [(x * -1) for x in self.xlist]
        newlist = [c for c in zip(newxlist, self.ylist)]
        if isinstance(self.func, (list, tuple)):
            return newlist
        else:
            self.func.list = newlist

    def addpoints(self, thresh, addnptz=10):
        pointlist = self.inputxy
        distlist, xydistlist = Analyze(pointlist).distancelist()
        newcoords = []
        for i in range(len(pointlist) - 1):
            currentpoint = pointlist[i]
            dist2nxt = distlist[i]
            xdist2nxt = xydistlist[i][0]
            ydist2nxt = xydistlist[i][1]
            newcoords.append(currentpoint)
            if abs(dist2nxt) >= thresh:
                xinterval = xdist2nxt / addnptz
                yinterval = ydist2nxt / addnptz
                for j in range(addnptz):
                    newx = currentpoint[0] - (xinterval * (j + 1))
                    newy = currentpoint[1] - (yinterval * (j + 1))
                    newxy = (newx, newy)
                    newcoords.append(newxy)
        return newcoords

    def Ogeneratepointcloud(self, density, spread):
        pointlist = []
        probnum = 100
        probnums = np.linspace(0, spread, probnum)
        # for i in range(100):
        #     probabilitylist = probabilitylist + ([probnums[i]] * (i + 1))
        probabilitylist = [[probnums[i]] * ((i + 1)**2) for i in range(probnum)]
        probabilitylist = list(itertools.chain.from_iterable(probabilitylist))
        for coord in self.inputxy:
            xmin, xmax = coord[0] - spread, coord[0] + spread
            ymin, ymax = coord[1] - spread, coord[1] + spread
            xrandomlist = np.random.randint(xmin, xmax, density)
            yrandomlist = np.random.randint(ymin, ymax, density)
            for point in zip(xrandomlist, yrandomlist):
                distfilter = np.random.choice(probabilitylist)
                dist = Analyze((coord, point)).distancelist()[0][0]
                if dist < distfilter:
                    xdiff, ydiff = coord[0] - point[0], coord[1] - point[1]
                    nx = coord[0] + (xdiff * 0.2)
                    ny = coord[1] + (ydiff * 0.2)
                    npoint = (nx, ny)
                    pointlist.append(npoint)
                else:
                    pointlist.append(point)
        return pointlist

    def O2generatepointcloud(self, density, spread):
        pointlist = []
        probnum = spread * 5
        probnums = np.linspace(1/5, spread, probnum)
        preblist = [[round(probnums[-(i + 1)], 2)] * (i + 1) for i in range(probnum)]
        problist = list(itertools.chain.from_iterable(preblist))[::-1]
        problist = ([-n for n in problist][::-1] + problist)[::2]

        for coord in self.inputxy:
            center_x, center_y = coord[0], coord[1]
            for i in range(density):
                radius = np.random.choice(problist)
                angle = 2 * pi * random.random()
                x = radius * cos(angle) + center_x
                y = radius * sin(angle) + center_y
                point_coord = (x, y)
                pointlist.append(point_coord)
        return pointlist

    def O3generatepointcloud(self, density, spread):
        pointlist = []
        probnum = spread * 5

        for coord in self.inputxy:
            center_x, center_y = coord[0], coord[1]
            for i in range(density):
                randx, randy = np.random.normal(0, spread / 6, 2)
                x = randx + center_x
                y = randy + center_y
                point_coord = (x, y)
                pointlist.append(point_coord)
        return pointlist

    def generatepointcloud(self, density, spread, exp=1):
        pointlist = []
        probnum = spread * 5
        probnums = np.linspace(1/5, spread, probnum)
        preblist = [[round(probnums[-(i + 1)], 2)] * (i + 1) for i in range(probnum)]
        problist = list(itertools.chain.from_iterable(preblist))[::-1]
        problist = ([-n for n in problist][::-1] + problist)[::2]
        for coord in self.inputxy:
            center_x, center_y = coord[0], coord[1]
            for i in range(density):
                radius = np.random.exponential(exp)
                angle = np.random.uniform(0, 2 * pi)
                x = radius * cos(angle) + center_x
                y = radius * sin(angle) + center_y
                point_coord = (x, y)
                pointlist.append(point_coord)
        return pointlist


class Analyze:
    def __init__(self, funclist=[[]]):
        if not isinstance(funclist[0], list):
            funclist = [funclist]
        self.funclist = funclist
        self.coordlist = []

    def crosspoint(self, xtolerance=0.2, ytolerance=10, show=False):
        biglist = self.funclist
        listnum = len(biglist)
        listsize = len(biglist[0])
        ypoints = []
        points = []

        for n in range(listnum):
            for i in range(listsize):
                ind = n + 1
                if n == listnum - 1:
                    ind = 0
                if abs(biglist[n][i][0] - biglist[ind][i][0]) < xtolerance:
                    ypoints.append(biglist[n][i])

        for n in range(len(ypoints)):
            ind = n + 1
            if n == len(ypoints) - 1:
                ind = 0
            if abs(ypoints[n][1] - ypoints[ind][1]) < ytolerance:
                points.append(ypoints[n])
        self.coordlist = points
        avg = self.avgcoord(points)
        if show is True:
            self.drawdots(points)
            self.drawdots(avg)
        return points, avg

    def center(self, show=False):
        avgs = []
        for i in self.funclist:
            avgs.append(self.avgcoord(i))
        center = self.avgcoord(avgs)
        if show is True:
            self.drawdots(center)
        return center

    def center2(self, show=False):
        fulllist = []
        for i in self.funclist:
            fulllist = fulllist + i
        center = self.avgcoord(fulllist)
        if show is True:
            self.drawdots(center)
        return center

    def distancelist(self):
        coords = self.funclist
        distlist = []
        xydistlist = []
        for i in range(len(coords)):
            i2 = ((i + 1) % len(coords))
            dist, xdist, ydist = self.distance(coords[i], coords[i2], seperate=True)
            # xdist = round(coords[i][0] - coords[i2][0], 6)
            # ydist = round(coords[i][1] - coords[i2][1], 6)
            # dist = round(sqrt((xdist ** 2) + (ydist ** 2)), 2)
            distlist.append(dist)
            xydistlist.append((xdist, ydist))
        return distlist, xydistlist

    @staticmethod
    def drawdots(points, size=10):
        turtle.color('white')
        if isinstance(points, list):
            for i in points:
                turtle.penup()
                turtle.goto(i)
                turtle.pendown()
                turtle.dot(size)
        elif isinstance(points, tuple):
            turtle.penup()
            turtle.goto(points)
            turtle.pendown()
            turtle.dot(size)

    @staticmethod
    def avgcoord(coords):
        # print(coords)
        xs, ys = [xy[0] for xy in coords], [xy[1] for xy in coords]
        if len(xs) and len(ys) > 0:
            xavg, yavg = sum(xs)/len(xs), sum(ys)/len(ys)
            avgcoord = (xavg, yavg)
            return avgcoord
        else:
            return None

    @staticmethod
    def distance(a, b, seperate=False):
        xdist = round(a[0] - b[0], 6)
        ydist = round(a[1] - b[1], 6)
        dist = round(sqrt((xdist ** 2) + (ydist ** 2)), 2)
        if seperate is True:
            return dist, xdist, ydist
        else:
            return dist


class RadialAngularPattern:

    def __init__(self, size, angles=[[125, 1, 3]], turncycle=0, jank=None,
                 colors=color_list, pensize=1, position=[0, 0]):
        turtle.setheading(0)
        self._colors = colors
        self._pensize = pensize
        self._size = size
        turtle.pensize(self._pensize)
        self._angles = angles
        self._turncycle = turncycle
        self._jank = jank
        self.position = position
        if isinstance(colors, (ColorScheme, ColorScheme)):
            colors = colors.hex
        elif isinstance(colors, str):
            colors = [colors]
        self._colorlist = colors
        self._turnlist = []
        if isinstance(angles, int):
            self._angles = [[angles]]
            angles = [[angles]]
        if isinstance(angles[0], int):
            self._angles = [angles]
        for i in range(len(self._angles)):
            self.create_turns(i)
        self._nTurns = [t for t in self._turnlist if t is not None]
        self.goto(position)
        self._startpos = turtle.pos()
        # self.goto()
        self.list = self.capturepath()
        self.centeredlist = []
        self.dot(position)
        self.center()
        self.list = self.capturepath()
    #
    # def __repr__(self):
    #     list = list(self.list)
    #     return list
    #
    # def __str__(self):
    #     return str(self.list)
    #
    # def __getitem__(self, index):
    #     return self.list[index]
    #
    # def __setitem__(self, index, value):
    #     self.list[index] = value
    #
    # def __len__(self):
    #     return len(self.list)

    def create_turns(self, n):
        tparams = self._angles[n]
        if isinstance(tparams, float):
            tparams = [tparams]
        if n == 0:
            self.turn1 = Turn(*tparams)
            self._turnlist.append(self.turn1)
        if n == 1:
            self.turn2 = Turn(*tparams)
            self._turnlist.append(self.turn2)
        if n == 2:
            self.turn3 = Turn(*tparams)
            self._turnlist.append(self.turn3)
        if n == 3:
            self.turn4 = Turn(*tparams)
            self._turnlist.append(self.turn4)

    def draw(self):
        if len(self._nTurns) == 1:
            self.oneangle()
        elif len(self._nTurns) == 2:
            self.twoangle()
        elif len(self._nTurns) == 3:
            self.threeangle()
        elif len(self._nTurns) == 4:
            self.fourangle()

    def oneangle(self):

        for k in range(10000):

            ColorCycle(self._colorlist).colorsetter(k)

            self.anglego(0)
            if self.checkplace():
                turtle.goto(self._startpos)
                break

    def twoangle(self):

        for k in range(10000):

            ColorCycle(self._color).colorsetter(k)

            self.anglego(0)
            if self._turncycle == 1 or self._turncycle == 5:
                self.anglego(0)

            self.anglego(1)
            if self._turncycle == 2 or self._turncycle == 5:
                self.anglego(1)

            if self._jank is not None:
                turtle.forward(self._jank)

            if self.checkplace():
                turtle.goto(self._startpos)
                break

    def threeangle(self):

        for k in range(10000):

            ColorCycle(self._color).colorsetter(k)

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
                turtle.goto(self._startpos)
                break

    def fourangle(self):

        for k in range(10000):

            ColorCycle(self._color).colorsetter(k)

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
                turtle.goto(self._startpos)
                break

    def anglego(self, n):
        turtle.forward(self._size)
        self._nTurns[n].go()

    def checkplace(self):
        sx, sy = round(self._startpos[0]), round(self._startpos[1])
        current = turtle.pos()
        x, y = round(current[0]), round(current[1])
        if sx == x and sy == y:
            return True
        else:
            return False

    def goto(self, coord=None, penup=False):
        turtle.penup()
        if coord is None:
            turtle.goto(self._startpos)
        else:
            turtle.goto(coord)
        if penup is False:
            turtle.pendown()

    def center(self):
        precenter = Analyze(self.list).center()
        dist, xdist, ydist = Analyze().distance(self.position, precenter, seperate=True)
        print('dist:', dist)
        newcenter = (self.position[0] - precenter[0], self.position[1] - precenter[1])
        self.goto(newcenter)
        self._startpos = turtle.pos()

    def capturepath(self, penup=True):
        if penup is True:
            turtle.penup()
        self.goto(penup=penup)
        turtle.begin_poly()
        if len(self._nTurns) == 1:
            self.oneangle()
        elif len(self._nTurns) == 2:
            self.twoangle()
        elif len(self._nTurns) == 3:
            self.threeangle()
        elif len(self._nTurns) == 4:
            self.fourangle()
        turtle.end_poly()
        self.goto((0, 0))
        lst = turtle.get_poly()
        lst = [tuple(xy) for xy in lst]
        return lst

    def dot(self, point):
        turtle.color('yellow')
        turtle.penup()
        turtle.goto(point)
        turtle.pendown()
        turtle.dot(10)


class PolarPattern:
    def __init__(self, radianlist, radiuslist, size, position=[0, 0]):
        self.radianlist = radianlist
        self.radiuslist = radiuslist
        self.polarlist = [c for c in zip(self.radiuslist, self.radianlist)]
        self.cartesianlist = [self.pol2cart(pc[0], pc[1]) for pc in
                              self.polarlist]
        self.list = self.sizeup(self.cartesianlist, size)
        if position[0] != 0:
            Transform(self).xshift(position[0])
        if position[1] != 0:
            Transform(self).yshift(position[1])
        self.position = position
        # self.goto(self.position)

    def draw(self, lst=None):
        if lst is None:
            lst = self.list
        turtle.penup()
        turtle.goto(lst[0])
        turtle.pendown()
        for xy in lst:
            turtle.goto(xy)

    @staticmethod
    def sizeup(list_, factor=50):
        list = [(xy[0] * factor, xy[1] * factor) for xy in list_]
        return list

    @staticmethod
    def cart2pol(x, y):
        radius = np.sqrt(x ** 2 + y ** 2)
        theta = np.arctan2(y, x)
        return (radius, theta)

    @staticmethod
    def pol2cart(radius, theta):
        x = radius * np.cos(theta)
        y = radius * np.sin(theta)
        return (x, y)

    def goto(self, position):
        turtle.penup()
        turtle.goto(position)
        turtle.pendown()


class FlowerPattern(PolarPattern):
    def __init__(self, npetals, innerdepth=3, size=50, poly=500, color='green',
                 position=[0, 0]):
        self._npetals = npetals
        self._innerdepth = innerdepth
        if isinstance(color, (ColorScheme, ColorScheme)):
            color = color.hex
        if isinstance(color, list):
            color = color[0]
            print('Only 1 color can be used. Using first in list')
        turtle.color(color)
        radianlist = np.linspace(0, 7, poly)
        radiuslist = [(3 - (innerdepth * cos(npetals * theta))) for theta in
                      radianlist]
        super().__init__(radianlist, radiuslist, size, position)


class SpiralPattern(PolarPattern):
    def __init__(self, linedist=1, diameter=100, scale=20, poly=400,
                 centerdist=0, color='orange', position=[0, 0]):
        linedist = linedist / 10
        self._tightness = linedist
        self._size = diameter
        angldiv = (diameter * poly)
        if isinstance(color, (ColorScheme, ColorScheme)):
            color = color.hex
        if isinstance(color, list):
            color = color[0]
            print('Only 1 color can be used. Using first in list')
        turtle.color(color)
        radianlist = np.linspace(0, diameter, angldiv // 6)
        radiuslist = [(angl * linedist) + centerdist for angl in radianlist]
        super().__init__(radianlist, radiuslist, scale, position)


class FlowerPattern2(PolarPattern):
    def __init__(self, npetals, innerdepth=3, size=5, reps=300, color='green', position=[0, 0]):
        self._npetals = npetals
        self._innerdepth = innerdepth
        if isinstance(color, (ColorScheme, ColorScheme)):
            color = color.hex
        if isinstance(color, list):
            color = color[0]
            print('Only 1 color can be used. Using first in list')
        turtle.color(color)
        divs = 50 * reps
        radianlist = np.linspace(0, reps, divs)
        radiuslist = [(3 + theta + innerdepth * cos(npetals * theta)) for theta in
                      radianlist]
        super().__init__(radianlist, radiuslist, size, position)


class Wave:
    def __init__(self, stretch=50, height=100, position=[0, 0], length=20,
                 color='yellow', cosin=False):
        if isinstance(color, (ColorScheme, ColorScheme)):
            color = color.hex
        if isinstance(color, list):
            color = color[0]
            print('Only 1 color can be used. Using first in list')
        turtle.color(color)
        self.xlist = np.linspace(-length, length, length * 25)
        if cosin is False:
            self.ylist = [sin(x) for x in self.xlist]
        else:
            self.ylist = [cos(x) for x in self.xlist]
        self._Olist = [xy for xy in zip(self.xlist, self.ylist)]
        self._talllist = Transform(self._Olist).yscale(height)
        self.list = Transform(self._talllist).xscale(stretch)
        if position != [0, 0]:
            self.list = Transform(self.list).xshift(position[0])
            self.list = Transform(self.list).yshift(position[1])

    def draw(self):
        lst = self.list
        turtle.penup()
        turtle.goto(lst[0])
        turtle.pendown()
        for xy in lst:
            turtle.goto(xy)

    def capturepath(self, penup=True):
        lst = self.list
        turtle.penup()
        turtle.goto(lst[0])
        if penup is False:
            turtle.pendown()
        turtle.begin_poly()
        for xy in lst:
            turtle.goto(xy)
        turtle.end_poly()
        return turtle.get_poly()


class DrawPath:
    def __init__(self, coordlist, pensize=1, colors='white', colordist=0, lines=True, dots=False, dotsize=1):
        self.coordlist = coordlist
        self.pensize = pensize
        self.colors = colors
        self.goto()
        turtle.pensize(self.pensize)
        self.colorcycle = self.colorset()
        self._colordist = colordist
        self.dotsize = dotsize
        if dots is True:
            self.dots()
        if lines is True:
            self.draw()

    def goto(self, coords=None):
        if coords is None:
            turtle.penup()
            turtle.goto(self.coordlist[0])
            turtle.pendown()
        else:
            turtle.penup()
            turtle.goto(coords)
            turtle.pendown()

    def colorset(self):
        if isinstance(self.colors, (ColorScheme, ColorScheme)):
            self.colors = self.colors.hex
        elif isinstance(self.colors, str):
            self.colors = [self.colors]
        if isinstance(self.colors, str):
            turtle.color(self.colors)
            return False
        elif len(self.colors) == 1:
            turtle.color(self.colors[0])
            return False
        else:
            return True

    def draw(self):
        dist = 0
        colordist = self._colordist
        colorcount = 0
        turtle.color(self.colors[colorcount])
        for i in range(len(self.coordlist)):
            colorcount += 1
            if dist > colordist and self.colorcycle is True:
                if colorcount >= len(self.colors):
                    colorcount = 0
                # index = i % len(self.colors)
                color = self.colors[colorcount]
                turtle.color(color)
                dist = 0
            pos = turtle.pos()
            turtle.goto(self.coordlist[i])
            dist += turtle.distance(pos)

    def dots(self):
        for i in range(len(self.coordlist)):
            if self.colorcycle is True:
                index = i % len(self.colors)
                color = self.colors[index]
                turtle.color(color)
            self.goto(self.coordlist[i])
            turtle.dot(self.dotsize)


class LVL2:
    @staticmethod
    def layered_flowers(layers=30, npetals=6, innerdepth=3, sizefactor=2,
                        pensize=1, rotate=0, rotaterate=1, colors=color_list,
                        position=[0, 0]):
        sf = 1
        rotationfactor = 1
        if isinstance(colors, (ColorScheme, ColorScheme)):
            colors = colors.hex
        for i in range(1, layers):
            if isinstance(colors, list):
                colind = i % len(colors)
                color2 = colors[colind]
            else:
                color2 = colors
            f = FlowerPattern(npetals, innerdepth, sf, color=color2)
            sf += 1 * sizefactor
            if rotate != 0:
                Transform(f).rotate(rotate * rotationfactor)
                rotationfactor += rotaterate
            if position != [0, 0]:
                Transform(f).xshift(position[0])
                Transform(f).yshift(position[1])
            turtle.pensize(pensize)
            f.draw()

    @staticmethod
    def sin_spiral(strands=20, xshift=10, yshift=0, rotate=0, rotaterate=1,
                   rotatecenter=[0, 0], colors=color_list, wavelength=50, amplitude=100, wlshift=0,
                   ampshift=0, length=20, cosine=False, position=[0, 0]):
        funclist = []
        xpos, ypos = position[0], position[1]
        rotationfactor = 1
        pathlist = []
        if isinstance(colors, (ColorScheme, ColorScheme)):
            colors = colors.hex
        for i in range(strands):
            colind = i % len(colors)
            col = colors[colind]
            sin1 = Wave(stretch=wavelength, height=amplitude, color=col,
                        position=[xpos, ypos], length=length, cosin=cosine)
            xpos += xshift
            ypos += yshift
            wavelength += wlshift
            amplitude += ampshift
            if rotate != 0:
                Transform(sin1).rotate(rotate * rotationfactor, rotatecenter)
                rotationfactor += rotaterate
                for xy in sin1.list:
                    if not isinstance(xy, tuple):
                        pass
                        # print(type(xy))
                    for val in xy:
                        pass
            funclist.append(sin1.list)
            pathlist.append(sin1.capturepath())
        # checkptz, point = Analyze(funclist).crosspoint()
        turtle.color('white')
        turtle.penup()
        # turtle.goto(point)
        turtle.pendown()
        turtle.dot(5)
        return pathlist


    @staticmethod
    def sin_avg_point_rotation(strands=20, xshift=10, yshift=0,
                               rotate=1, rotaterate=1,totalrotation=None,
                               colors=color_list, wavelength=50, amplitude=100, wlshift=0,
                               ampshift=0, length=20, cosine=False,
                               position=[0, 0], showpoint=False, draworig=False, getpoint=False):
        funclist = []
        xpos, ypos = position[0], position[1]
        wavelength2 = wavelength
        amplitude2 = amplitude
        if isinstance(colors, (ColorScheme, ColorScheme)):
            colors = colors.hex
        rotationfactor = 1
        for i in range(strands):
            colind = i % len(colors)
            col = colors[colind]
            sin1 = Wave(stretch=wavelength2, height=amplitude, color=col,
                        position=[xpos, ypos], length=length, cosin=cosine)
            xpos += xshift
            ypos += yshift
            wavelength2 += wlshift
            amplitude2 += ampshift
            funclist.append(sin1.list)
            if draworig is True:
                sin1.draw()
        _, rotation_point = Analyze(funclist).crosspoint()
        # print(type(funclist), type(funclist[0]), type(funclist[0][0]))
        center = Analyze(funclist).center()
        # center2 = Analyzer(funclist).center2()

        """Part 2"""
        xpos, ypos = position[0], position[1]
        rotationfactor = 1
        if totalrotation is None:
            funclist2 = []
            totalrotation = -(rotate * (strands / 2))
        for i in range(strands):
            colind = i % len(colors)
            col = colors[colind]
            sin1 = Wave(stretch=wavelength, height=amplitude, color=col,
                        position=[xpos, ypos], length=length, cosin=cosine)
            xpos += xshift
            ypos += yshift
            wavelength += wlshift
            amplitude += ampshift
            if rotate != 0 and rotation_point is not None:
                Transform(sin1).rotate(rotate * rotationfactor, rotation_point)
                rotationfactor += rotaterate
            # if center is not None:
                # Transform(sin1).xshift(-center[0])
                # Transform(sin1).yshift(-center[1])
            if totalrotation > 0:
                Transform(sin1).rotate(totalrotation, center)
            funclist2.append(sin1.list)
            sin1.draw()
        if showpoint is True and rotation_point is not None:
            turtle.penup()
            turtle.goto(rotation_point)
            turtle.pendown()
            turtle.color('white')
            turtle.dot(6)
            turtle.penup()
            turtle.goto(center)
            turtle.pendown()
            turtle.color('gray')
            turtle.dot(6)
            turtle.penup()
        if getpoint is True:
            return funclist2, rotation_point
        else:
            return funclist2

    @staticmethod
    def spiral_spiral(reps=30, rotation=5, linedist=10, diameter=10, scale=20,
                      poly=400, centerdist=0, colors=color_list):
        rotate = 0
        if isinstance(colors, (ColorScheme, ColorScheme)):
            colors = colors.hex
        for i in range(reps):
            colind = i % len(colors)
            col = colors[colind]
            spiral = SpiralPattern(linedist=linedist, diameter=diameter,
                                   scale=scale, poly=poly,
                                   centerdist=centerdist, color=col)
            Transform(spiral).rotate(rotate)
            spiral.draw()
            rotate += rotation

    @staticmethod
    def antenas(colors=color_list, xshift=5, yshift=0, position=[100, 100]):
        xloc, yloc = position[0], position[1]
        if isinstance(colors, (ColorScheme, ColorScheme)):
            colors = colors.hex
        for i in range(10):
            colind = i % len(colors)
            col = colors[colind]
            sp1 = SpiralPattern(30, 3, color=col, position=[xloc, yloc])
            sp1.draw()
            xloc += xshift
            yloc += yshift


speed = 1000
turtle.setup(1900, 1200)  # Laptop screen
turtle.speed(10)
# turtle.setup(3840, 2200)     # 4K screen
turtle.bgcolor('black')
# turtle.bgpic('turtle_background_image1-02-01.png')
turtle.tracer(speed, 0)
turtle.hideturtle()




#
#             r          o           y          yg           g           bg          b           b         p
rainbow = {'r': [[255, 255], [255, 255], [255, 220], [220,  75], [75,    3], [3,     3], [3,    30], [30,  125], [125, 220], [220, 255]],
           'g': [[0,   150], [150, 255], [255, 255], [255, 255], [255, 255], [255, 145], [145,   3], [3,     3], [3,     3], [3,     0]],
           'b': [[0,     0], [0,     0], [0,     3], [3,     3], [3,   240], [240, 255], [255, 255], [255, 255], [255, 255], [255,   0]]}
try2 = {'r': [0, 255, 200, 255],
        'g': [0, 50, 50, 0],
        'b': [255, 200, 255, 100]}

rainbow1 = ColorScheme(rainbow, 60)
# newcol1 = ColorScheme(try2, 260, symetrical=True)

# point = LVL2.sin_avg_point_rotation(60, xshift=0, wavelength=35,
#                                     wlshift=0.2, ampshift=0,
#                                     rotate=0.5, length=40,
#                                     colors=rainbow1, showpoint=False,
#                                     cosine=False)

# ra1 = RadialAngularPattern(500, [125], colors=rainbow1).capturepath(penup=False)
# center = Analyze(ra1).center(True)
# center2 = Analyze(ra1).center2()
ra2 = RadialAngularPattern(500, [125], colors=rainbow1).capturepath()
# spi = LVL2.sin_avg_point_rotation(20, 0, 0, 2)
# print(type(spi), type(spi[0]))

DrawPath(ra2, 1, rainbow1)
# DrawPath([center], dots=True, dotsize=10)
# DrawPath([center2], dots=True, dotsize=10)
# print(ra1)
# print(center)

# path1 = RadialAngularPattern(500).draw()
# path1 = RadialAngularPattern(500).capturepath()
# DrawPath(path1, 1, rainbow1, lines=True) #, dots=True)
# path1 = Transform(path1).addpoints(100, 200)
# path2 = LVL2.sin_spiral(rotate=5)
# path2 = LVL2.sin_avg_point_rotation(rotate=5, rotaterate=2, showpoint=True, draworig=False)
# cloud1 = Transform(path2).generatepointcloud(10, 10, exp=6)
# DrawPath(cloud1, 1, 'white', lines=False, dots=True, dotsize=0.1)
# DrawPath(path1, 2, rainbow1, colordist=50, lines=True) #, dots=True)

# LVL2.layered_flowers(layers=80, npetals=6, innerdepth=1, sizefactor=2, pensize=4, rotate=1, colors=rainbow1)
# LVL2.sin_spiral(30, xshift=10, wlshift=1, ampshift=0, rotate=0, colors=color_list)
# LVL2.sin_spiral(50, 2, rotate=1, cosine=True, colors=purple_to_black)
# LVL2.layered_flowers(50, rotate=1, color=black_to_purple)
# LVL2.antenas()


turtle.exitonclick()
