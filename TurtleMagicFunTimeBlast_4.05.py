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


# class Analyze:
#     def __init__(self, funclist=[[]]):
#         if not isinstance(funclist[0], list):
#             funclist = [funclist]
#         self.funclist = funclist
#         self.coordlist = []
#
#     def crosspoint(self, xtolerance=0.2, ytolerance=10, show=False):
#         biglist = self.funclist
#         listnum = len(biglist)
#         listsize = len(biglist[0])
#         ypoints = []
#         points = []
#
#         for n in range(listnum):
#             for i in range(listsize):
#                 ind = n + 1
#                 if n == listnum - 1:
#                     ind = 0
#                 if abs(biglist[n][i][0] - biglist[ind][i][0]) < xtolerance:
#                     ypoints.append(biglist[n][i])
#
#         for n in range(len(ypoints)):
#             ind = n + 1
#             if n == len(ypoints) - 1:
#                 ind = 0
#             if abs(ypoints[n][1] - ypoints[ind][1]) < ytolerance:
#                 points.append(ypoints[n])
#         self.coordlist = points
#         avg = self.avgcoord(points)
#         if show is True:
#             self.drawdots(points)
#             self.drawdots(avg)
#         if len(points) == 0:
#             print('No crosspoint canidates were found. Returning None')
#         return points, avg
#
#     def center(self, show=False):
#         avgs = []
#         for i in self.funclist:
#             print(i)
#             avgs.append(self.avgcoord(i))
#         center = self.avgcoord(avgs)
#         if show is True:
#             self.drawdots(center)
#         return center
#
#     def center2(self, show=False):
#         fulllist = []
#         for i in self.funclist:
#             fulllist = fulllist + i
#         center = self.avgcoord(fulllist)
#         if show is True:
#             self.drawdots(center)
#         return center
#
#     def distancelist(self):
#         coords = self.funclist
#         distlist = []
#         xydistlist = []
#         for i in range(len(coords)):
#             i2 = ((i + 1) % len(coords))
#             dist, xdist, ydist = self.distance(coords[i], coords[i2], seperate=True)
#             # xdist = round(coords[i][0] - coords[i2][0], 6)
#             # ydist = round(coords[i][1] - coords[i2][1], 6)
#             # dist = round(sqrt((xdist ** 2) + (ydist ** 2)), 2)
#             distlist.append(dist)
#             xydistlist.append((xdist, ydist))
#         return distlist, xydistlist
#
#     @staticmethod
#     def drawdots(points, size=10):
#         turtle.color('white')
#         if isinstance(points, list):
#             for i in points:
#                 turtle.penup()
#                 turtle.goto(i)
#                 turtle.pendown()
#                 turtle.dot(size)
#         elif isinstance(points, tuple):
#             turtle.penup()
#             turtle.goto(points)
#             turtle.pendown()
#             turtle.dot(size)
#
#     @staticmethod
#     def Oavgcoord(coords):
#         # print(coords)
#         xs, ys = [xy[0] for xy in coords], [xy[1] for xy in coords]
#         if len(xs) and len(ys) > 0:
#             xavg, yavg = sum(xs)/len(xs), sum(ys)/len(ys)
#             avgcoord = (xavg, yavg)
#             return avgcoord
#         else:
#             return None
#
#     @staticmethod
#     def avgcoord(coords):
#         # print(coords)
#         xs, ys = [xy[0] for xy in coords], [xy[1] for xy in coords]
#         if len(xs) and len(ys) > 0:
#             xavg, yavg = sum(xs) / len(xs), sum(ys) / len(ys)
#             avgcoord = (xavg, yavg)
#             return avgcoord
#         else:
#             return None
#
#     @staticmethod
#     def distance(a, b, seperate=False):
#         xdist = round(a[0] - b[0], 6)
#         ydist = round(a[1] - b[1], 6)
#         dist = round(sqrt((xdist ** 2) + (ydist ** 2)), 2)
#         if seperate is True:
#             return dist, xdist, ydist
#         else:
#             return dist


# class Transform:
#     def __init__(self, func):
#         self.func = func
#         if isinstance(func, (list, tuple)):
#             inputxy = func
#             self.inputxy = func
#         else:
#             inputxy = func.list
#             self.inputxy = func.list
#         if not isinstance(inputxy[0], list):
#             inputxy = [list(lst) for lst in inputxy]
#             self.inputxy = inputxy
#         self._input = inputxy
#         self.xlist = [i[0] for i in inputxy]
#         self.ylist = [i[1] for i in inputxy]
#         self.list = [c for c in zip(self.xlist, self.ylist)]
#         self.cartesianlist = [self.pol2cart(pc[0], pc[1]) for pc in inputxy]
#         self.polarlist = [self.cart2pol(xy[0], xy[1]) for xy in inputxy]
#
#     @staticmethod
#     def cart2pol(x, y):
#         radius = np.sqrt(x ** 2 + y ** 2)
#         theta = np.arctan2(y, x)
#         return radius, theta
#
#     @staticmethod
#     def pol2cart(radius, theta):
#         x = radius * np.cos(theta)
#         y = radius * np.sin(theta)
#         return x, y
#
#     def xscale(self, scaleamt):
#         self.xlist = map(lambda x: x * scaleamt, self.xlist)
#         self.list = [c for c in zip(self.xlist, self.ylist)]
#         if isinstance(self.func, (list, tuple)):
#             return self.list
#         else:
#             self.func.list = self.list
#
#     def yscale(self, scaleamt):
#         self.ylist = map(lambda y: y * scaleamt, self.ylist)
#         self.list = [c for c in zip(self.xlist, self.ylist)]
#         if isinstance(self.func, (list, tuple)):
#             return self.list
#         else:
#             self.func.list = self.list
#
#     def xshift(self, shiftamt):
#         self.xlist = map(lambda x: x + shiftamt, self.xlist)
#         self.list = [c for c in zip(self.xlist, self.ylist)]
#         if isinstance(self.func, (list, tuple)):
#             return self.list
#         else:
#             self.func.list = self.list
#
#     def yshift(self, shiftamt):
#         self.ylist = map(lambda y: y + shiftamt, self.ylist)
#         self.list = [c for c in zip(self.xlist, self.ylist)]
#         if isinstance(self.func, (list, tuple)):
#             return self.list
#         else:
#             self.func.list = self.list
#
#     def origin_rotate(self, angle):
#         rads = angle * (pi / 180)
#         newxlist = [(x * cos(rads)) - (y * sin(rads)) for x, y in self.list]
#         newylist = [(y * cos(rads)) + (x * sin(rads)) for x, y in self.list]
#         newlist = [xy for xy in zip(newxlist, newylist)]
#         if isinstance(self.func, (list, tuple)):
#             return newlist
#         else:
#             self.func.list = newlist
#
#     def radian_rotate(self, angle):
#         rads = angle * (pi / 180)
#         radiuspolar = [c[0] for c in self.polarlist]
#         thetapolar = [c[1] for c in self.polarlist]
#         newthetalist = [i + rads for i in thetapolar]
#         newpollist = [rp for rp in zip(radiuspolar, newthetalist)]
#         newlist = [self.pol2cart(rp[0], rp[1]) for rp in newpollist]
#         if isinstance(self.func, (list, tuple)):
#             return newlist
#         else:
#             self.func.list = newlist
#
#     def rotate(self, angle, center=[0, 0]):
#         rads = angle * (pi / 180)
#         x0, y0 = center[0], center[1]
#         # ((x - x0) * cos(rads) + (y - y0) * sin(rads) + x0) # x
#         # (−(x − x0) * sin(rads) + (y − y0) * cos(rads) + y0) # y
#         newxlist = [((x - x0) * cos(rads) + (y - y0) * sin(rads) + x0) for x, y
#                     in self.list]
#         newylist = [(-(x - x0) * sin(rads) + (y - y0) * cos(rads) + y0) for x, y
#                     in self.list]
#         newlist = [xy for xy in zip(newxlist, newylist)]
#         if isinstance(self.func, (list, tuple)):
#             return newlist
#         else:
#             self.func.list = newlist
#
#     def reflectx(self):
#         newylist = [(y * -1) for y in self.ylist]
#         newlist = [c for c in zip(self.xlist, newylist)]
#         if isinstance(self.func, (list, tuple)):
#             return newlist
#         else:
#             self.func.list = newlist
#
#     def reflecty(self):
#         newxlist = [(x * -1) for x in self.xlist]
#         newlist = [c for c in zip(newxlist, self.ylist)]
#         if isinstance(self.func, (list, tuple)):
#             return newlist
#         else:
#             self.func.list = newlist
#
#     def addpoints(self, thresh, addnptz=10):
#         pointlist = self.inputxy
#         distlist, xydistlist = Analyze(pointlist).distancelist()
#         newcoords = []
#         for i in range(len(pointlist) - 1):
#             currentpoint = pointlist[i]
#             dist2nxt = distlist[i]
#             xdist2nxt = xydistlist[i][0]
#             ydist2nxt = xydistlist[i][1]
#             newcoords.append(currentpoint)
#             if abs(dist2nxt) >= thresh:
#                 xinterval = xdist2nxt / addnptz
#                 yinterval = ydist2nxt / addnptz
#                 for j in range(addnptz):
#                     newx = currentpoint[0] - (xinterval * (j + 1))
#                     newy = currentpoint[1] - (yinterval * (j + 1))
#                     newxy = (newx, newy)
#                     newcoords.append(newxy)
#         return newcoords
#
#     def Ogeneratepointcloud(self, density, spread):
#         pointlist = []
#         probnum = 100
#         probnums = np.linspace(0, spread, probnum)
#         # for i in range(100):
#         #     probabilitylist = probabilitylist + ([probnums[i]] * (i + 1))
#         probabilitylist = [[probnums[i]] * ((i + 1)**2) for i in range(probnum)]
#         probabilitylist = list(itertools.chain.from_iterable(probabilitylist))
#         for coord in self.inputxy:
#             xmin, xmax = coord[0] - spread, coord[0] + spread
#             ymin, ymax = coord[1] - spread, coord[1] + spread
#             xrandomlist = np.random.randint(xmin, xmax, density)
#             yrandomlist = np.random.randint(ymin, ymax, density)
#             for point in zip(xrandomlist, yrandomlist):
#                 distfilter = np.random.choice(probabilitylist)
#                 dist = Analyze((coord, point)).distancelist()[0][0]
#                 if dist < distfilter:
#                     xdiff, ydiff = coord[0] - point[0], coord[1] - point[1]
#                     nx = coord[0] + (xdiff * 0.2)
#                     ny = coord[1] + (ydiff * 0.2)
#                     npoint = (nx, ny)
#                     pointlist.append(npoint)
#                 else:
#                     pointlist.append(point)
#         return pointlist
#
#     def O2generatepointcloud(self, density, spread):
#         pointlist = []
#         probnum = spread * 5
#         probnums = np.linspace(1/5, spread, probnum)
#         preblist = [[round(probnums[-(i + 1)], 2)] * (i + 1) for i in range(probnum)]
#         problist = list(itertools.chain.from_iterable(preblist))[::-1]
#         problist = ([-n for n in problist][::-1] + problist)[::2]
#
#         for coord in self.inputxy:
#             center_x, center_y = coord[0], coord[1]
#             for i in range(density):
#                 radius = np.random.choice(problist)
#                 angle = 2 * pi * random.random()
#                 x = radius * cos(angle) + center_x
#                 y = radius * sin(angle) + center_y
#                 point_coord = (x, y)
#                 pointlist.append(point_coord)
#         return pointlist
#
#     def O3generatepointcloud(self, density, spread):
#         pointlist = []
#         probnum = spread * 5
#
#         for coord in self.inputxy:
#             center_x, center_y = coord[0], coord[1]
#             for i in range(density):
#                 randx, randy = np.random.normal(0, spread / 6, 2)
#                 x = randx + center_x
#                 y = randy + center_y
#                 point_coord = (x, y)
#                 pointlist.append(point_coord)
#         return pointlist
#
#     def generatepointcloud(self, density, spread, exp=1):
#         pointlist = []
#         probnum = spread * 5
#         probnums = np.linspace(1/5, spread, probnum)
#         preblist = [[round(probnums[-(i + 1)], 2)] * (i + 1) for i in range(probnum)]
#         problist = list(itertools.chain.from_iterable(preblist))[::-1]
#         problist = ([-n for n in problist][::-1] + problist)[::2]
#         for coord in self.inputxy:
#             center_x, center_y = coord[0], coord[1]
#             for i in range(density):
#                 radius = np.random.exponential(exp)
#                 angle = np.random.uniform(0, 2 * pi)
#                 x = radius * cos(angle) + center_x
#                 y = radius * sin(angle) + center_y
#                 point_coord = (x, y)
#                 pointlist.append(point_coord)
#         return pointlist


class Pattern:
    def __init__(self, lst,  colors, pensize=1, position=[0, 0]):
        self.list = lst
        self.position = position
        self.colors = colors
        self.ldepth = None
        self.set_depth()
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
        self.goto()
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
        self.goto()
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

    def set_depth(self):
        if isinstance(self.list[0], tuple) and isinstance(self.list[0][0], (int, float)):
            self.ldepth = 1
        elif isinstance(self.list[0], list):
            self.ldepth = 2
            if isinstance(self.list[0][0], list):
                self.ldepth = 3

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
        if penup:
            turtle.penup()
        if coord is None:
            turtle.goto(self.position)
        else:
            turtle.goto(coord)
        if not penup:
            turtle.pendown

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
                 colors=color_list, pensize=1, position=[0, 0], showcenter=False):
        self._size = size
        self._angles = angles
        self._turncycle = turncycle
        self._jank = jank
        self.position = position
        if isinstance(colors, str):
            colors = [colors]
        self.colors = colors
        self._turnlist = []
        if isinstance(angles, int):
            self._angles = [[angles]]
            angles = [[angles]]
        if isinstance(angles[0], int):
            self._angles = [angles]
        for i in range(len(self._angles)):
            self.create_turns(i)
        self._Turns = [t for t in self._turnlist if t is not None]
        # self.goto(position)
        self._startpos = turtle.pos()
        self.goto()
        self.list = self.capturepath()
        self.centeredlist = []
        # self.center(showcenter=showcenter)
        self.list = self.capturepath()
        super().__init__(self.list, self.colors, pensize, self._startpos)

    def create_turns(self, n):
        tparams = self._angles[n]
        if isinstance(tparams, float):
            tparams = [tparams]
        if n == 0:
            # self.turn1 = self.turn(*tparams)
            self._turnlist.append(tparams)
        if n == 1:
            # self.turn2 = self.turn(*tparams)
            self._turnlist.append(tparams)
        if n == 2:
            # self.turn3 = self.turn(*tparams)
            self._turnlist.append(tparams)
        if n == 3:
            # self.turn4 = self.turn(*tparams)
            self._turnlist.append(tparams)

    def draw(self):
        if len(self._Turns) == 1:
            self.oneangle()
        elif len(self._Turns) == 2:
            self.twoangle()
        elif len(self._Turns) == 3:
            self.threeangle()
        elif len(self._Turns) == 4:
            self.fourangle()

    def oneangle(self):

        for k in range(10000):

            self.colorcycle(k)

            self.anglego(0)
            if self.checkplace():
                turtle.goto(self._startpos)
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
                turtle.goto(self._startpos)
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
                turtle.goto(self._startpos)
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
                turtle.goto(self._startpos)
                break

    def anglego(self, n):
        turtle.forward(self._size)
        self.turn(*self._Turns[n])

    def checkplace(self):
        sx, sy = round(self._startpos[0]), round(self._startpos[1])
        current = turtle.pos()
        x, y = round(current[0]), round(current[1])
        if sx == x and sy == y:
            return True
        else:
            return False

    # def goto(self, coord=None, penup=False):
    #     turtle.penup()
    #     if coord is None:
    #         turtle.goto(self._startpos)
    #     else:
    #         turtle.goto(coord)
    #     if penup is False:
    #         turtle.pendown()

    # def center(self, showcenter=False):
    #     precenter = Analyze(self.list).center(show=showcenter)
    #     dist, xdist, ydist = Analyze().distance(self.position, precenter, seperate=True)
    #     # print('dist:', dist)
    #     newstart = (self.position[0] - precenter[0], self.position[1] - precenter[1])
    #     turtle.penup()
    #     # self.dot(newstart)
    #     self.goto(newstart)
    #     # print('newstart:', newstart)
    #     self._startpos = turtle.pos()

    def capturepath(self, penup=True):
        if penup:
            turtle.penup()
            turtle.tracer(1000, 1)
            turtle.speed(10)
        # self.goto(penup=penup)
        turtle.begin_poly()
        if len(self._Turns) == 1:
            self.oneangle()
        elif len(self._Turns) == 2:
            self.twoangle()
        elif len(self._Turns) == 3:
            self.threeangle()
        elif len(self._Turns) == 4:
            self.fourangle()
        turtle.end_poly()
        # self.goto((0, 0))
        lst = turtle.get_poly()
        lst = [tuple(xy) for xy in lst]
        turtle.pendown()
        if penup:
            turtle.tracer(drawspeed, 1)
            turtle.speed(speed)
        return lst


rainbow = {'r': [[255, 255], [255, 255], [255, 220], [220,  75], [75,    3], [3,     3], [3,    30], [30,  125], [125, 220], [220, 255]],
           'g': [[0,   150], [150, 255], [255, 255], [255, 255], [255, 255], [255, 145], [145,   3], [3,     3], [3,     3], [3,     0]],
           'b': [[0,     0], [0,     0], [0,     3], [3,     3], [3,   240], [240, 255], [255, 255], [255, 255], [255, 255], [255,   0]]}

try1 = {'r': [0, 255], 'g': [0, 255], 'b': [0, 255]}


rainbow1 = ColorScheme(rainbow, 600)
try1 = ColorScheme(try1, 1000)

speed = 10
drawspeed = 100

setup(drawspeed)

ra1 = RadialAngularPattern(150, [[110, 2]], jank=200, turncycle=5, pensize=1, showcenter=True, colors=rainbow1, position=[200, 200])
# Transform(ra1).addpoints(100, 300)
# print(ra1)
# ra1.drawpath()
# turtle.forward(50)


turtle.exitonclick()