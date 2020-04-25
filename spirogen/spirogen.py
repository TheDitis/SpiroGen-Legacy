import turtle
import numpy as np
from matplotlib.colors import rgb2hex as pltcolors
from scipy.spatial import distance
from math import *

default_color_list = [
    'red', 'crimson', 'orangered', 'darkorange', 'orange', 'gold',
    'yellow', 'greenyellow', 'lawngreen', 'limegreen', 'springgreen',
    'mediumspringgreen', 'aquamarine', 'turquoise', 'aqua',
    'deepskyblue', 'dodgerblue', 'mediumslateblue', 'mediumpurple',
    'blueviolet', 'darkviolet', 'purple', 'mediumvioletred'
]


def setup(genspeed=1, turtlespeed=10, backgroundcolor='black', hide=True, resolution=(1920, 1200)):
    if hide:
        turtle.hideturtle()
    turtle.setup(*resolution)  # Laptop screen
    # turtle.setup(3840, 2200)     # 4K screen
    turtle.color('white')
    turtle.speed(turtlespeed)
    turtle.bgcolor(backgroundcolor)
    turtle.tracer(genspeed, 0)
    turtle.pensize(1)
    global speed
    speed = turtlespeed
    global drawspeed
    drawspeed = genspeed


class Transform:

    def __init__(self, func):
        self.func = func
        if isinstance(func, (list, tuple)):
            inputxy = func
            self.inputxy = func
        elif isinstance(func, (Pattern, PolarPattern, SpiralPattern, TimesTable)):
            inputxy = func.list
            self.inputxy = func.list
        if not isinstance(inputxy[0], list):
            inputxy = [list(lst) for lst in inputxy]
            self.inputxy = inputxy
        self._input = inputxy
        self.ldepth = get_depth(self.inputxy)
        if self.ldepth == 1:
            self.xlist = [i[0] for i in inputxy]
            self.ylist = [i[1] for i in inputxy]
        if self.ldepth == 2:
            self.xlist, self.ylist = [], []
            for xy in inputxy:
                if isinstance(xy, (tuple, list)) and len(xy) == 2:
                    self.xlist.append(xy[0])
                    self.ylist.append(xy[1])
                elif isinstance(xy[0], (tuple, list)) and len(xy[0]) == 2:
                    for i in xy:
                        self.xlist.append(i[0])
                        self.ylist.append(i[1])
            for i in self.xlist:
                if not isinstance(i, (float, int)):
                    print('Transform might fail, item not an integer: ', i, type(i))

        self.list = [c for c in zip(self.xlist, self.ylist)]
        if self.ldepth == 1:
            self.cartesianlist = [self.pol2cart(pc[0], pc[1]) for pc in inputxy]
            self.polarlist = [self.cart2pol(xy[0], xy[1]) for xy in inputxy]

    def __repr__(self):
        # if isinstance(self.func, (list, tuple)):
        #     return self.cartesianlist
        # else:
        #     return self.cartesianlist
        lst = list(self.cartesianlist)
        return lst

    def __str__(self):
        return str(self.cartesianlist)

    def __getitem__(self, index):
        return self.cartesianlist[index]

    def __setitem__(self, index, value):
        self.cartesianlist[index] = value

    def __len__(self):
        return len(self.cartesianlist)


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
            return self.list

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
            return newlist

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
        if isinstance(self.func, Wave):
            self.func.list = newylist
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

    def generatepointcloud(self, density, spread, exp=1):
        pointlist = []
        if self.ldepth == 1:
            for coord in self.inputxy:
                center_x, center_y = coord[0], coord[1]
                for i in range(density):
                    radius = (np.random.exponential(exp) * spread)
                    angle = np.random.uniform(0, 2 * pi)
                    x = radius * cos(angle) + center_x
                    y = radius * sin(angle) + center_y
                    point_coord = (x, y)
                    pointlist.append(point_coord)
        elif self.ldepth == 2:
            for lst in self.inputxy:
                for coord in lst:
                    print(f"coord: {coord}")
                    center_x, center_y = coord[0], coord[1]
                    for i in range(density):
                        radius = (np.random.exponential(exp) * spread)
                        angle = np.random.uniform(0, 2 * pi)
                        x = radius * cos(angle) + center_x
                        y = radius * sin(angle) + center_y
                        point_coord = (x, y)
                        pointlist.append(point_coord)
        return pointlist


class Analyze:
    def __init__(self, funclist=[[]], ldepth=1):
        self.funclist = funclist
        if isinstance(self.funclist, Pattern):
            self.funclist = self.funclist.list
            ldepth = get_depth(self.funclist)
        elif isinstance(self.funclist[0], Pattern):
            self.funclist = [i.list for i in self.funclist]
            ldepth = get_depth(self.funclist)
        self.coordlist = []
        self.ldepth = ldepth

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
        if len(points) == 0:
            print('No crosspoint canidates were found. Returning None')
        return points, avg

    def center(self, show=False):

        avgs = []
        if self.ldepth == 1:
            avgs.append(self.avgcoord(self.funclist))
            center = self.avgcoord(avgs)
        elif self.ldepth == 2:
            for i in self.funclist:
                avgs.append(self.avgcoord(i))
            xs = [xy[0] for xy in avgs]
            ys = [xy[1] for xy in avgs]
            xavg = sum(xs) / len(xs)
            yavg = sum(ys) / len(xs)
            avg = (xavg, yavg)
            center = avg
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
            distlist.append(dist)
            xydistlist.append((xdist, ydist))
        return distlist, xydistlist

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

    def avgcoord(self, coords):
        # if self.ldepth == 1:
        xs, ys = [xy[0] for xy in coords], [xy[1] for xy in coords]
        if len(xs) and len(ys) > 0:
            xavg = sum(xs) / len(xs)
            yavg = sum(ys) / len(ys)
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


class Colors:
    @staticmethod
    def rainbow(n_colors=100):
        scheme = {
            'r': [[255, 255], [255, 255], [255, 220], [220, 75], [75, 3], [3, 3], [3, 30], [30, 125], [125, 220], [220, 255]],
            'g': [[0, 150], [150, 255], [255, 255], [255, 255], [255, 255], [255, 145], [145, 3], [3, 3], [3, 3], [3, 0]],
            'b': [[0, 0], [0, 0], [0, 3], [3, 3], [3, 240], [240, 255], [255, 255], [255, 255], [255, 255], [255, 0]]}
        return ColorScheme(scheme, n_colors)

    @staticmethod
    def grayscale1(n_colors=100):
        scheme = {'r': [0, 255], 'g': [0, 255], 'b': [0, 255]}
        return ColorScheme(scheme, n_colors)

    @staticmethod
    def hot1(n_colors):
        scheme = {'r': [0, 255, 255, 255], 'g': [0, 0, 255], 'b': [0, 0]}
        return ColorScheme(scheme, n_colors)

    @staticmethod
    def hot2(n_colors):
        scheme = {'r': [0, 255, 255], 'g': [0, 0, 255], 'b': [0, 0, 0, 60]}
        return ColorScheme(scheme, n_colors)


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

    def __init__(self, lst,  colors='white', pensize=1, position=[0, 0]):
        self.list = lst
        self.position = position
        if isinstance(colors, str):
            colors = [colors]
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
        self.goto(self.list[0], penup=True)
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

    def set_depth(self):
        if isinstance(self.list[0], tuple) and isinstance(self.list[0][0], (int, float)):
            return 1
        elif isinstance(self.list[0], list):
            if isinstance(self.list[0][0], list):
                return 3
            else:
                return 2

    def simpledraw(self):
        # print('lvl1')
        for ind in range(len(self.list)):
            self.colorcycle(ind)
            turtle.goto(self.list[ind])

    def lvl2draw(self):
        # print('lvl2')
        for lst in self.list:
            for ind in range(len(lst)):
                self.colorcycle(ind)
                turtle.goto(lst[ind])

    def lvl3draw(self):
        # print('lvl3')
        for group in self.list:
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
            turtle.goto(self.position)
        else:
            turtle.goto(coord)
        turtle.pendown()

    def colorcycle(self, ind):
        length = len(self.colors)
        modind = ind % length
        turtle.color(self.colors[modind])
        return self.colors[modind]

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
            if reps == 0:
                reps = 1
            turn = abs(angle) / reps
            for j in range(reps):
                turtle.forward(curve)
                if angle < 0:
                    turtle.left(turn)
                else:
                    turtle.right(turn)


class PolarPattern:
    def __init__(self, radianlist, radiuslist, size, position=[0, 0], pensize=1,
                 xscale=1, yscale=1):
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
        if xscale != 1:
            Transform(self).xscale(xscale)
        if yscale != 1:
            Transform(self).yscale(yscale)
        self.position = position
        self._pensize = pensize

        # self.goto(self.position)

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

    def draw(self, lst=None):
        turtle.pensize(self._pensize)
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


class Wave(Pattern):
    def __init__(self, stretch=50, height=100, pensize=1, position=(0, 0), length=25,
                 color='yellow', cosin=False):
        if isinstance(color, list):
            color = color[0]
            print('Only 1 color can be used. Using first in list')
        turtle.color(color)
        if length < 0:
            self.xlist = np.linspace(length, abs(length) + (1 / (abs(length) * 25)), abs(length) * 25)
        else:
            self.xlist = np.linspace(-length, round(length + (1 / (length * 25))), round(length * 25))
        if cosin is False:
            self.ylist = [sin(x) for x in self.xlist]
        else:
            self.ylist = [cos(x) for x in self.xlist]
        self._Olist = [xy for xy in zip(self.xlist, self.ylist)]
        super().__init__(self._Olist, color, pensize, position)
        self._talllist = Transform(self._Olist).yscale(height)
        self.list = Transform(self._talllist).xscale(stretch)
        if position != (0, 0):
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


class Rectangle(Pattern):
    def __init__(self, width=50, height=50, pensize=1, position=(0, 0),
                 color='yellow'):
        if isinstance(color, list):
            color = color[0]
            print('Only 1 color can be used. Using first in list')
        turtle.color(color)
        xpos, ypos = position[0], position[1]
        topl = (xpos - (width / 2), ypos + (height / 2))
        topr = (xpos + (width / 2), ypos + (height / 2))
        botl = (xpos - (width / 2), ypos - (height / 2))
        botr = (xpos + (width / 2), ypos - (height / 2))
        self.plist = [topl, topr, botr, botl, topl]
        super().__init__(self.plist, color, pensize, position)
        self.list = Transform(self.plist).xscale(width / 2)
        self.list = Transform(self.list).yscale(height / 2)

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


class Circle(Pattern):
    def __init__(self, width=50, height=50, pensize=1, position=(0, 0),
                 color='yellow'):
        if isinstance(color, list):
            color = color[0]
            print('Only 1 color can be used. Using first in list')
        turtle.color(color)
        radius = (height / 2)
        xpos, ypos = position[0], position[1]
        self.plist = self.create_circle(radius, xpos, ypos)
        super().__init__(self.plist, color, pensize, position)
        self.list = Transform(self.plist).xscale(width / 2)
        self.list = Transform(self.list).yscale(height / 2)

    def draw(self):
        lst = self.list
        turtle.penup()
        turtle.goto(lst[0])
        turtle.pendown()
        for xy in lst:
            turtle.goto(xy)

    def create_circle(self, radius, xpos, ypos, penup=True):
        if penup:
            turtle.penup()
        else:
            turtle.pendown()
        turtle.goto((xpos - radius, ypos))
        turtle.begin_poly()
        turtle.circle(radius)
        turtle.end_poly()
        circle = [tuple(i) for i in turtle.get_poly()]
        return circle


class RadialAngularPattern(Pattern):

    def __init__(self, size, angles=[[125, 3]], turncycle=0, jank=None,
                 colors=default_color_list, pensize=1, position=[0, 0], showcenter=False, penup=False):
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
        # self.center =
        self.list = self.center(showcenter=showcenter)
        super().__init__(self.list, self.colors, pensize, self._startpos)
        if showcenter:
            self.dot((0, 0), 5)

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
            turtle.speed(speed)
            turtle.tracer(drawspeed, 1)
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

    def center(self, showcenter=False):
        precenter = Analyze(self.list, self.ldepth).center(show=showcenter)
        newlist = [(xy[0] - precenter[0], xy[1] - precenter[1]) for xy in self.list]
        # self._startpos = (self.position[0] - precenter[0], self.position[1] - precenter[1])
        return newlist


class FlowerPattern(PolarPattern):
    def __init__(self, npetals, innerdepth=3, size=50, poly=500, color='green',
                 position=[0, 0], pensize=1):
        self._npetals = npetals
        self._innerdepth = innerdepth
        self._pensize = pensize
        if isinstance(color, (ColorScheme, ColorScheme)):
            color = color.hex
        if isinstance(color, list):
            color = color[0]
            print('Only 1 color can be used. Using first in list')
        turtle.color(color)
        radianlist = np.linspace(0, 7, poly)
        radiuslist = [(3 - (innerdepth * cos(npetals * theta))) for theta in
                      radianlist]
        super().__init__(radianlist, radiuslist, size, position, pensize)


class SpiralPattern(PolarPattern):
    def __init__(self, linelength=1, diameter=100, scale=20, poly=400,
                 centerdist=0, color='orange', position=[0, 0], pensize=1,
                 xscale=1, yscale=1):
        linelength = linelength / 10
        self._tightness = linelength
        self._size = diameter
        angldiv = (diameter * poly)
        self._pensize = pensize
        if isinstance(color, (ColorScheme, ColorScheme)):
            color = color.hex
        if isinstance(color, list):
            color = color[0]
            print('Only 1 color can be used. Using first in list')
        turtle.color(color)
        radianlist = np.linspace(0, diameter, angldiv // 6)
        radiuslist = [(angl * linelength) + centerdist for angl in radianlist]
        super().__init__(radianlist, radiuslist, scale, position, pensize, xscale, yscale)


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


class DrawPath:
    def __init__(self, coordlist, pensize=1, colors='white', colordist=0, lines=True, dots=False, dotsize=1, colorsync=True, colordistthresh=None):
        notfunc = True
        if isinstance(coordlist[0], Wave):
            print('passed')
            for i in range(len(coordlist)):
                colind = i % len(colors)
                color = colors[colind]
                turtle.color(color)
                coordlist[i].draw()
            notfunc = False
        if notfunc:
            self.coordlist = coordlist
            if isinstance(pensize, (int, float)):
                self.pensize = pensize
                turtle.pensize(self.pensize)
            elif isinstance(pensize, tuple) and len(pensize) == 2:
                self.pensize = np.linspace(pensize[0], pensize[1], len(coordlist))
            self.colors = colors
            self.colorsync = colorsync
            self.colordistthresh = colordistthresh
            self.ldepth = self.set_depth()
            self.goto()
            self.colorcycle = self.colorset()
            self._colordist = colordist
            self.dotsize = dotsize
            if lines is True:
                self.draw()
            if dots is True:
                self.dots()

    def goto(self, coords=None, ldepth=None):
        if ldepth is None:
            if self.ldepth == 1:
                start = self.coordlist[0]
            elif self.ldepth == 2:
                start = self.coordlist[0][0]
            elif self.ldepth == 3:
                start = self.coordlist[0][0][0]
            else:
                print('In DrawPath.goto(), ldepth error. ldepth: ', self.ldepth)
        if coords is None:
            turtle.penup()
            turtle.goto(start)
            turtle.pendown()
        else:
            turtle.penup()
            turtle.goto(coords)
            turtle.pendown()

    def colorset(self):
        if isinstance(self.colors, (Colors, ColorScheme)):
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
        colorcount = 0
        colordist = self._colordist
        if self.ldepth == 1:
            dist = 0
            for i in range(len(self.coordlist)):
                colorcount += 1
                if dist > colordist and self.colorcycle is True:
                    if colorcount >= len(self.colors):
                        colorcount = 0
                    color = self.colors[colorcount]
                    turtle.color(color)
                    dist = 0
                pos = turtle.pos()
                turtle.goto(self.coordlist[i])
                dist += turtle.distance(pos)
            distfromstart = Analyze().distance(self.coordlist[0], self.coordlist[-1])
            turtle.goto(self.coordlist[-1])
            if distfromstart <= 5:
                self.dots(turtle.pos(), 1)
        elif self.ldepth == 2:
            for j in range(len(self.coordlist)):
                if isinstance(self.pensize, (np.ndarray, list, tuple)):
                    pensind = j % len(self.pensize)
                    turtle.pensize(self.pensize[pensind])
                colind = j % len(self.colors)
                turtle.color(self.colors[colind])
                self.goto(self.coordlist[j][0], 1)
                for i in range(len(self.coordlist[j])):
                    turtle.goto(self.coordlist[j][i])
        elif self.ldepth >= 3:
            print('Drawpath function for ldepth: ', str(self.ldepth), ' not written yet.')

    def dots(self, coords=None, size=1):
        colordistthresh = self.colordistthresh
        if coords is None:
            colcount = 0
            for i in range(len(self.coordlist)):
                if self.colorcycle is True and colordistthresh is None:
                    index = i % len(self.colors)
                    color = self.colors[index]
                    turtle.color(color)
                elif colordistthresh != None:
                    if i > 0 and i < len(self.coordlist):
                        dist = Analyze().distance(self.coordlist[i], self.coordlist[i-1])
                        if dist >= colordistthresh:
                            colcount += 1
                        colind = colcount % len(self.colors)
                        turtle.color(self.colors[colind])
                self.goto(self.coordlist[i])
                turtle.dot(self.dotsize)
        else:
            if not isinstance(coords, list):
                coords = [coords]
            for i in range(len(coords)):
                self.goto(coords[i])
                turtle.dot(size)

    def set_depth(self):
        # l = self.coordlist
        # cnt = 0
        # print('l')
        # while isinstance(l[0], (list, tuple)):
        #     cnt += 1
        #     l = l[0]
        #     print(cnt, l)
        # return cnt
        if isinstance(self.coordlist[0], tuple) and isinstance(self.coordlist[0][0], (int, float)):
            return 1
        elif isinstance(self.coordlist[0], list):
            if isinstance(self.coordlist[0][0], list):
                return 3
            else:
                return 2

    # def set_color_ld2(self):


class TimesTable:
    def __init__(self, radius=300, npoints=100, multby=2, range_=200, doublelines=False, color='white', pensize=1, rotation=0, xscale=1, yscale=1):
        if isinstance(color, str):
            self._color = [color]
        elif isinstance(color, list) or isinstance(color, ColorScheme):
            self._color = color
        else:
            print('Color type must be either a valid color string, or a list of valid color strings')
            raise TypeError
        self._npoints = npoints
        self._multby = multby
        self._range = list(range(range_))
        bigrange = list(range(range_ * 20))
        self._multlist = [n * multby for n in bigrange]
        self._doublelines = not doublelines
        self.ring = self.create_ring(radius)
        self.ring = Transform(self.ring).xscale(xscale)
        self.ring = Transform(self.ring).yscale(yscale)
        self.ring = Transform(self.ring).origin_rotate(180 + rotation)
        self._coordpairs = {bigrange[i]: self.ring[i % len(self.ring)] for i in range(len(bigrange))}
        self._pensize = pensize
        self.list = self.draw(drawcircle=False, penup=True)

    def __repr__(self):
        lst = list(self.list)
        return lst

    def create_ring(self, radius):
        turtle.penup()
        turtle.goto((0, -radius))
        turtle.begin_poly()
        turtle.circle(radius, steps=(self._npoints - 1))
        turtle.end_poly()
        return list(turtle.get_poly())

    def draw(self, drawcircle=True, penup=False):
        biglist = []
        turtle.pensize(self._pensize)
        if penup:
            turtle.penup()
        else:
            turtle.pendown()
        if drawcircle:
            self.draw_circle()
        self.goto(self.ring[0], True)
        turtle.begin_poly()
        for i in range(len(self._range)):
            colind = i % len(self._color)
            ind = i % self._npoints
            product = i * self._multby
            # if product < 200:
            turtle.color(self._color[colind])
            self.goto(self.ring[ind], penup=self._doublelines)
            self.goto(self._coordpairs[i * self._multby])
        turtle.end_poly()
        lst = [tuple(i) for i in turtle.get_poly()]
        biglist.append(lst)
        # print('list: ', biglist, 'len: ', len(lst))
        return biglist

    def draw_circle(self):
        turtle.penup()
        turtle.goto(self.ring[0])
        turtle.pendown()
        for i in range(len(self.ring)):
            colind = i % len(self._color)
            turtle.color(self._color[colind])
            turtle.goto(self.ring[i])

    @staticmethod
    def goto(coord, penup=False):
        if penup:
            turtle.penup()
        else:
            turtle.pendown()
        turtle.goto(coord)
        turtle.pendown()


class CascadeLines(Pattern):
    def __init__(self, nlines=160, lengthrange=(5, 500), distrange=(10, 600), pensizerange=(1, 10), rotation=0, color='white', position=(0, 0)):
        self._nlines = nlines
        self._lenlist = np.linspace(lengthrange[0], lengthrange[1], nlines)
        self._distlist = np.linspace(distrange[0], distrange[1], nlines)
        self._penrange = np.linspace(pensizerange[0], pensizerange[1], nlines)
        self._startpos = position
        self._rotation = rotation
        self.paths = self.draw()
        super().__init__(self.paths)

    def draw(self):
        pathlist = []
        turtle.penup()
        turtle.goto((self._startpos[0] - (self._lenlist[0] / 2), self._startpos[1]))
        for i in range(self._nlines):
            turtle.penup()
            turtle.goto((self._startpos[0] - (self._lenlist[i] / 2), self._startpos[1] - self._distlist[i]))
            # turtle.setheading(i * 3)
            turtle.setheading(0)
            # turtle.pendown()
            turtle.begin_poly()
            # turtle. circle(self._lenlist[i], 280)
            turtle.forward(self._lenlist[i])
            turtle.end_poly()
            line = list(turtle.get_poly())
            if self._rotation > 0:
                line = Transform(line).rotate(self._rotation * i, center=self._startpos)
            pathlist.append(line)
        return pathlist


class LVL2:
    @staticmethod
    def layered_flowers(layers=30, npetals=6, innerdepth=3, sizefactor=2,
                        pensize=1, rotate=0, rotaterate=1, colors=default_color_list,
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
            f = FlowerPattern(npetals, innerdepth, sf, color=color2, pensize=pensize)
            sf += 1 * sizefactor
            if rotate != 0:
                Transform(f).rotate(rotate * rotationfactor)
                rotationfactor += rotaterate
            if position != [0, 0]:
                Transform(f).xshift(position[0])
                Transform(f).yshift(position[1])
            f.draw()

    @staticmethod
    def sin_spiral(strands=20, xshift=10, yshift=0, rotate=0, rotaterate=1,
                   rotatecenter=[0, 0], colors=default_color_list, wavelength=50, amplitude=100, wlshift=0,
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
                    for val in xy:
                        pass
            funclist.append(sin1.list)
            pathlist.append(sin1.list)
        # checkptz, point = Analyze(funclist).crosspoint()
        # turtle.color('white')
        # turtle.penup()
        # # turtle.goto(point)
        # turtle.pendown()
        # turtle.dot(5)
        return pathlist

    @staticmethod
    def sin_avg_point_rotation(strands=20, xshift=10, yshift=0,
                               rotate=1, rotaterate=1, individualrotation=0, totalrotation=None,
                               colors=default_color_list, wavelength=50, amplitude=100, wlshift=0,
                               ampshift=0, length=25, lenshift=0, idkyet=False, cosine=False, pensize=1, connectends=False, webends=False,
                               position=[0, 0], showpoint=False, draworig=False, getpoint=False):
        funclist = []
        xpos, ypos = position[0], position[1]
        wavelength2 = wavelength
        amplitude2 = amplitude
        length2 = length
        wavelength3 = wavelength
        amplitude3 = amplitude
        length3 = length
        lenshift = lenshift / 100
        for i in range(strands):
            colind = i % len(colors)
            col = colors[colind]
            if not idkyet:
                length2 = length
            sin1 = Wave(stretch=wavelength2, height=amplitude2, color=col,
                        position=[xpos, ypos], length=length2, cosin=cosine)
            xpos += xshift
            ypos += yshift
            wavelength2 += wlshift
            amplitude2 += ampshift
            length2 += lenshift
            funclist.append(sin1.list)
            if draworig is True:
                sin1.draw()
        _, rotation_point = Analyze(funclist).crosspoint()
        center = Analyze(funclist, ldepth=get_depth(funclist)).center(show=False)
        # dot(center, 10)
        print('center: ', center)

        """Part 2"""
        # else:
        rotationfactor = 1
        funclist2 = []
        if totalrotation is None:
            totalrotation = -(rotate * (strands / 2))
        for i in range(strands):
            colind = i % len(colors)
            col = colors[colind]
            sin1 = Wave(stretch=wavelength, height=amplitude, color=col,
                        position=[xpos, ypos], length=length, cosin=cosine, pensize=pensize)
            xpos += xshift
            ypos += yshift
            wavelength += wlshift
            amplitude += ampshift
            length += lenshift
            if rotate != 0 and rotation_point is not None:
                Transform(sin1).rotate(rotate * rotationfactor, rotation_point)
                rotationfactor += rotaterate
            else:
                rotation_point = (0, 0)
            if totalrotation > 0:
                Transform(sin1).rotate(totalrotation, center)
            funclist2.append(sin1)
            if individualrotation != 0:
                indcenter = Analyze(sin1).center()
                Transform(sin1).rotate(individualrotation * (i / 10), indcenter)
        center2 = Analyze(funclist2, ldepth=get_depth(funclist2)).center(show=False)

        """Part 3"""
        if center2 != position:
            xdiff = position[0] - center2[0]
            ydiff = position[1] - center2[1]
            Transform(sin1).xshift(xdiff)
            Transform(sin1).yshift(ydiff)
        xpos, ypos = position[0] - xdiff, position[1] - ydiff
        rotationfactor = 1
        funclist3 = []
        endlists = []
        endliste = []
        if totalrotation is None:
            totalrotation = -(rotate * (strands / 2))
        for i in range(strands):
            colind = i % len(colors)
            col = colors[colind]
            sin1 = Wave(stretch=wavelength3, height=amplitude3, color=col,
                        position=[xpos, ypos], length=length3, cosin=cosine, pensize=pensize)
            xpos += xshift
            ypos += yshift
            wavelength3 += wlshift
            amplitude3 += ampshift
            length3 += lenshift
            if rotate != 0 and rotation_point is not None:
                Transform(sin1).rotate(rotate * rotationfactor, rotation_point)
                rotationfactor += rotaterate
            else:
                rotation_point = (0, 0)
            if totalrotation > 0:
                Transform(sin1).rotate(totalrotation, center)
            funclist3.append(sin1)
            if individualrotation != 0:
                indcenter = Analyze(sin1).center()
                Transform(sin1).rotate(individualrotation * (i / 10), indcenter)

            if i > 0:
                if connectends or webends:
                    endlists.append(sin1[0])
                    endliste.append(sin1[-1])
            if center2 != position:
                xdiff = position[0] - center2[0]
                ydiff = position[1] - center2[1]
                Transform(sin1).xshift(xdiff)
                Transform(sin1).yshift(ydiff)

        if not draworig:
            curfunc = funclist3
            for i in range(len(curfunc)):
                colind = i % len(colors)
                col = colors[colind]
                turtle.color(col)
                curfunc[i].draw()

        if webends:
            turtle.penup()
            turtle.goto(endlists[0])
            turtle.pendown()
            for i in range(len(endlists)):
                colind = i % len(colors)
                col = colors[colind]
                turtle.color(col)
                turtle.goto(endlists[i])

        if connectends == 1 or connectends == 3:

            # Sorting endlist starts
            sorted_endlists = []
            els_copy = endlists.copy()
            sorted_endlists.append(endlists[0])
            ind = 0
            while len(els_copy) > 1:
                sorted_endlists.append(els_copy[ind])
                point = els_copy[ind]
                els_copy.pop(ind)
                ind = closest_point(point, els_copy)
                print(ind)

            thresh = 20
            turtle.penup()
            turtle.goto(sorted_endlists[0])
            turtle.tracer(10, 0)
            turtle.pendown()
            for i in range(len(sorted_endlists)):
                colors = ['white']
                colind = i % len(colors)
                col = colors[colind]
                turtle.color(col)
                dist = Analyze().distance(sorted_endlists[i], sorted_endlists[i - 1])
                if abs(dist) > thresh:
                    turtle.penup()
                else:
                    turtle.pendown()
                turtle.goto(sorted_endlists[i])
                turtle.color('white')
                # turtle.dot()

        if connectends == 2 or connectends == 3:

            # Sorting endlist ends
            sorted_endliste = []
            ele_copy = endliste.copy()
            sorted_endliste.append(endliste[0])
            ind = 0
            while len(ele_copy) > 1:
                sorted_endliste.append(ele_copy[ind])
                point = ele_copy[ind]
                ele_copy.pop(ind)
                ind = closest_point(point, ele_copy)
                print(ind)

            thresh = 20
            turtle.penup()
            turtle.goto(sorted_endliste[0])
            turtle.tracer(10, 0)
            turtle.pendown()
            for i in range(len(sorted_endliste)):
                colors = ['white']
                colind = i % len(colors)
                col = colors[colind]
                turtle.color(col)
                dist = Analyze().distance(sorted_endliste[i], sorted_endliste[i - 1])
                if abs(dist) > thresh:
                    turtle.penup()
                else:
                    turtle.pendown()
                turtle.goto(sorted_endliste[i])
                turtle.color('white')

        if showpoint is True and rotation_point is not None:
            # dot(rotation_point, 6, 'white')
            dot(center, 6, 'yellow')
        if getpoint is True:
            return funclist2, rotation_point
        else:
            return funclist2

    @staticmethod
    def spiral_spiral(reps=30, rotation=5, curve=10, diameter=10, scale=20,
                      poly=400, centerdist=0, colors=default_color_list):
        rotate = 0
        for i in range(reps):
            colind = i % len(colors)
            col = colors[colind]
            spiral = SpiralPattern(linelength=curve, diameter=diameter,
                                   scale=scale, poly=poly,
                                   centerdist=centerdist, color=col)
            Transform(spiral).rotate(rotate)
            spiral.draw()
            rotate += rotation

    @staticmethod
    def antenas(colors=default_color_list, xshift=5, yshift=0, position=[100, 100]):
        xloc, yloc = position[0], position[1]
        for i in range(10):
            colind = i % len(colors)
            col = colors[colind]
            sp1 = SpiralPattern(30, 3, color=col, position=[xloc, yloc])
            sp1.draw()
            xloc += xshift
            yloc += yshift

    @staticmethod
    def iterative_rotation(function=Wave, reps=30, xshift=0, yshift=0, stretch=20, length=30, depth=30,
                           stretchshift=0, lenshift=0, depthshift=0, shift=False, colors='white', pensize=1,
                           individualrotation=2, rotationcenter=(0, 0), position=(0, 0), draworig=False, branches=10):
        funclist = []
        xpos, ypos = position[0], position[1]
        lenshift = lenshift
        length2 = length
        depth2 = depth
        stretch2 = stretch
        indrotate2 = individualrotation
        if isinstance(colors, str):
            colors = [colors]
        for i in range(reps):
            colind = i % len(colors)
            col = colors[colind]
            func1 = function(stretch2, depth2, pensize, (xpos, ypos), length2, col, shift)
            xpos += xshift
            ypos += yshift
            length2 += lenshift
            depth2 += depthshift
            stretch2 += stretchshift
            func1 = func1.list
            if indrotate2 != 0:
                func1 = Transform(func1).rotate(indrotate2, rotationcenter)
                indrotate2 += individualrotation
            funclist.append(func1)
            if draworig is True:
                func1.draw()

        if branches != 0 or branches != 1:

            orig = funclist.copy()

            angle = 360 / branches

            for i in range(branches - 1):
                for b in orig:
                    new = Transform(b).rotate((angle * (i + 1)), position)
                    funclist.append(new)

        # center = Analyze(funclist, ldepth=get_depth(funclist)).center(show=True)

        # """Part 2"""
        # # else:
        # rotationfactor = 1
        # funclist2 = []
        # if totalrotation is None:
        #     totalrotation = -(rotate * (reps / 2))
        # for i in range(reps):
        #     colind = i % len(colors)
        #     col = colors[colind]
        #     func1 = Wave(stretch=wavelength, height=amplitude, color=col,
        #                 position=[xpos, ypos], length=length, cosin=cosine, pensize=pensize)
        #     xpos += xshift
        #     ypos += yshift
        #     wavelength += wlshift
        #     amplitude += ampshift
        #     length += lenshift
        #     if rotate != 0 and rotation_point is not None:
        #         Transform(func1).rotate(rotate * rotationfactor, rotation_point)
        #         rotationfactor += rotaterate
        #     else:
        #         rotation_point = (0, 0)
        #     if totalrotation > 0:
        #         Transform(func1).rotate(totalrotation, center)
        #     funclist2.append(func1)
        #     if individualrotation != 0:
        #         indcenter = Analyze(func1).center()
        #         Transform(func1).rotate(individualrotation * (i / 10), indcenter)
        # center2 = Analyze(funclist2, ldepth=get_depth(funclist2)).center(show=showpoint)
        #
        # """Part 3"""
        # if center2 != position:
        #     xdiff = position[0] - center2[0]
        #     ydiff = position[1] - center2[1]
        #     Transform(func1).xshift(xdiff)
        #     Transform(func1).yshift(ydiff)
        # xpos, ypos = position[0] - xdiff, position[1] - ydiff
        # rotationfactor = 1
        # funclist3 = []
        # endlists = []
        # endliste = []
        # if totalrotation is None:
        #     totalrotation = -(rotate * (reps / 2))
        # for i in range(reps):
        #     colind = i % len(colors)
        #     col = colors[colind]
        #     func1 = Wave(stretch=wavelength3, height=amplitude3, color=col,
        #                 position=[xpos, ypos], length=length3, cosin=cosine, pensize=pensize)
        #     xpos += xshift
        #     ypos += yshift
        #     wavelength3 += wlshift
        #     amplitude3 += ampshift
        #     length3 += lenshift
        #     if rotate != 0 and rotation_point is not None:
        #         Transform(func1).rotate(rotate * rotationfactor, rotation_point)
        #         rotationfactor += rotaterate
        #     else:
        #         rotation_point = (0, 0)
        #     if totalrotation > 0:
        #         Transform(func1).rotate(totalrotation, center)
        #     funclist3.append(func1)
        #     if individualrotation != 0:
        #         indcenter = Analyze(func1).center()
        #         Transform(func1).rotate(individualrotation * (i / 10), indcenter)
        #
        #     if i > 0:
        #         if connectends or webends:
        #             endlists.append(func1[0])
        #             endliste.append(func1[-1])
        #     if center2 != position:
        #         xdiff = position[0] - center2[0]
        #         ydiff = position[1] - center2[1]
        #         Transform(func1).xshift(xdiff)
        #         Transform(func1).yshift(ydiff)
        #
        if not draworig:
            curfunc = funclist
            for i in range(len(curfunc)):
                colind = i % len(colors)
                col = colors[colind]
                turtle.color(col)
                DrawPath(curfunc[i], colors=col, pensize=pensize)
                # curfunc[i].draw()
        #
        # if webends:
        #     turtle.penup()
        #     turtle.goto(endlists[0])
        #     turtle.pendown()
        #     for i in range(len(endlists)):
        #         colind = i % len(colors)
        #         col = colors[colind]
        #         turtle.color(col)
        #         turtle.goto(endlists[i])
        #
        # if connectends == 1 or connectends == 3:
        #
        #     # Sorting endlist starts
        #     sorted_endlists = []
        #     els_copy = endlists.copy()
        #     sorted_endlists.append(endlists[0])
        #     ind = 0
        #     while len(els_copy) > 1:
        #         sorted_endlists.append(els_copy[ind])
        #         point = els_copy[ind]
        #         els_copy.pop(ind)
        #         ind = closest_point(point, els_copy)
        #         print(ind)
        #
        #     thresh = 20
        #     turtle.penup()
        #     turtle.goto(sorted_endlists[0])
        #     turtle.tracer(10, 0)
        #     turtle.pendown()
        #     for i in range(len(sorted_endlists)):
        #         colors = ['white']
        #         colind = i % len(colors)
        #         col = colors[colind]
        #         turtle.color(col)
        #         dist = Analyze().distance(sorted_endlists[i], sorted_endlists[i - 1])
        #         if abs(dist) > thresh:
        #             turtle.penup()
        #         else:
        #             turtle.pendown()
        #         turtle.goto(sorted_endlists[i])
        #         turtle.color('white')
        #         # turtle.dot()
        #
        # if connectends == 2 or connectends == 3:
        #
        #     # Sorting endlist ends
        #     sorted_endliste = []
        #     ele_copy = endliste.copy()
        #     sorted_endliste.append(endliste[0])
        #     ind = 0
        #     while len(ele_copy) > 1:
        #         sorted_endliste.append(ele_copy[ind])
        #         point = ele_copy[ind]
        #         ele_copy.pop(ind)
        #         ind = closest_point(point, ele_copy)
        #         print(ind)
        #
        #     thresh = 20
        #     turtle.penup()
        #     turtle.goto(sorted_endliste[0])
        #     turtle.tracer(10, 0)
        #     turtle.pendown()
        #     for i in range(len(sorted_endliste)):
        #         colors = ['white']
        #         colind = i % len(colors)
        #         col = colors[colind]
        #         turtle.color(col)
        #         dist = Analyze().distance(sorted_endliste[i], sorted_endliste[i - 1])
        #         if abs(dist) > thresh:
        #             turtle.penup()
        #         else:
        #             turtle.pendown()
        #         turtle.goto(sorted_endliste[i])
        #         turtle.color('white')
        #
        # if showpoint is True and rotation_point is not None:
        #     dot(rotation_point, 6, 'white')
        #     dot(center, 6, 'white')
        # if getpoint is True:
        #     return funclist2, rotation_point
        # else:
        #     return funclist2

    @staticmethod
    def random_iterative_rotation(function=None, reps=None, xshift=None, yshift=None, stretch=None, length=None, depth=None,
                           stretchshift=None, lenshift=None, depthshift=None, shift=False, colors='white', pensize=1,
                           individualrotation=None, rotationcenter=(None, None), position=(0, 0), draworig=False, branches=None):

        report = ""
        if function is None:
            flist = [Wave, Rectangle, Circle]
            funcindex = int(np.random.randint(0, len(flist) - 1, 1))
            print(funcindex)
            function = flist[funcindex]
            report += " fucntion={}".format(str(function))
        if reps is None:
            reps = int(np.random.randint(1, 100, 1))
            report += ", reps={}".format(reps)
        if xshift is None:
            xshift = round(abs(float(np.random.randn())) * 2, 2)
            report += ", xshift={}".format(xshift)
        if yshift is None:
            yshift = round(abs(float(np.random.randn())) * 2, 2)
            report += ", yshift={}".format(yshift)
        if stretch is None:
            stretch = round(abs(float(np.random.randn())) * 20, 2)
            report += ", stretch={}".format(stretch)
        if length is None:
            length = round(abs(float(np.random.randn())) * 20, 2)
            report += ", length={}".format(length)
        if depth is None:
            depth = round(abs(float(np.random.randn())) * 20, 2)
            report += ", depth={}".format(depth)
        if stretchshift is None:
            stretchshift = round(float(np.random.randn()) * 2, 2)
            report += ", stretchshift={}".format(stretchshift)
        if lenshift is None:
            lenshift = round(float(np.random.randn()) * 2, 2)
            report += ", lenshift={}".format(lenshift)
        if depthshift is None:
            depthshift = round(abs(float(np.random.randn())) * 5, 2)
            report += ", depthshift={}".format(depthshift)
        if individualrotation is None:
            individualrotation = round(abs(float(np.random.randn(1))) * 10, 2)
            report += ", individualrotation={}".format(individualrotation)
        if rotationcenter[0] is None:
            rotationcenter = (int(np.random.randint(-300, 300)), rotationcenter[1])
            reportrotcenter = True
        if rotationcenter[1] is None:
            rotationcenter = (rotationcenter[0], int(np.random.randint(-300, 300)))
            reportrotcenter = True
        if reportrotcenter:
            report += ", rotationcenter={}".format(rotationcenter)
        if branches is None:
            branches = int(np.random.randint(1, 31, 1))
            report += ", branches={}".format(branches)
        print(report)

        colors2 = ColorScheme(colors, reps)

        LVL2.iterative_rotation(function, reps, xshift, yshift, stretch, length, depth,
                                stretchshift, lenshift, depthshift, shift, colors2, pensize,
                                individualrotation, rotationcenter, position, draworig, branches)


def closest_point(node, nodes):
    closest_index = distance.cdist([node], nodes).argmin()
    return closest_index


def get_depth(coordlist):
    depth = 0
    if isinstance(coordlist[0], tuple) and isinstance(coordlist[0][0], (int, float)):
        depth = 1
    elif isinstance(coordlist[0], list):
        if isinstance(coordlist[0][0], list):
            depth = 3
        else:
            depth = 2
    if depth > 0:
        return depth
    else:
        print('Error: no list-depth detected in get_depth function!')
        return depth


def dot(loc=(0, 0), size=3, color='white'):
    turtle.penup()
    turtle.goto(loc)
    turtle.color(color)
    turtle.dot(size)


def wait():
    turtle.hideturtle()
    turtle.done()
    # turtle.exitonclick()


def reset():
    turtle.reset()


def bye():
    turtle.bye()