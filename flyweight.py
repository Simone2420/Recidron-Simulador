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
class FlyWeightCorrugatedBottle(EspecificTrash):
    def __init__(self, model=None, collider=None, color=None):
        super().__init__(model, collider, color)
class FlyWeightCan(EspecificTrash):
    def __init__(self, model=None, collider=None, color=None):
        super().__init__(model, collider, color)
class FlyweightPlasticCup(EspecificTrash):
    def __init__(self, model=None, collider=None, color=None):
        super().__init__(model, collider, color)
class FlyweighCorrugatedPaper(EspecificTrash):
    def __init__(self, model=None, collider=None, color=None):
        super().__init__(model, collider, color) 
class StyrofoamTray(EspecificTrash):
    def __init__(self, model=None, collider=None, color=None):
        super().__init__(model, collider, color)
class StyrofoamCan(EspecificTrash):
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
class CorrugatedBottlesFactory:
    _corrugated_bottles = {}
    @classmethod
    def get_bottle(cls, model, collider, color):
        key = (model, collider, color)
        if key not in cls._corrugated_bottles:
            cls._corrugated_bottles[key] = FlyWeightCorrugatedBottle(model, collider, color)
        return cls._corrugated_bottles[key]
class CansFactory:
    _cans = {}
    @classmethod
    def get_can(cls, model, collider, color):
        key = (model, collider, color)
        if key not in cls._cans:
            cls._cans[key] = FlyWeightCan(model, collider, color)
        return cls._cans[key]
class PlasticCupFactory:
    _plastic_glass = {}
    @classmethod
    def get_plastic_glass(cls, model, collider, color):
        key = (model, collider, color)
        if key not in cls._plastic_glass:
            cls._plastic_glass[key] = FlyweightPlasticCup(model, collider, color)
        return cls._plastic_glass[key]
class CorrugatedPaperFactory:
    _corrugated_paper = {}
    @classmethod
    def get_corrugated_paper(cls, model, collider, color):
        key = (model, collider, color)
        if key not in cls._corrugated_paper:
            cls._corrugated_paper[key] = FlyweighCorrugatedPaper(model, collider, color)
        return cls._corrugated_paper[key]
class StyrofoamTrayFactory:
    _styrofoam_tray = {}
    @classmethod
    def get_styrofoam_tray(cls, model, collider, color):
        key = (model, collider, color)
        if key not in cls._styrofoam_tray:
            cls._styrofoam_tray[key] = StyrofoamTray(model, collider, color)
        return cls._styrofoam_tray[key]
class StyrofoamCanFactory:
    _styrofoam_can = {}
    @classmethod
    def get_styrofoam_can(cls, model, collider, color):
        key = (model, collider, color)
        if key not in cls._styrofoam_can:
            cls._styrofoam_can[key] = StyrofoamCan(model, collider, color)
        return cls._styrofoam_can[key]
class TrashGenerator:
    @classmethod
    def generate_trash(cls,player,num_colectibles=70):
        try:
            trash_types = [
                "bottle",
                "corrugated_bottle",
                "plastic_cup",
                "can",
                "corrugated_paper",
                "styrofoam_tray",
                "styrofoam_can"
                ]
            for _ in range(num_colectibles):
                trash_selected = random.choice(trash_types)
                x,z = random_excluding(-48,48,-3,3),random_excluding(-48,48,-3,3)
                fixed_y = 0
                scale: float
                random_weight = random.randint(1,4)
                match random_weight:
                    case 1:
                        scale = 1
                        fixed_y = .02
                    case 2:
                        scale = 1.2
                        fixed_y =.03
                    case 3:
                        scale = 1.5
                        fixed_y =.05
                    case 4:
                        scale = 1.7
                        fixed_y =.06
                if trash_selected == "bottle":
                    flyweightbottle = BottlesFactory.get_bottle(
                        model='./assets/water_bottle.obj',
                        collider='box',
                        color=color.random_color()
                    )
                    collectible = Recolectable(
                        player,
                        position= (x,fixed_y,z),
                        model= flyweightbottle.model,
                        collider=flyweightbottle.collider,
                        color=flyweightbottle.color,
                        object_type=trash_selected,
                        weight=random_weight,
                        parent=scene,
                        scale=scale*0.6
                        )
                elif trash_selected == "corrugated_bottle":
                    corrugated_flyweightbottle = CorrugatedBottlesFactory.get_bottle(
                        model='./assets/corrugated_bottle.obj',
                        collider='box',
                        color=color.random_color()
                    )
                    collectible = Recolectable(
                        player,
                        position= (x,fixed_y,z),
                        model= corrugated_flyweightbottle.model,
                        collider=corrugated_flyweightbottle.collider,
                        color=corrugated_flyweightbottle.color,
                        object_type=trash_selected,
                        weight=random_weight,
                        parent=scene,
                        scale=scale*0.6
                    )
                elif trash_selected == "plastic_cup":
                    flyweightplasticcup = PlasticCupFactory.get_plastic_glass(
                        model='./assets/plastic_cup.obj',
                        collider='box',
                        color=color.random_color()
                    )
                    collectible = Recolectable(
                        player,
                        position= (x,fixed_y+1.5,z),
                        model= flyweightplasticcup.model,
                        collider=flyweightplasticcup.collider,
                        color=flyweightplasticcup.color,
                        texture="./assets/material_cup.png",
                        object_type=trash_selected,
                        weight=random_weight,
                        parent=scene,
                        scale=scale*3
                    )
                elif trash_selected == "can":
                    flyweightcan = CansFactory.get_can(
                        model='./assets/can7.obj',
                        collider='box',
                        color=color.red
                    )
                    collectible = Recolectable(
                        player,
                        position= (x,fixed_y+2,z),
                        model= flyweightcan.model,
                        texture="./assets/metal2.png",
                        color=flyweightcan.color,
                        collider=flyweightcan.collider,
                        object_type=trash_selected,
                        weight=random_weight,
                        parent=scene,
                        scale=scale*2.5
                        )
                elif trash_selected == "corrugated_paper":
                    flyweightcorrugatedpaper = CorrugatedPaperFactory.get_corrugated_paper(
                        model='./assets/corrugated_paper.obj',
                        collider='box',
                        color=color.random_color()
                    )
                    collectible = Recolectable(
                        player, 
                        position= (x,fixed_y,z),
                        model= flyweightcorrugatedpaper.model,
                        collider=flyweightcorrugatedpaper.collider,
                        color=flyweightcorrugatedpaper.color,
                        object_type=trash_selected,
                        weight=random_weight,
                        parent=scene,
                        scale=scale*.5
                    )
                elif trash_selected == "styrofoam_tray":
                    flyweightstyrofoamtray = StyrofoamTrayFactory.get_styrofoam_tray(
                        model='./assets/styrofoam_tray.obj',
                        collider='box',
                        color=color.random_color()
                    )
                    collectible = Recolectable(
                        player,
                        position= (x,fixed_y+.5,z),
                        model= flyweightstyrofoamtray.model,
                        collider=flyweightstyrofoamtray.collider,
                        color=flyweightstyrofoamtray.color,
                        texture="./assets/styrofoam.png",
                        object_type=trash_selected,
                        weight=random_weight,
                        parent=scene,
                        scale=scale*2.5
                    )
                elif trash_selected == "styrofoam_can":
                    flyweightstyrofoamcan = StyrofoamCanFactory.get_styrofoam_can(
                        model='./assets/styrofoam_can.obj',
                        collider='box',
                        color=color.random_color()
                    )
                    collectible = Recolectable(
                        player,
                        position= (x,fixed_y+1,z),
                        model= flyweightstyrofoamcan.model,
                        collider=flyweightstyrofoamcan.collider,
                        color=flyweightstyrofoamcan.color,
                        object_type=trash_selected,
                        weight=random_weight,
                        parent=scene,
                        scale=scale*2
                    )
        except Exception as e:
            print(f"Error {e}")
            
