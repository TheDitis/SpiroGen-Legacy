from spirogen import RadialAngularPattern, FlowerPattern, \
    SpiralPattern, FlowerPattern2
from spirogen import LVL2


class Pattern:
    def __init__(self, id, name, type, params):
        self._id = id
        self._name = name
        self._type = type
        self._params = params

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
    def type(self):
        return self._type

    @type.setter
    def type(self, type):
        self._type = type

    @property
    def params(self):
        return self._params

    @params.setter
    def params(self, params):
        self._params = params

    def get_pattern_obj(self):
        if self._type == "RadialAngularPattern":
            return RadialAngularPattern(**self._params)
        elif self._type == "FlowerPattern":
            return FlowerPattern(**self._params)
        elif self._type == "SpiralPattern":
            return SpiralPattern(**self._params)
        elif self._type == "FlowerPattern2":
            return FlowerPattern2(**self._params)
        elif self._type == "LayeredFlowers":
            return LVL2.layered_flowers(**self._params)
        elif self._type == "SinSpiral":
            return LVL2.sin_spiral(**self._params)
        elif self._type == "IterativeRotation":
            return LVL2.iterative_rotation(**self._params)
