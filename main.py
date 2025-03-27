from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import random
from flyweight import *
from recolectable import *
from dron import *

simulation = Ursina()
def singleton(cls):
    instances = {}
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return get_instance

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

recolectable_bottle = Recolectable(
    player,
    parent=scene,
    model='./modelos_graficos/can.obj',
    origin_y=-.5,
    position=(3, .9, 3),
    collider='box',
    scale=(.13, .13, .13)

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
recolectable_bottle.on_click = recolectable_bottle.get_recolectable
recolectable_bottle_2.on_click = recolectable_bottle_2.get_recolectable
colectibles = TrashGenerator.generate_trash(player)
trashcan = TrashCan(
    model="./modelos_graficos/trash_can.obj",
    texture="./modelos_graficos/trash_can_texture.png",
    collider="mesh",
    position=(0,2.5,0),
    scale=5
)
sky = Sky()
def apply_gravity():
    for entity in scene.entities:
        if hasattr(entity, 'apply_gravity') and entity.apply_gravity:
            if not entity.intersects().hit:
                entity.velocity_y -= 9.81 * time.dt  
                entity.y += entity.velocity_y * time.dt  
            else:
                
                entity.velocity_y = 0
                entity.apply_gravity = False

def update():
    apply_gravity()

simulation.run()

