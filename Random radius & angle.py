import random
from math import *

# radius of the circle
circle_r = 10
# center of the circle (x, y)
circle_x = 5
circle_y = 7
# random angle
alpha = 2 * pi * random.random()
# random radius
r = circle_r * sqrt(random.random())
# calculating coordinates
x = r * cos(alpha) + circle_x
y = r * sin(alpha) + circle_y

print("Random point", (x, y))