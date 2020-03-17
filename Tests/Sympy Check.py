import numpy as np
import sympy as sp
# import turtle
import matplotlib.pyplot as plt
import svgwrite

# turtle.hideturtle()
# turtle.speed(10)
# turtle.tracer(10, 0)

color_list = [
    'red', 'crimson', 'orangered', 'darkorange', 'orange', 'gold',
    'yellow', 'greenyellow', 'lawngreen', 'limegreen', 'springgreen',
    'mediumspringgreen', 'aquamarine', 'turquoise', 'aqua',
    'deepskyblue', 'dodgerblue', 'mediumslateblue', 'mediumpurple',
    'blueviolet', 'darkviolet', 'purple', 'mediumvioletred'
]


dimensions = (1000, 1000)
xmid = dimensions[0] / 2
ymid = dimensions[1] / 2

dwg = svgwrite.Drawing('test2.1.svg', size=dimensions)


def sin(amplitude=1, phase=0, wavelength=1, start=0, end=2*np.pi, ):
    # a, pi, x, h, b, k = sp.symbols('a pi x h b k')
    xrange = np.linspace(start, end, int((max(end, start) - min(end, start))) * 25)
    a = amplitude
    pi = np.pi
    h = phase
    b = wavelength
    for x in xrange:
        func2 = a * np.sin((x - h) / b)
        # expr1 = (x - h) / b
        # expr1 = expr1.subs(x, i)
        # print(expr1)
        # print(expr1.evalf())
        # function = a * np.sin(float(expr1.evalf()))  # + k
        res = func2
        print(res)


def sin2(x, amplitude=1, phase=0, wavelength=1, yshift=0, start=0, end=2*np.pi, ):
    a = amplitude
    pi = np.pi
    h = phase
    b = wavelength
    k = yshift
    # for x in xrange:
    func2 = a * np.sin((x - h) / b) + k
    return func2


def draw(func, dist, **kwargs):
    xrange = np.linspace(0, dist*np.pi, int((dist / 4)*np.pi) * 10)
    y = np.vectorize(func)(xrange, **kwargs)
    xrange = xrange + xmid
    y = y + ymid
    points = zip(xrange, y)
    print(points)
    prevp = (xrange[0], y[0])
    for p in points:
        dwg.add(dwg.line(prevp, p, stroke='red', fill='blue'))
        # dwg.add(dwg.line(prevp, p, stroke=svgwrite.rgb(10, 10, 16, '%')))
        # turtle.pendown()
        # turtle.goto(p)
        # turtle.penup()
        prevp = p


def draw2(func, dist, **kwargs):
    xrange = np.linspace(0, dist*np.pi, int((dist / 4)*np.pi) * 10)
    y = np.vectorize(func)(xrange, **kwargs)
    xrange = xrange + xmid
    y = y + ymid
    points = zip(xrange, y)
    prevp = coord2string((xrange[0], y[0]))
    d_str = 'M' + prevp + ' '
    for p in points:
        p = coord2string(p)
        prevp = coord2string(prevp)
        print(prevp)
        d_str += 'L' + p + ' '
        prevp = p
    dwg.add(dwg.path(d=d_str,
                     stroke="purple",
                     fill="none",
                     stroke_width=1)
            )


def coord2string(coord):
    coord = str(coord)[1:-1]
    coord = coord.replace(' ', '')
    return coord

"""
    'M470,240 C490,290, 550,290, 570,240'
"""
    # print(function.evalf())
    # return (a + ramp * theta) * np.sin(wl * theta + x_shift) + y_shift

draw2(sin2, 128, amplitude=60, wavelength=16)
# sin(10, 0, 1)

dwg.save()

# turtle.exitonclick()
