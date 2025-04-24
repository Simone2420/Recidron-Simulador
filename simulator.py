from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import random
from simulator import *

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

def input(key):
    if key == "escape":
        end_simulation(simulation)
def update():
    apply_gravity()
    verificate_collition_with_trash_can(trashcan,player)
simulation.run()

