from spirogen import ColorScheme as CS


class ColorScheme:
    def __init__(self, id, name, ncolors, colors):
        self._id = id
        self._name = name
        self._ncolors = ncolors
        self._colors = colors

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id):
        self._id = id

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def ncolors(self):
        return self._ncolors

    @ncolors.setter
    def ncolors(self, number):
        self._ncolors = number

    @property
    def colors(self):
        return self._colors

    @colors.setter
    def colors(self, colors):
        self._colors = colors

    def get_colorscheme_obj(self):
        return CS(self._colors, self._ncolors)