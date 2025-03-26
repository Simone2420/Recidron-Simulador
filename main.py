from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import random
from flyweight import *
from recolectable import *
from dron import *
# Inicializar la ventana
simulation = Ursina()


class TrashCan(Entity):
    pass


# Crear el jugador
player = Dron()
player.position = (0, 10, 0)
# Crear el suelo
ground = Entity(
    model='plane',
    texture='grass',
    collider='box',
    scale=(50, 1, 50)
)


# Crear recolectables
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

sky = Sky()
def apply_gravity():
    for entity in scene.entities:
        if hasattr(entity, 'apply_gravity') and entity.apply_gravity:
            # Aplicar gravedad solo si el objeto no está colisionando con el suelo
            if not entity.intersects().hit:
                entity.velocity_y -= 9.81 * time.dt  # Simular aceleración gravitacional
                entity.y += entity.velocity_y * time.dt  # Actualizar posición vertical
            else:
                # Si colisiona con el suelo, detener la caída
                entity.velocity_y = 0
                entity.apply_gravity = False

# Ejecutar el juego
def update():
    apply_gravity()

simulation.run()