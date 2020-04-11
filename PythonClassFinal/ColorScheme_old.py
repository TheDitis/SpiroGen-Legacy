from matplotlib.colors import rgb2hex as pltcolors
import numpy as np


class ColorScheme:

    def __init__(self, colordict, ncolors=50, symetrical=False):
        self._ncolors = ncolors
        self._symetrical = symetrical
        if symetrical is True:
            self._ncolors = ncolors // 2
        self._keylist = ['r', 'g', 'b']
        self._colors = colordict
        self.check_inputs()
        self._rlist = self._colors['r']
        self._glist = self._colors['g']
        self._blist = self._colors['b']
        self._rgbdivs = {}
        self._roundto = 3
        self.set_transition_divisions()
        self._fades = self.set_fades()
        self._rgbcolors = self.join_colors()
        self._rgb0to1 = self.scale0to1(self._rgbcolors)
        self._hex = []
        self.hexconvert()
        if symetrical is True:
            self._rgb0to1 = self._rgb0to1 + self._rgb0to1[::-1]
            self._rgb0to1 = self._rgb0to1 + self._rgb0to1[::-1]
            self._hex = self._hex + self._hex[::-1]

    def __repr__(self):
        hexlist = self._hex
        return hexlist

    def __str__(self):
        return str(self._colors)

    def __getitem__(self, index):
        return self._hex[index]

    def __setitem__(self, index, value):
        self._hex[index] = value

    def __len__(self):
        return len(self._hex)

    def setup(self):
        self.check_inputs()
        self._rlist = self._colors['r']
        self._glist = self._colors['g']
        self._blist = self._colors['b']
        self._rgbdivs = {}
        self._roundto = 3
        self.set_transition_divisions()
        self._fades = self.set_fades()
        self._rgbcolors = self.join_colors()
        self._rgb0to1 = self.scale0to1(self._rgbcolors)
        self._hex = []
        self.hexconvert()
        if self._symetrical is True:
            self._rgb0to1 = self._rgb0to1 + self._rgb0to1[::-1]
            self._rgb0to1 = self._rgb0to1 + self._rgb0to1[::-1]
            self._hex = self._hex + self._hex[::-1]

    def check_inputs(self):
        for k in self._keylist:
            color = self._colors[k]
            if not isinstance(color, list):
                print('Inputs must be in the form of a list')
            if isinstance(color[0], list):
                for l in range(len(color)):
                    if len(color[l]) == 1:
                        self._colors[k][l] = [color[l][0], color[l][0]]
                        print('Revising short list', self._colors[k][l])
                    if len(color[l]) > 2:
                        print('Color value lists can have no more than '
                              '2 numbers')
                        print(color[l], 'needs to be revised')
                        raise ValueError
                self.convert2list()

    def convert2list(self):
        for k in self._keylist:
            newlist = []
            color = self._colors[k]
            for i in range(len(color)):
                if i < len(color) - 1:
                    newlist.append(color[i][0])
                elif i == len(color) - 1:
                    newlist.append(color[i][0])
                    newlist.append(color[i][1])
            self._colors[k] = newlist

    def set_transition_divisions(self):
        rlen = len(self._rlist) - 1
        glen = len(self._glist) - 1
        blen = len(self._blist) - 1
        rdivs = [self._ncolors // rlen] * rlen
        gdivs = [self._ncolors // glen] * glen
        bdivs = [self._ncolors // blen] * blen
        rgbdivs = {'r': rdivs, 'g': gdivs, 'b': bdivs}
        # Adding or subtracting from sections for divisibility
        for k in self._keylist:
            if sum(rgbdivs[k]) != self._ncolors:
                diff = self._ncolors - sum(rgbdivs[k])
                if diff < 0:
                    f = -1
                elif diff > 0:
                    f = 1
                for l in range(diff):
                    rgbdivs[k][-(l + 1)] += f
        self._rgbdivs = rgbdivs

    def set_fades(self):
        rgbdivs = self._rgbdivs
        fades = {'r': [], 'g': [], 'b': []}
        # rdivs, gdivs, bdivs = rgbdivs['r'], rgbdivs['g'], rgbdivs['b'],
        decimal = self._roundto
        for k in self._keylist:
            clist = self._colors[k]
            for i in range(len(clist) - 1):
                first, last = clist[i], clist[i + 1]
                section = np.linspace(first, last, rgbdivs[k][i])
                section = (np.around(section, decimal)).tolist()
                fades[k] = fades[k] + section
        return fades

    def join_colors(self):
        rgb = [(c[0], c[1], c[2]) for c in
               zip(self._fades['r'], self._fades['g'], self._fades['b'])]
        return rgb

    def scale0to1(self, rgblist):
        newlist = []
        roundto = self._roundto
        for col in rgblist:
            scaledval = [round(i / 255, roundto) for i in col]

            newlist.append(scaledval)
        return newlist

    def hexconvert(self):
        for i in self._rgb0to1:
            hexcol = pltcolors(i)
            self._hex.append(hexcol)

    def shiftlightness(self, delta):
        newcolors = {'r': [], 'g': [], 'b': []}
        for k in self._keylist:
            for val in self._colors[k]:
                newval = val + delta
                if newval > 255:
                    newval = 255
                elif newval < 0:
                    newval = 0
                newcolors[k].append(newval)
        self._colors = newcolors
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
        for k in self._keylist:
            colorvals = self._colors[k]
            scope = (len(colorvals) * goto) // 100
            sublist = np.linspace(amt, 0, scope)
            if True:
                for ind in range(len(colorvals)):
                    ind2 = ind
                    if direction == 1:
                        ind = -(ind + 1)
                    if ind2 < len(sublist):
                        self._colors[k][ind] += sublist[ind2]
                        if self._colors[k][ind] < 0:
                            self._colors[k][ind] = 0
                        elif self._colors[k][ind] > 255:
                            self._colors[k][ind] = 255
        self.hexconvert()
        self.setup()