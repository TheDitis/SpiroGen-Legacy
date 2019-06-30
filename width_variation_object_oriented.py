import turtle

def color_gen_old():
    color_list = [
        'red', 'crimson', 'orangered', 'darkorange', 'orange', 'gold',
        'yellow', 'greenyellow', 'lawngreen', 'limegreen', 'springgreen',
        'mediumspringgreen', 'aquamarine', 'turquoise', 'aqua',
        'deepskyblue', 'dodgerblue', 'mediumslateblue', 'mediumpurple',
        'blueviolet', 'darkviolet', 'purple', 'mediumvioletred'
    ]


class Turt:
    _name_mapping = {
        'size': 'pensize',
    }
    def __init__(self, color):
        self.color = color

    def update(self, **kwargs):
        for name, value in kwargs.items():
            if name in self._name_mapping:
                name = self._name_mapping[name]
            func = getattr(turt, name)
            func(value)

    @property
    def color(self):
        return self.color

    @color.setter
    def color(self, color):
        if not isinstance(color, str):
            raise ValueError('color must be string')
        self.color = color
        self.turtle.color(self.color)


turt = Turt('blue')
# # property
# print(self.color)
# turt.color = 'red'
# # update
# turt.update(color='red', size=5)


class ColorGen:
    _defaults = {
        'colors': [
            'red', 'crimson', 'orangered', 'darkorange', 'orange', 'gold',
            'yellow', 'greenyellow', 'lawngreen', 'limegreen', 'springgreen',
            'mediumspringgreen', 'aquamarine', 'turquoise', 'aqua',
            'deepskyblue', 'dodgerblue', 'mediumslateblue', 'mediumpurple',
            'blueviolet', 'darkviolet', 'purple', 'mediumvioletred'
        ],
        'size': range(5, 20)
    }

    def __init__(self, repeats=5, list_=None):
        """
        Generator for color name strings for turtle.
        Args:
            repeats (int): number of times to return the same color
                before moving to the next
            color_list (list): list of colors to iterate through
        """
        # counter
        self.n = 0
        self.repeats = repeats
        if list_:
            self.list = color_list
        else:
            self.color_list = self._defaults['color_list']

    def __next__(self):
        # floor division to stay on each i value for number of `repeats`
        i = self.n // self.repeats
        # start over once index would normally go out of range
        i = i % len(self.color_list)
        # increment counter
        self.n += 1
        return self.color_list[i]

    def __iter__(self):
        return self


class RandomColorGen(ColorGen):
    def __next__(self):
        pass


class Artist:
    def __init__(self, bgcolor, speed, RoC, lines):
        turtle.bgcolor(bgcolor)
        turtle.speed(speed)
        turtle.penup()
        turtle.goto(-RoC / 2, RoC / 2)
        turtle.color(next(self.color_gen_old))


class SquareArtist(Artist):
    def __init__(self, bgcolor, speed, mode, RoC, lines='straight'):
        super().__init__(bgcolor, speed)
        self.mode = mode

    def loop(self):
        pass


class SpiralSquareArtist(SquareArtist):

    def __init__(self, bgcolor, speed, mode, RoC, lines='straight'):
        super(Artist).__init__(bgcolor, speed)
        self.mode = mode

joe = Turt()
joe.