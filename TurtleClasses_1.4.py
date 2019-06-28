import turtle
from matplotlib.colors import rgb2hex as pltcolors

color_list2 = [
        'red', 'crimson', 'orangered', 'darkorange', 'orange', 'gold',
        'yellow', 'greenyellow', 'lawngreen', 'limegreen', 'springgreen',
        'mediumspringgreen', 'aquamarine', 'turquoise', 'aqua',
        'deepskyblue', 'dodgerblue', 'mediumslateblue', 'mediumpurple',
        'blueviolet', 'darkviolet', 'purple', 'mediumvioletred'
    ]


def color_gen():
    pass


class ColorScheme:

    def __init__(self, listlen, Rrange=[0, 0], Grange=[0, 0], Brange=[0, 0], Rfactor=0):        #Takes length of list and range to be spanned over that length for each color
        self._length = listlen                                  #
        self._RedR = Rrange
        self._GreenR = Grange
        self._BlueR = Brange
        factor = (1 / 255)
        self.rgbcolors = []
        self.rgbcolorscale = []
        self.hexcolors = []
        R1, R2 = self._RedR[0], self._RedR[1]
        G1, G2 = self._GreenR[0], self._GreenR[1]
        B1, B2 = self._BlueR[0], self._BlueR[1]
        Rmin, Rmax = min(R1, R2), max(R1, R2)
        Gmin, Gmax = min(G1, G2), max(G1, G2)
        Bmin, Bmax = min(B1, B2), max(B1, B2)
        Rintrvl = (Rmax - Rmin) / listlen
        Gintrvl = (Gmax - Gmin) / listlen
        Bintrvl = (Bmax - Bmin) / listlen
        if R1 > R2:
            Rintrvl = -Rintrvl
        if G1 > G2:
            Gintrvl = -Gintrvl
        if B1 > B2:
            Bintrvl = -Bintrvl
        NewR, NewG, NewB = R1, G1, B1
        for i in range(listlen):
            rgb = [NewR, NewG, NewB]
            rgbfloats = [i * factor for i in rgb]
            rgb = [int(round(n)) for n in rgb]
            rgbfloats = [round(n, 2) for n in rgbfloats]
            NewR, NewG, NewB = NewR + Rintrvl, NewG + Gintrvl, NewB + Bintrvl
            self.rgbcolors.append(rgb)
            self.rgbcolorscale.append(rgbfloats)
        self.hexconvert()


    def hexconvert(self):
        for i in self.rgbcolorscale:
            hexcol = pltcolors(i)
            self.hexcolors.append(hexcol)


class Turt:

    def __init__(self, color='green', size=1, speed=10, xy=[0, 0], heading=0):
        self._color = color
        self._size = size
        self._speed = speed
        self._heading = heading
        self.turtle = turtle.Turtle()
        if isinstance(self._color, str):
            self.turtle.color(self._color)
        self.turtle.pensize(self._size)
        self.turtle.speed(self._speed)
        self.turtle.penup()
        self.turtle.goto(xy[0], xy[1])
        self.turtle.seth(self._heading)
        self.turtle.pendown()
        self._xy = self.turtle.pos()

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
        print("color setter method called")
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


class Pattern:

    def __init__(self, dest_turt, repeats, colist):
        self._turt = dest_turt
        self._reps = repeats
        self._colors = colist

    def forward(self, dist):
        self._turt.turtle.forward(dist)

    def circle(self, radius, extent=None, steps=None):
        self._turt.turtle.circle(radius, extent=extent, steps=steps)

    def rainbowcircles(self, repeats=50, radius=5, pos=[0, 0]):
        self._turt.position = pos
        for i in range(repeats):
            self._turt.turtle.color(self._turt.color_gen(i))
            self.circle(radius * (i + 1))

    def rainbowcircles_centered(self, repeats, radius, factor=1, pos=None, heading=0): # FIX
        pi = 3.14159
        if pos != None:
            self._turt.turtle.penup()
            self._turt.turtle.goto(pos)
            self._turt.turtle.pendown()
        for i in range(repeats):
            rad = radius * (i + 1)
            pos2 = self._turt.turtle.pos()
            print(pos2)
            self._turt.turtle.penup()
            if heading == 0:
                self._turt.turtle.goto(pos2[0], pos2[1] - radius)
            elif heading == 180:
                self._turt.turtle.goto(pos2[0], pos2[1] + radius)
            elif heading == 270:
                self._turt.turtle.goto(pos2[0] - radius, pos2[1])
            elif heading == 90:
                self._turt.turtle.goto(pos2[0] + radius, pos2[1])
            # print('New Pos:' + str(self._turt.turtle.pos()))
            self._turt.heading = heading
            self._turt.turtle.pendown()
            self._turt.turtle.color(self._turt.color_gen(i))
            self.circle(rad)

    def rainbowcircles_outfromcenter(self, repeats, radius, RoC, pos=[0, 0]):
        for i in range(repeats):
            # pos = self._turt.turtle.pos()
            self._turt.turtle.penup()
            self._turt.turtle.goto(pos[0], pos[1] - ((radius / RoC) * (i + 1)))
            self._turt.heading = 0
            self._turt.turtle.pendown()
            self._turt.turtle.color(self._turt.color_gen(i)(i))
            self.circle(radius * (i + 1))

    def cardioid_thing(self, repeats, radius, position=[0, 0]):
        self._turt.position = position
        for i in range(4):
            self._turt.heading = 90 * i
            self.rainbowcircles(repeats, radius)

    def cardioid_flower(self, repeats, radius, position=[0, 0]):
        self._turt.position = position
        for i in range(4):
            self._turt.heading = 90 * i
            self.rainbowcircles(repeats, radius)
        self._turt.position = position
        for i in range(4):
            self._turt.heading = (90 * i) - 45
            self.rainbowcircles(repeats, radius)

    def hypercardioid_thing(self, repeats, radius, position=[0, 0]):
        self._turt.position = position
        for i in range(2):
            self._turt.heading = 180 * i
            self.rainbowcircles(repeats, radius)

    def record_thing(self, repnum=6, circnum=50, radius=5):
        for i in range(repnum):
            self._turt.position = [(-repnum / 2) + i, 0]
            self.rainbowcircles_centered(circnum, radius)

    def many_circles(self, repeats=50, radius=5):
        xint = repeats * radius
        yint = 750
        xdiv = 2000 / (radius * repeats)
        xlist = [-1000 + (i * (radius * repeats)) for i in range(int(xdiv) + 1)]
        yrange_ = int((2*yint) / xint)
        print(len(xlist) + 1)
        for j in xlist:
            self.rainbowcircles_centered(repeats, radius, pos=[j, yint])
            for i in range(yrange_):
                self.rainbowcircles_centered(repeats, radius)


speed = 1000
turtle.bgcolor('black')
turtle.tracer(speed, 0)


'''
Create color schemes here

1st Argument is the number of colors you want to be in your scheme
2nd, 3rd, and 4th arguments are the start and end values for Red, Green, and Blue respectively
It will create a list of colors of specified length (n), and each generated color value will 
change from each color to the next by equal increments from the start value, to the end value 
of each of the RGB ranges     
'''                  # len      R        G         B
redtoblue = ColorScheme(51, [255, 0], [0, 200], [0, 255])
yellowgreenblue = ColorScheme(51, [255, 0], [255, 150], [0, 255])


# Here I create a turtle object named franklin, and give him a color scheme to follow
# argument 2 is pensize and argument 3 is speed, although this is currently overridden above by the tracer method
# to give him a color scheme, put the schemename.hexcolors as the first argument
franklin = Turt(color_list2, 1, 10)

# I then create a pattern instance, assigning the turtle we want to execute the patterns
# The second argument is the number of repeats
# The third argument is a color scheme, although this is currently overridden by the turtles scheme
patterngen1 = Pattern(franklin, 20, color_list2)


'''
Here are some patterns to try. 
1st argument for most patterns is number of circles per circle thing
2nd argument for most patterns is starting radius
'''
# patterngen1.rainbowcircles(100, 5)
# patterngen1.many_circles(50, 10)
patterngen1.cardioid_flower(50, 5)
# patterngen1.hypercardioid_thing(50, 5)
# patterngen1.record_thing()


turtle.exitonclick() # This makes it so that the window doesn't close itself once it's done drawing
