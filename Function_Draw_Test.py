import turtle
from math import *
import numpy as np


def cart2pol(x, y):
    rho = np.sqrt(x**2 + y**2)
    phi = np.arctan2(y, x)
    return(rho, phi)


def pol2cart(rho, phi):
    x = rho * np.cos(phi)
    y = rho * np.sin(phi)
    return(x, y)


# xrange = list(range(-20, 21))
# ylist = [i**2 for i in xrange]
# coords =[xy for xy in zip(xrange, ylist)]
#
# polarcoords = [cart2pol(xy[0], xy[1]) for xy in coords]

petals = 6
#
# for xy in polarcoords:
#     turtle.goto(xy)


class FlowerPattern:
    def __init__(self, npetals, innerdepth=3, sizefactor=50):
        self._npetals = npetals
        self._innerdepth = innerdepth
        radianlist = np.linspace(0, 60, 6000)
        radiuslist = [(3 - (innerdepth * cos(petals * phi))) for phi in radianlist]
        self.polarlist = [c for c in zip(radiuslist, radianlist)]
        self.cartesianlist = [pol2cart(pc[0], pc[1]) for pc in self.polarlist]
        self.sizeuplist = self.sizeup(sizefactor)


    def sizeup(self, factor=50):
        sizeuplist = [(xy[0] * factor, xy[1] * factor) for xy in self.cartesianlist]
        return sizeuplist

    def draw(self, lst=None):
        if lst == None:
            lst = self.sizeuplist
        turtle.penup()
        turtle.goto(lst[0])
        turtle.pendown()
        for xy in lst:
            turtle.goto(xy)



# philist = np.linspace(0, 60, 6000)
# rholist = [(3 - (8 * cos(petals * phi))) for phi in philist]
# polcoordlist = [c for c in zip(rholist, philist)]
# pol2cartlist = [pol2cart(pc[0], pc[1]) for pc in polcoordlist]
# sizeup = [(xy[0]* 50, xy[1] * 50) for xy in pol2cartlist]


speed = 10
# turtle.penup()
# turtle.goto(sizeup[0])
# turtle.pendown()
turtle.tracer(speed, 1)
#
# for xy in sizeup:
#     turtle.goto(xy)
f8petals = FlowerPattern(8, 8)
f8petals.draw()


turtle.exitonclick()