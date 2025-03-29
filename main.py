from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import random
from flyweight import *
from recolectable import *
from dron import *
from utilities import *
simulation = Ursina()
def singleton(cls):
    instances = {}
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return get_instance
cube = Entity(
    model="cube",
    position = (5,1,6),
    collider = "box",
    scale=1
)
class TrashCan(Entity):
    @singleton
    def __init__(self,**kwargs):
        super().__init__(**kwargs)

player = Dron()
player.position = (0, 10, 0)

ground = Entity(
    model='plane',
    texture='grass',
    collider='box',
    scale=(50, 1, 50)
)
invisible_ground = Entity(
    model="cube",
    collider="box",
    position=(0,.1,0),
    scale=(50,.1,50),
    visible=False
)
recolectable_bottle = Recolectable(
    player,
    parent=scene,
    model='./modelos_graficos/can7.obj',
    origin_y=-.5,
    texture="./modelos_graficos/metal2.png",
    color=color.red,
    position=(3, .9, 3),
    collider='box',
    scale=3

)

recolectable_bottle_2 = Recolectable(
    player,
    parent=scene,
    model='./modelos_graficos/yogurt.obj',
    color=color.red,
    origin_y=-.5,
    position=(10, 0, 4),
    collider='box',
    scale=(.2, .2, .2)
)
colectibles = TrashGenerator.generate_trash(player)
trashcan = TrashCan(
    model="./modelos_graficos/trash_can.obj",
    texture="./modelos_graficos/trash_can_texture.png",
    collider="box",
    double_sided=True,
    position=(0,3,0),
    scale=5
)
sky = Sky()

    
def update():
    previous_position = player.position
    apply_gravity()
    verificate_collition_with_trash_can(trashcan,player)
simulation.run()

