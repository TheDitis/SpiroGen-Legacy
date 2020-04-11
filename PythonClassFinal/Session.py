class Session:
    def __init__(self, id, name, pattern_id, colorscheme_id):
        self._id = id
        self._name = name
        self._pattern_id = pattern_id
        self._colorscheme_id = colorscheme_id
        self._pattern = self.load("pattern", pattern_id)
        self._colorscheme = self.load("color", self._colorscheme_id)

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
    def pattern_id(self):
        return self._pattern_id

    @pattern_id.setter
    def pattern_id(self, id):
        self._pattern_id = id
        self.load('pattern', id=id)

    @property
    def colorscheme_id(self):
        return self._colorscheme_id

    @colorscheme_id.setter
    def colorscheme_id(self, id):
        self._colorscheme_id = id
        self.load('color', id=id)

    def save(self):
        # here would be the save method for the sql database
        pass

    @classmethod
    def load(cls, type="session", name=None, id=None):
        # here would be the loading method to get a session from the database
        if name is None and id is None:
            print("you must enter either a name or an id")
        elif name is not None and id is not None:
            print("You must use either a name or an id, not both")
        elif name is not None:
            if type == 'session':
                # set session attributes
                pass
            elif type == 'pattern':
                # get pattern from db and set self._pattern to it
                pass
            elif type == 'color':
                # get colorscheme id from the db and set pattern to it
                pass
            # find id of item with that given name and load it
            return "Object"
        elif id is not None:
            # load the item with the given id, if it exists
            return "Object"
