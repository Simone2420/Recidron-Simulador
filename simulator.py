from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import random
from flyweight import *
from recolectable import *
from dron import *
from utilities import *
simulation = Ursina()

cube = Entity(
    model="cube",
    position = (40,1,-40),
    collider = "box",
    scale=1
)
class TrashCan(Entity):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)

player = Dron()
player.position = (0, 10, 0)

ground = Entity(
    model='plane',
    texture='grass',
    collider='box',
    scale=(100, 1, 100)
)
invisible_ground = Entity(
    model="cube",
    collider="box",
    position=(0,.1,0),
    scale=(100,.1,100),
    visible=False
)
recolectable_bottle = Recolectable(
    player,
    parent=scene,
    model='./assets/can7.obj',
    origin_y=-.5,
    texture="./assets/metal2.png",
    color=color.red,
    position=(3, .9, 3),
    collider='box',
    scale=3

)

recolectable_bottle_2 = Recolectable(
    player,
    parent=scene,
    model='./assets/yogurt.obj',
    color=color.red,
    origin_y=-.5,
    position=(10, 0, 4),
    collider='box',
    scale=(.2, .2, .2)
)
colectibles = TrashGenerator.generate_trash(player)
trashcan = TrashCan(
    model="./assets/trash_can.obj",
    texture="./assets/trash_can_texture.png",
    collider="box",
    double_sided=True,
    position=(0,3,0),
    scale=5
)
sky = Sky()

    
def update():
    apply_gravity()
    verificate_collition_with_trash_can(trashcan,player)
simulation.run()

