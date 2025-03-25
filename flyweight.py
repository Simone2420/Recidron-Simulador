from ursina import *
class EspecificTrash:
    def __init__(self, model=None, collider=None, color=None):
        self.model = model
        self.collider = collider
        self.color = color
    

class FlyWeightBottle(EspecificTrash):
    def __init__(self, model=None, collider=None, color=None):
        super().__init__(self, model, collider, color)

class FlyWeightCan(EspecificTrash):
    def __init__(self, model=None, collider=None, color=None):
        super().__init__(self, model, collider, color)

class BottlesFactory:
    _bottles = {}
    @classmethod
    def get_bottle(cls, model, collider, color):
        key = (model, collider, color)
        if key not in cls._bottles:
            cls._bottles[key] = FlyWeightBottle(model, collider, color)
        return cls._bottles[key]
class CansFactory:
    _cans = {}
    @classmethod
    def get_can(cls, model, collider, color):
        key = (model, collider, color)
        if key not in cls._cans:
            cls._cans[key] = FlyWeightCan(model, collider, color)
        return cls._cans[key]


