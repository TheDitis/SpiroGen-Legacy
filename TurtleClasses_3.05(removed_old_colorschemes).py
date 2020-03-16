import turtle
import random
import itertools
import numpy as np
from math import *
from matplotlib.colors import rgb2hex as pltcolors


# TODO: Point cloud generator
# TODO: Imporve centering function

color_list = [
    'red', 'crimson', 'orangered', 'darkorange', 'orange', 'gold',
    'yellow', 'greenyellow', 'lawngreen', 'limegreen', 'springgreen',
    'mediumspringgreen', 'aquamarine', 'turquoise', 'aqua',
    'deepskyblue', 'dodgerblue', 'mediumslateblue', 'mediumpurple',
    'blueviolet', 'darkviolet', 'purple', 'mediumvioletred'
]


# class Turt:
#
#     def __init__(self, color=color_list, pensize=1, speed=10, xy=[0, 0],
#                  heading=0, turt=None):
#         if turt is None:
#             self._turt = turtle.Turtle()
#             self._turt.hideturtle()
#         else:
#             self._turt = turt
#         self._color = color
#         self._size = pensize
#         if isinstance(self._color, str):
#             self._turt.color(self._color)
#         if isinstance(self._color, list):
#             self._turt.color(self._color[0])
#         self._turt.pensize(self._size)
#         self._speed = speed
#         self._heading = heading
#         self._turt.pensize(self._size)
#         self._turt.speed(self._speed)
#         self._turt.penup()
#         self._turt.goto(xy[0], xy[1])
#         self._turt.seth(self._heading)
#         self._xy = self._turt.pos()
#         self._turt.pendown()
#
#     @property
#     def color(self):
#         return self._color
#
#     @property
#     def pensize(self):
#         return self._size
#
#     @property
#     def speed(self):
#         return self._speed
#
#     @property
#     def heading(self):
#         return self._heading
#
#     @property
#     def position(self):
#         return self._xy
#
#     @color.setter
#     def color(self, col):
#         self._color = col
#         self.turtle.color(self._color)
#
#     @pensize.setter
#     def pensize(self, size):
#         print("pen getter method called")
#         self._size = size
#         self.turtle.pensize(self._size)
#
#     @speed.setter
#     def speed(self, spd):
#         self._speed = spd
#         self.turtle.speed(self._speed)
#
#     @heading.setter
#     def heading(self, dir):
#         self._heading = dir
#         self.turtle.seth(self._heading)
#
#     @position.setter
#     def position(self, xy):
#         self.turtle.penup()
#         self._xy = xy
#         self.turtle.goto(xy[0], xy[1])
#         self.turtle.pendown()
#
#     def forward(self, dist):
#         # self._turt.pendown()
#         self._turt.forward(dist)
#
#     def angle(self, angle):
#         if angle < 0:
#             self._turt.left(abs(angle))
#         else:
#             self._turt.right(angle)
#
#     def color_gen(self, i):
#         if isinstance(self._color, str):
#             color_list = [self._color]
#         else:
#             color_list = [x for x in self._color]
#         ind = (i + 1) % len(color_list)
#         return color_list[ind]
# class OColorCycle:
#     def __init__(self, colorlist, turt):
#         self._color = colorlist
#         self._turt = turt
#         # print(self._color, self._turt)
#
#     def colorsetter(self, ind):
#         length = len(self._color)
#         modind = ind % length
#         # print('colorsetter called')
#         # print(modind)
#         # print(self._color[modind])
#         self._turt.color(self._color[modind])
#         return self._color[modind]
# class OTurn(Turt):
#
#     def __init__(self, turt, angle, curve=None, curvesize=5):
#         super().__init__(turt=turt)
#         self._angle = angle
#         self._curve = curve
#         self._curvesize = curvesize
#
#     def go(self):
#         if self._curve is None or self._curve == 0:
#             self._turt.right(self._angle)
#         else:
#             reps = round(abs(self._angle) / 10)
#             turn = abs(self._angle) / reps
#             for j in range(reps):
#                 self._turt.forward(self._curvesize)
#                 if self._angle < 0:
#                     self._turt.left(turn)
#                 else:
#                     self._turt.right(turn)
# class OldRadialAngularPattern(Turt):
#
#     def __init__(self, size, angles=[[125, 1, 3]], turncycle=0, jank=None,
#                  colors=color_list, turt=None, pensize=1, position=[0, 0]):
#         super().__init__(colors, pensize=pensize, turt=turt)
#         self._size = size
#         self._angles = angles
#         self._turncycle = turncycle
#         self._jank = jank
#         self._position = position
#         if isinstance(colors, (ColorScheme, ColorScheme)):
#             colors = colors.hex
#         elif isinstance(colors, str):
#             colors = [colors]
#         self._colorlist = colors
#         self._turnlist = []
#         if isinstance(angles, int):
#             self._angles = [[angles]]
#             angles = [[angles]]
#         if isinstance(angles[0], int):
#             self._angles = [angles]
#             angles = [angles]
#         for i in range(len(self._angles)):
#             self.create_turns(i)
#         # self._turnlist = [self.turn1, self.turn2, self.turn3, self.turn4]
#         self._nTurns = [t for t in self._turnlist if t is not None]
#         self._turt.position = [-(size / 2), (size / 2)]
#         self._startpos = self._turt.position
#         self.goto()
#         self.center()
#
#     def create_turns(self, n):
#         tparams = self._angles[n]
#         # print(self._angles, tparams)
#         if n == 0:
#             self.turn1 = Turn(self._turt, *tparams)
#             self._turnlist.append(self.turn1)
#         if n == 1:
#             self.turn2 = Turn(self._turt, *tparams)
#             self._turnlist.append(self.turn2)
#         if n == 2:
#             self.turn3 = Turn(self._turt, *tparams)
#             self._turnlist.append(self.turn3)
#         if n == 3:
#             self.turn4 = Turn(self._turt, *tparams)
#             self._turnlist.append(self.turn4)
#
#     def draw(self):
#         if len(self._nTurns) == 1:
#             self.oneangle()
#         elif len(self._nTurns) == 2:
#             self.twoangle()
#         elif len(self._nTurns) == 3:
#             self.threeangle()
#         elif len(self._nTurns) == 4:
#             self.fourangle()
#
#     def oneangle(self):
#
#         for k in range(100):
#
#             ColorCycle(self._colorlist, self._turt).colorsetter(k)
#
#             self.anglego(0)
#             if self.checkplace():
#                 self._turt.position = self._startpos
#                 break
#
#     def twoangle(self):
#
#         for k in range(100):
#
#             ColorCycle(self._color, self._turt).colorsetter(k)
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
#                 self._turt.forward(self._jank)
#
#             if self.checkplace():
#                 self._turt.position = self._startpos
#                 break
#
#     def threeangle(self):
#
#         for k in range(100):
#
#             ColorCycle(self._color, self._turt).colorsetter(k)
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
#                 self._turt.forward(self._jank)
#
#             if self.checkplace():
#                 self._turt.position = self._startpos
#                 break
#
#     def fourangle(self):
#
#         for k in range(100):
#
#             ColorCycle(self._color, self._turt).colorsetter(k)
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
#                 self._turt.forward(self._jank)
#
#             if self.checkplace():
#                 self._turt.position = self._startpos
#                 break
#
#     def anglego(self, n):
#         self._turt.forward(self._size)
#         self._nTurns[n].go()
#
#     def checkplace(self):
#         sx, sy = round(self._startpos[0]), round(self._startpos[1])
#         current = self._turt.pos()
#         x, y = round(current[0]), round(current[1])
#         if sx == x and sy == y:
#             return True
#         else:
#             return False
#
#     def goto(self):
#         self._turt.penup()
#         self._turt.goto(self._position)
#         self._turt.pendown()
#
#     def center(self):
#         self._turt.penup()
#         self._turt.goto(- (self._size / 2), 0)
#         self._turt.pendown()


# class ORadialAngularPattern(Turt):
#
#     def __init__(self, size, angles=[[125, 1, 3]], turncycle=0, jank=None,
#                  colors=color_list, turt=None, pensize=1, position=[0, 0]):
#         super().__init__(colors, pensize=pensize, turt=turt)
#         self._size = size
#         self._angles = angles
#         self._turncycle = turncycle
#         self._jank = jank
#         self._position = position
#         if isinstance(colors, (ColorScheme, ColorScheme)):
#             colors = colors.hex
#         elif isinstance(colors, str):
#             colors = [colors]
#         self._colorlist = colors
#         self._turnlist = []
#         if isinstance(angles, int):
#             self._angles = [[angles]]
#             angles = [[angles]]
#         if isinstance(angles[0], int):
#             self._angles = [angles]
#             angles = [angles]
#         for i in range(len(self._angles)):
#             self.create_turns(i)
#         # self._turnlist = [self.turn1, self.turn2, self.turn3, self.turn4]
#         self._nTurns = [t for t in self._turnlist if t is not None]
#         self._turt.position = [-(size / 2), (size / 2)]
#         self._startpos = self._turt.position
#         print(self._turt.position)
#         self.goto()
#         self.center()
#
#     def create_turns(self, n):
#         tparams = self._angles[n]
#         # print(self._angles, tparams)
#         if n == 0:
#             self.turn1 = Turn(self._turt, *tparams)
#             self._turnlist.append(self.turn1)
#         if n == 1:
#             self.turn2 = Turn(self._turt, *tparams)
#             self._turnlist.append(self.turn2)
#         if n == 2:
#             self.turn3 = Turn(self._turt, *tparams)
#             self._turnlist.append(self.turn3)
#         if n == 3:
#             self.turn4 = Turn(self._turt, *tparams)
#             self._turnlist.append(self.turn4)
#
#     def draw(self):
#         if len(self._nTurns) == 1:
#             self.oneangle()
#         elif len(self._nTurns) == 2:
#             self.twoangle()
#         elif len(self._nTurns) == 3:
#             self.threeangle()
#         elif len(self._nTurns) == 4:
#             self.fourangle()
#
#     def oneangle(self):
#
#         for k in range(100):
#
#             ColorCycle(self._colorlist, self._turt).colorsetter(k)
#
#             self.anglego(0)
#             if self.checkplace():
#                 self._turt.position = self._startpos
#                 break
#
#     def twoangle(self):
#
#         for k in range(100):
#
#             ColorCycle(self._color, self._turt).colorsetter(k)
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
#                 self._turt.forward(self._jank)
#
#             if self.checkplace():
#                 self._turt.position = self._startpos
#                 break
#
#     def threeangle(self):
#
#         for k in range(100):
#
#             ColorCycle(self._color, self._turt).colorsetter(k)
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
#                 self._turt.forward(self._jank)
#
#             if self.checkplace():
#                 self._turt.position = self._startpos
#                 break
#
#     def fourangle(self):
#
#         for k in range(100):
#
#             ColorCycle(self._color, self._turt).colorsetter(k)
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
#                 self._turt.forward(self._jank)
#
#             if self.checkplace():
#                 self._turt.position = self._startpos
#                 break
#
#     def anglego(self, n):
#         self._turt.forward(self._size)
#         self._nTurns[n].go()
#
#     def checkplace(self):
#         sx, sy = round(self._startpos[0]), round(self._startpos[1])
#         current = self._turt.pos()
#         x, y = round(current[0]), round(current[1])
#         if sx == x and sy == y:
#             return True
#         else:
#             return False
#
#     def goto(self):
#         self._turt.penup()
#         self._turt.goto(self._position)
#         # if self.penup is False:
#         self._turt.pendown()
#
#     def center(self):
#         self._turt.penup()
#         self._turt.goto(- (self._size / 2), 0)
#         self._turt.pendown()
#
#     def capturepath(self, penup=True):
#         if penup is True:
#             self._turt.penup()
#         self._turt.begin_poly()
#         if len(self._nTurns) == 1:
#             self.oneangle()
#         elif len(self._nTurns) == 2:
#             self.twoangle()
#         elif len(self._nTurns) == 3:
#             self.threeangle()
#         elif len(self._nTurns) == 4:
#             self.fourangle()
#         self._turt.end_poly()
#         return self._turt.get_poly()

# class OldColorScheme:
#
#     def __init__(self, listlen, Rrange=[0, 0], Grange=[0, 0], Brange=[0, 0], Rfactor=0):        #Takes length of list and range to be spanned over that length for each color
#         self._length = listlen                                  #
#         self._RedR = Rrange
#         self._GreenR = Grange
#         self._BlueR = Brange
#         self.rgbcolors = []
#         self.rgbcolorscale = []
#         self.hex = []
#         self.assign()
#
#     def assign(self):
#         factor = (1 / 255)
#         R1, R2 = self._RedR[0], self._RedR[1]
#         G1, G2 = self._GreenR[0], self._GreenR[1]
#         B1, B2 = self._BlueR[0], self._BlueR[1]
#         Rmin, Rmax = min(R1, R2), max(R1, R2)
#         Gmin, Gmax = min(G1, G2), max(G1, G2)
#         Bmin, Bmax = min(B1, B2), max(B1, B2)
#         Rintrvl = (Rmax - Rmin) / self._length
#         Gintrvl = (Gmax - Gmin) / self._length
#         Bintrvl = (Bmax - Bmin) / self._length
#         if R1 > R2:
#             Rintrvl = -Rintrvl
#         if G1 > G2:
#             Gintrvl = -Gintrvl
#         if B1 > B2:
#             Bintrvl = -Bintrvl
#         NewR, NewG, NewB = R1, G1, B1
#         for i in range(self._length):
#             rgb = [NewR, NewG, NewB]
#             rgbfloats = [i * factor for i in rgb]
#             rgb = [int(round(n)) for n in rgb]
#             rgbfloats = [round(n, 2) for n in rgbfloats]
#             NewR, NewG, NewB = NewR + Rintrvl, NewG + Gintrvl, NewB + Bintrvl
#             self.rgbcolors.append(rgb)
#             self.rgbcolorscale.append(rgbfloats)
#         self._hexconvert()
#
#     def _hexconvert(self):
#         for i in self.rgbcolorscale:
#             hexcol = pltcolors(i)
#             self.hex.append(hexcol)


# class OldColorSchemeDict:
#
#     def __init__(self, colordict, ncolors=50):
#         self.redlist = colordict['r']
#         self.greenlist = colordict['g']
#         self.bluelist = colordict['b']
#         self.ncolors = ncolors
#         self.keylist = ['r', 'g', 'b']
#         # self.cols = {'r': redlist, 'g': greenlist, 'b': bluelist}
#         self.cols = colordict
#         self.check_inputs()
#         self.rlist = self.cols['r']
#         self.glist = self.cols['g']
#         self.blist = self.cols['b']
#         self.rgbdivs = {}
#         self.roundto = 3
#         self.set_transition_divisions()
#         self.rvals, self.gvals, self.bvals = self.set_fades()
#         self.rgbcolors = self.join_colors()
#         self.rgb0to1 = self.scale0to1(self.rgbcolors)
#         self.hex = []
#         self.hexconvert()
#
#     def check_inputs(self):
#         for k in self.keylist:
#             current = self.cols[k]
#             if isinstance(current, int):
#                 print('Inputs must be in the form of a list of lists')
#             if not isinstance(current[0], list):
#                 self.cols[k] = [self.cols[k]]
#             for l in range(len(current)):
#                 if len(current[l]) == 1:
#                     self.cols[k][l] = [current[l][0], current[l][0]]
#                     print('Revising short list', self.cols[k][l])
#                 if len(current[l]) > 2:
#                     print('Color value lists can have no more than 2 numbers')
#                     print(current[l], 'needs to be revised')
#
#     def set_transition_divisions(self):
#         rlen = len(self.rlist)
#         glen = len(self.glist)
#         blen = len(self.blist)
#         rdivs = [self.ncolors // len(self.rlist)] * rlen
#         gdivs = [self.ncolors // len(self.glist)] * glen
#         bdivs = [self.ncolors // len(self.blist)] * blen
#         rgbdivs = {'r': rdivs, 'g': gdivs, 'b': bdivs}
#         # Adding or subtracting from sections for divisibility
#         for k in self.keylist:
#             if sum(rgbdivs[k]) != self.ncolors:
#                 diff = self.ncolors - sum(rgbdivs[k])
#                 if diff < 0:
#                     f = -1
#                 elif diff > 0:
#                     f = 1
#                 for l in range(diff):
#                     rgbdivs[k][-l] += f
#
#         self.rgbdivs = rgbdivs
#
#     def set_fades(self):
#         rgbdivs = self.rgbdivs
#         # rblank, gblank, bblank = self.split_lists()
#         rfades, gfades, bfades = [], [], []
#         rdivs, gdivs, bdivs = rgbdivs['r'], rgbdivs['g'], rgbdivs['b'],
#         decimal = self.roundto
#
#         for i in range(len(self.rlist)):
#             first, last = self.rlist[i][0], self.rlist[i][1]
#             section = np.linspace(first, last, rdivs[i])
#             section = np.around(section, decimal)
#             section = np.array(section)
#             section = section.tolist()
#             rfades = rfades + section
#
#         for i in range(len(self.glist)):
#             first, last = self.glist[i][0], self.glist[i][1]
#             section = np.linspace(first, last, gdivs[i])
#             section = np.around(section, decimal)
#             section = np.array(section)
#             section = section.tolist()
#             gfades = gfades + section
#
#         for i in range(len(self.blist)):
#             first, last = self.blist[i][0], self.blist[i][1]
#             section = np.linspace(first, last, bdivs[i])
#             section = np.around(section, decimal)
#             section = np.array(section)
#             section = section.tolist()
#             bfades = bfades + section
#
#         return rfades, gfades, bfades
#
#     def join_colors(self):
#         rgb = [(c[0], c[1], c[2]) for c in
#                zip(self.rvals, self.gvals, self.bvals)]
#         return rgb
#
#     def scale0to1(self, rgblist):
#         newlist = []
#         roundto = self.roundto
#         for col in rgblist:
#             scaledval = [round(i / 255, roundto) for i in col]
#
#             newlist.append(scaledval)
#         return newlist
#
#     def hexconvert(self):
#         for i in self.rgb0to1:
#             hexcol = pltcolors(i)
#             self.hex.append(hexcol)
#
#
# class ColorScheme:
#
#     def __init__(self, ncolors=50, redlist=[[0, 255]], greenlist=[[0, 255]], bluelist=[[0, 255]]):
#         self.ncolors = ncolors
#         self.keylist = ['r', 'g', 'b']
#         self.cols = {'r': redlist, 'g': greenlist, 'b': bluelist}
#         self.check_inputs()
#         self.rlist = self.cols['r']
#         self.glist = self.cols['g']
#         self.blist = self.cols['b']
#         self.rgbdivs = {}
#         self.roundto = 3
#         self.set_transition_divisions()
#         self.rvals, self.gvals, self.bvals = self.set_fades()
#         self.rgbcolors = self.join_colors()
#         self.rgb0to1 = self.scale0to1(self.rgbcolors)
#         self.hex = []
#         self.hexconvert()
#
#     def check_inputs(self):
#         for k in self.keylist:
#             current = self.cols[k]
#             if isinstance(current, int):
#                 print('Inputs must be in the form of a list of lists')
#             if not isinstance(current[0], list):
#                 self.cols[k] = [self.cols[k]]
#             for l in range(len(current)):
#                 if len(current[l]) == 1:
#                     self.cols[k][l] = [current[l][0], current[l][0]]
#                     print('Revising short list', self.cols[k][l])
#                 if len(current[l]) > 2:
#                     print('Color value lists can have no more than 2 numbers')
#                     print(current[l], 'needs to be revised')
#
#     def set_transition_divisions(self):
#         rlen = len(self.rlist)
#         glen = len(self.glist)
#         blen = len(self.blist)
#         rdivs = [self.ncolors // len(self.rlist)] * rlen
#         gdivs = [self.ncolors // len(self.glist)] * glen
#         bdivs = [self.ncolors // len(self.blist)] * blen
#         rgbdivs = {'r': rdivs, 'g': gdivs, 'b': bdivs}
#         # Adding or subtracting from sections for divisibility
#         for k in self.keylist:
#             if sum(rgbdivs[k]) != self.ncolors:
#                 diff = self.ncolors - sum(rgbdivs[k])
#                 if diff < 0:
#                     f = -1
#                 elif diff > 0:
#                     f = 1
#                 for l in range(diff):
#                     rgbdivs[k][-l] += f
#         self.rgbdivs = rgbdivs
#
#     def split_lists(self):
#         rblank, gblank, bblank = [], [], []
#         for k in self.keylist:
#             kcurrent = self.rgbdivs[k]
#             klen = len(self.rgbdivs[k])
#             for i in range(klen):
#                 # rval = self.rgbdivs['r']
#                 val = kcurrent[i]
#                 if k == 'r':
#                     rblank.append([0] * val)
#                 elif k == 'g':
#                     gblank.append([0] * val)
#                 elif k == 'b':
#                     bblank.append([0] * val)
#         return rblank, gblank, bblank
#
#     def set_fades(self):
#         rgbdivs = self.rgbdivs
#         # rblank, gblank, bblank = self.split_lists()
#         rfades, gfades, bfades = [], [], []
#         rdivs, gdivs, bdivs = rgbdivs['r'], rgbdivs['g'], rgbdivs['b'],
#         decimal = self.roundto
#
#         for i in range(len(self.rlist)):
#             first, last = self.rlist[i][0], self.rlist[i][1]
#             section = np.linspace(first, last, rdivs[i])
#             section = np.around(section, decimal)
#             section = np.array(section)
#             section = section.tolist()
#             rfades = rfades + section
#
#         for i in range(len(self.glist)):
#             first, last = self.glist[i][0], self.glist[i][1]
#             section = np.linspace(first, last, gdivs[i])
#             section = np.around(section, decimal)
#             section = np.array(section)
#             section = section.tolist()
#             gfades = gfades + section
#
#         for i in range(len(self.blist)):
#             first, last = self.blist[i][0], self.blist[i][1]
#             section = np.linspace(first, last, bdivs[i])
#             section = np.around(section, decimal)
#             section = np.array(section)
#             section = section.tolist()
#             bfades = bfades + section
#
#         return rfades, gfades, bfades
#
#     def join_colors(self):
#         rgb = [(c[0], c[1], c[2]) for c in
#                zip(self.rvals, self.gvals, self.bvals)]
#         return rgb
#
#     def scale0to1(self, rgblist):
#         newlist = []
#         roundto = self.roundto
#         for col in rgblist:
#             scaledval = [round(i / 255, roundto) for i in col]
#
#             newlist.append(scaledval)
#         return newlist
#
#     def hexconvert(self):
#         for i in self.rgb0to1:
#             hexcol = pltcolors(i)
#             self.hex.append(hexcol)


class ColorScheme:

    def __init__(self, colordict, ncolors=50, symetrical=False):
        self.redlist = colordict['r']
        self.greenlist = colordict['g']
        self.bluelist = colordict['b']
        self.ncolors = ncolors
        if symetrical is True:
            self.ncolors = ncolors // 2
        self.keylist = ['r', 'g', 'b']
        # self.cols = {'r': redlist, 'g': greenlist, 'b': bluelist}
        self.colors = colordict
        self.check_inputs()
        self.rlist = self.colors['r']
        self.glist = self.colors['g']
        self.blist = self.colors['b']
        self.rgbdivs = {}
        self.roundto = 3
        self.set_transition_divisions()
        self.rvals, self.gvals, self.bvals = self.set_fades()
        self.rgbcolors = self.join_colors()
        self.rgb0to1 = self.scale0to1(self.rgbcolors)
        self.hex = []
        self.hexconvert()
        if symetrical is True:
            self.rgb0to1 = self.rgb0to1 + self.rgb0to1[::-1]
            self.rgb0to1 = self.rgb0to1 + self.rgb0to1[::-1]
            self.hex = self.hex + self.hex[::-1]

    def check_inputs(self):
        for k in self.keylist:
            valuelist = self.colors[k]
            if not isinstance(valuelist, list):
                print('Inputs must be in the form of a list')
            if not isinstance(valuelist[0], list):
                if len(valuelist) <= 2:
                    self.colors[k] = [self.colors[k]]
                elif len(valuelist) > 2:
                    valuelist = self.convert_format(valuelist, k)
            if isinstance(valuelist[0], list):
                for l in range(len(valuelist)):
                    if len(valuelist[l]) == 1:
                        self.colors[k][l] = [valuelist[l][0], valuelist[l][0]]
                        print('Revising short list', self.colors[k][l])
                    if len(valuelist[l]) > 2:
                        print('Color value lists can have no more than '
                              '2 numbers')
                        print(valuelist[l], 'needs to be revised')

    def convert_format(self, valuelist, key):
        # input [0, 100, 255]
        convertedlist = []
        for i in range(len(valuelist)):
            if i < len(valuelist) - 1:
                pair = [valuelist[i], valuelist[i + 1]]
                convertedlist.append(pair)
        # print(convertedlist)
        self.colors[key] = convertedlist
        return convertedlist

    def set_transition_divisions(self):
        rlen = len(self.rlist)
        glen = len(self.glist)
        blen = len(self.blist)
        rdivs = [self.ncolors // len(self.rlist)] * rlen
        gdivs = [self.ncolors // len(self.glist)] * glen
        bdivs = [self.ncolors // len(self.blist)] * blen
        rgbdivs = {'r': rdivs, 'g': gdivs, 'b': bdivs}
        # print(rgbdivs)
        # Adding or subtracting from sections for divisibility
        for k in self.keylist:
            if sum(rgbdivs[k]) != self.ncolors:
                diff = self.ncolors - sum(rgbdivs[k])
                # print(diff)
                if diff < 0:
                    f = -1
                elif diff > 0:
                    f = 1
                for l in range(diff):
                    rgbdivs[k][-l] += f

        self.rgbdivs = rgbdivs

    def set_fades(self):
        rgbdivs = self.rgbdivs
        # rblank, gblank, bblank = self.split_lists()
        rfades, gfades, bfades = [], [], []
        rdivs, gdivs, bdivs = rgbdivs['r'], rgbdivs['g'], rgbdivs['b'],
        decimal = self.roundto

        for i in range(len(self.rlist)):
            first, last = self.rlist[i][0], self.rlist[i][1]
            section = np.linspace(first, last, rdivs[i])
            section = np.around(section, decimal)
            section = np.array(section)
            section = section.tolist()
            rfades = rfades + section

        for i in range(len(self.glist)):
            first, last = self.glist[i][0], self.glist[i][1]
            section = np.linspace(first, last, gdivs[i])
            section = np.around(section, decimal)
            section = np.array(section)
            section = section.tolist()
            gfades = gfades + section

        for i in range(len(self.blist)):
            first, last = self.blist[i][0], self.blist[i][1]
            section = np.linspace(first, last, bdivs[i])
            section = np.around(section, decimal)
            section = np.array(section)
            section = section.tolist()
            bfades = bfades + section

        return rfades, gfades, bfades

    def join_colors(self):
        rgb = [(c[0], c[1], c[2]) for c in
               zip(self.rvals, self.gvals, self.bvals)]
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


class ColorCycle:
    def __init__(self, colorlist):
        self._color = colorlist
        # print(self._color, self._turt)

    def colorsetter(self, ind):
        length = len(self._color)
        modind = ind % length
        # print('colorsetter called')
        # print(modind)
        # print(self._color[modind])
        turtle.color(self._color[modind])
        return self._color[modind]


class Turn:

    def __init__(self, turt, angle, curve=None, curvesize=5):
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
        self._input = inputxy
        self.xlist = [i[0] for i in inputxy]
        self.ylist = [i[1] for i in inputxy]
        self.list = [c for c in zip(self.xlist, self.ylist)]
        self.cartesianlist = [self.pol2cart(pc[0], pc[1]) for pc in self.list]
        self.polarlist = [self.cart2pol(xy[0], xy[1]) for xy in self.list]

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
        distlist, xydistlist = Analyze(pointlist).distance()
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
                dist = Analyze((coord, point)).distance()[0][0]
                print(dist, distfilter)
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
        print(1)
        preblist = [[round(probnums[-(i + 1)], 2)] * (i + 1) for i in range(probnum)]
        print(2)
        problist = list(itertools.chain.from_iterable(preblist))[::-1]
        print(3)
        print(len(problist))
        problist = ([-n for n in problist][::-1] + problist)[::2]
        print(len(problist))
        # print(min(problist), max(problist), '\n', problist)

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

    def generatepointcloud(self, density, spread):
        pointlist = []
        probnum = spread * 5

        # print(min(problist), max(problist), '\n', problist)

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
        print(len(problist))
        problist = ([-n for n in problist][::-1] + problist)[::2]
        print(len(problist))
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
    def __init__(self, funclist):
        self.funclist = funclist
        self.coordlist = []

    def crosspoint(self, xtolerance=0.2, ytolerance=10):
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
        print(len(ypoints))
        print(len(points))
        self.coordlist = points
        avg = self.avgcoord(points)
        return points, avg

    def center(self):
        avgs = []
        for i in self.funclist:
            avgs.append(self.avgcoord(i))
        center = self.avgcoord(avgs)
        print(center)
        return center

    def center2(self):
        fulllist = []
        for i in self.funclist:
            fulllist = fulllist + i
        center = self.avgcoord(fulllist)
        return center

    def distance(self):
        coords = self.funclist
        distlist = []
        xydistlist = []
        for i in range(len(coords)):
            i2 = ((i + 1) % len(coords))
            xdist = round(coords[i][0] - coords[i2][0], 6)
            ydist = round(coords[i][1] - coords[i2][1], 6)
            dist = round(sqrt((xdist ** 2) + (ydist ** 2)), 2)
            distlist.append(dist)
            xydistlist.append((xdist, ydist))
        return distlist, xydistlist

    @staticmethod
    def avgcoord(coords):
        xs, ys = [xy[0] for xy in coords], [xy[1] for xy in coords]
        if len(xs) and len(ys) > 0:
            xavg, yavg = sum(xs)/len(xs), sum(ys)/len(ys)
            avgcoord = (xavg, yavg)
            return avgcoord
        else:
            return None


class RadialAngularPattern:

    def __init__(self, size, angles=[[125, 1, 3]], turncycle=0, jank=None,
                 colors=color_list, pensize=1, position=[0, 0]):
        self._colors = colors
        self._pensize = pensize
        self._size = size
        turtle.pensize(self._pensize)
        self._angles = angles
        self._turncycle = turncycle
        self._jank = jank
        self._position = position
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
            # angles = [angles]
        for i in range(len(self._angles)):
            self.create_turns(i)
        # self._turnlist = [self.turn1, self.turn2, self.turn3, self.turn4]
        self._nTurns = [t for t in self._turnlist if t is not None]
        self._position = (-(size / 2), (size / 2))
        self._startpos = turtle.pos()
        print(self._startpos)
        self.goto()
        self.center()

    def create_turns(self, n):
        tparams = self._angles[n]
        # print(self._angles, tparams)
        if n == 0:
            self.turn1 = Turn(turtle.Turtle(), *tparams)
            self._turnlist.append(self.turn1)
        if n == 1:
            self.turn2 = Turn(turtle.Turtle(), *tparams)
            self._turnlist.append(self.turn2)
        if n == 2:
            self.turn3 = Turn(turtle.Turtle(), *tparams)
            self._turnlist.append(self.turn3)
        if n == 3:
            self.turn4 = Turn(turtle.Turtle(), *tparams)
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

        for k in range(100):

            ColorCycle(self._colorlist).colorsetter(k)

            self.anglego(0)
            if self.checkplace():
                turtle.goto(self._startpos)
                break

    def twoangle(self):

        for k in range(100):

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

        for k in range(100):

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

        for k in range(100):

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
            print('checkplace returned True')
            return True
        else:
            return False

    def goto(self):
        turtle.penup()
        turtle.goto(self._startpos)
        # if self.penup is False:
        turtle.pendown()

    def center(self):
        turtle.penup()
        turtle.goto(- (self._size / 2), 0)
        self._startpos = turtle.pos()
        turtle.pendown()

    def capturepath(self, penup=True):
        if penup is True:
            turtle.penup()
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
        return turtle.get_poly()


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


class DrawPath:
    def __init__(self, coordlist, pensize, colors, colordist=0, lines=True, dots=False, dotsize=1):
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
            funclist.append(sin1.list)
            sin1.draw()
        checkptz, point = Analyze(funclist).crosspoint()
        turtle.color('white')
        turtle.penup()
        turtle.goto(point)
        turtle.pendown()
        turtle.dot(5)
        # for lst in funclist:
        #     for c in lst:
        #         turtle.goto(c)
        #         turtle.pendown()
        #         turtle.dot(3)
        #         turtle.penup()
        # for i in checkptz:
        #     turtle.goto(i)
        #     turtle.pendown()
        #     turtle.dot(2)
        #     turtle.penup()

    @staticmethod
    def sin_avg_point_rotation(strands=20, xshift=10, yshift=0, rotate=1, rotaterate=1, totalrotation=None,
                               colors=color_list, wavelength=50, amplitude=100, wlshift=0,
                   ampshift=0, length=20, cosine=False, position=[0, 0], showpoint=False, draworig=False):
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
        center = Analyze(funclist).center()
        # center2 = Analyzer(funclist).center2()

        """Part 2"""
        xpos, ypos = position[0], position[1]
        rotationfactor = 0.1
        if totalrotation is None:
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
            # if totalrotation > 0:
            Transform(sin1).rotate(totalrotation, center)
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

        return rotation_point

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


speed = 100000
turtle.setup(1900, 1200)  # Laptop screen
turtle.speed(10)
# turtle.setup(3840, 2200)     # 4K screen
turtle.bgcolor('black')
# turtle.bgpic('turtle_background_image1-02-01.png')
turtle.tracer(speed, 0)
turtle.hideturtle()


"""
SETTINGS:

LVL2.sin_spiral(50, 1, rotate=2, rotaterate=20, cosine=True)
LVL2.layered_flowers(layers=250, npetals=6, innerdepth=1, sizefactor=0.5, rotate=1, colors=rainbow1)

"""

"""
COLOR SCHEMES:

rainbow = {'r': [[255, 255], [255, 255], [255, 220], [220,  75], [75,    3], [3,     3], [3,    30], [30,  125], [125, 220], [220, 255]],
           'g': [[0,   150], [150, 255], [255, 255], [255, 255], [255, 255], [255, 145], [145,   3], [3,     3], [3,     3], [3,     0]],
           'b': [[0,     0], [0,     0], [0,     3], [3,     3], [3,   240], [240, 255], [255, 255], [255, 255], [255, 255], [255,   0]]}

bluepinkpurp = {'r': [[0, 255], [255, 150], [150, 200]], 
                'g': [[145, 0]], 
                'b': [[255, 150], [150, 255]]}
peacock = {'r': [[0, 255], [255, 150], [150, 200]],
           'g': [[0, 145], [145, 150], [150, 0]],
           'b': [[255, 150], [150, 255]]}
"""


reds = [[0, 255], [255, 150], [150, 200]]
greens = [[145, 0]]
blues = [[255, 150], [150, 255]]
bluepinkpurp = {'r': [[0, 255], [255, 150], [150, 200]], 'g': [[145, 0]], 'b': [[255, 150], [150, 255]]}

#
#             r          o           y          yg           g           bg          b           b         p
rainbow = {'r': [[255, 255], [255, 255], [255, 220], [220,  75], [75,    3], [3,     3], [3,    30], [30,  125], [125, 220], [220, 255]],
           'g': [[0,   150], [150, 255], [255, 255], [255, 255], [255, 255], [255, 145], [145,   3], [3,     3], [3,     3], [3,     0]],
           'b': [[0,     0], [0,     0], [0,     3], [3,     3], [3,   240], [240, 255], [255, 255], [255, 255], [255, 255], [255,   0]]}
try2 = {'r': [0, 255, 200, 255],
        'g': [0, 50, 50, 0],
        'b': [255, 200, 255, 100]}

rainbow1 = ColorScheme(rainbow, 100)
newcol1 = ColorScheme(try2, 260, symetrical=True)

# point = LVL2.sin_avg_point_rotation(60, xshift=0, wavelength=35, wlshift=0.2, ampshift=0, rotate=1, length=40, colors=newcol1, showpoint=True, cosine=True)
# ra1 = RadialAngularPattern(1000, [30, 20, 45], colors=rainbow1)

# path1 = RadialAngularPattern(500).draw()
path1 = RadialAngularPattern(500).capturepath()
# DrawPath(path1, 1, rainbow1, lines=True) #, dots=True)
path1 = Transform(path1).addpoints(100, 200)
path2 = LVL2.
cloud1 = Transform(path2).generatepointcloud(10, 10, exp=6)
DrawPath(cloud1, 1, 'white', lines=False, dots=True, dotsize=0.1)
DrawPath(path1, 2, rainbow1, colordist=50, lines=True) #, dots=True)

# LVL2.layered_flowers(layers=80, npetals=6, innerdepth=1, sizefactor=2, pensize=4, rotate=1, colors=rainbow1)
# LVL2.sin_spiral(30, xshift=10, wlshift=1, ampshift=0, rotate=0, colors=color_list)
# LVL2.sin_spiral(50, 2, rotate=1, cosine=True, colors=purple_to_black)
# LVL2.layered_flowers(50, rotate=1, color=black_to_purple)
# LVL2.antenas()


turtle.exitonclick()
