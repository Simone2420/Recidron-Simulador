from ursina import *
from recolectable import *
from dron import *
import random
import random

def random_excluding(low, high, exclude_low, exclude_high):
    while True:
        num = random.randint(low, high)
        if not (exclude_low <= num <= exclude_high):
            return num
class EspecificTrash:
    def __init__(self, model=None, collider=None, color=None):
        self.model = model
        self.collider = collider
        self.color = color
    

class FlyWeightBottle(EspecificTrash):
    def __init__(self, model=None, collider=None, color=None):
        super().__init__(model, collider, color)

class FlyWeightCan(EspecificTrash):
    def __init__(self, model=None, collider=None, color=None):
        super().__init__(model, collider, color)

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

class TrashGenerator:
    @classmethod
    def generate_trash(cls,player,num_colectibles=20):
        try:
            trash_types = ["botlle","can"]
            for _ in range(num_colectibles):
                trash_selected = random.choice(trash_types)
                x,z = random_excluding(-22,22,-5,5),random_excluding(-22,22,-5,5)
                if trash_selected == "botlle":
                    flyweightbottle = BottlesFactory.get_bottle(
                        model='./modelos_graficos/yogurt.obj',
                        collider='box',
                        color=color.random_color()
                    )
                    scale = (.2, .2, .2)
                    collectible = Recolectable(
                        player,
                        position= (x,0,z),
                        model= flyweightbottle.model,
                        collider=flyweightbottle.collider,
                        parent=scene,
                        color=flyweightbottle.color,
                        origin_y=-.5,
                        scale=scale
                        )
                elif trash_selected == "can":
                    flyweightcan = CansFactory.get_can(
                        model='./modelos_graficos/can7.obj',
                        collider='box',
                        color=color.red
                    )
                    scale = 3
                    collectible = Recolectable(
                        player,
                        position= (x,.02,z),
                        model= flyweightcan.model,
                        texture="./modelos_graficos/metal2.png",
                        color=flyweightcan.color,
                        collider=flyweightcan.collider,
                        parent=scene,
                        origin_y=-.5,
                        scale=scale
                        )
        except Exception as e:
            print(f"Error {e}")
            
