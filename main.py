from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import random

# Inicializar la ventana
simulation = Ursina()

class Dron(FirstPersonController):
    def __init__(self, **kwargs):
        super().__init__()
        self.vertical_speed = 5  # Velocidad de movimiento vertical
        self.collider = 'box'
        self.gravity = 0.005
        self.gun = None

    def update(self):
        super().update()
        self.direction = Vec3(
            self.forward * (held_keys['w'] - held_keys['s'])
            + self.right * (held_keys['d'] - held_keys['a'])
            + self.up * (held_keys['up arrow'] - held_keys['down arrow'])  # Movimiento vertical
        ).normalized()
        self.position += self.direction * self.speed * time.dt

    def input(self, key):
        super().input(key)
        if key == 'q' and hasattr(self, 'gun') and self.gun:
            # Realizar un raycast para detectar entidades frente al jugador
            hit_info = raycast(
                origin=self.position + (0, 1, 0),  # Ajustar origen para evitar el suelo
                direction=self.forward,
                distance=4,  # Distancia máxima de detección
                ignore=(self,)  # Ignorar al propio jugador
            )
            if hit_info.hit:
                # Colocar el objeto encima de la entidad detectada
                target = hit_info.entity
                self.gun.parent = scene
                self.gun.position = target.position + Vec3(0, 8, 0)

                # Aplicar gravedad a la botella
                self.gun.velocity_y = 0  # Inicializar la velocidad vertical
                self.gun.apply_gravity = True  # Indicador para aplicar gravedad
            else:
                # Soltar el objeto normalmente
                self.gun.parent = scene
                self.gun.position = camera.world_position + camera.forward * 4

                # Aplicar gravedad al objeto soltado
                self.gun.velocity_y = 0  # Inicializar la velocidad vertical
                self.gun.apply_gravity = True  # Indicador para aplicar gravedad

            self.gun = None

class TrashCan(Entity):
    pass

class Recolectable(Button):
    global player
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
    def get_recolectable(self):
        if player.gun is None:
            self.parent = camera
            self.position = Vec3(0, 0, 3)
            player.gun = self
            

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

# Crear una plataforma
platform = Entity(
    model='cube',
    color=color.orange,
    collider='box',
    position=(0, 1, 5),
    scale=(5, .1, 5)
)

# Crear un obstáculo
obstacle = Entity(
    model='./modelos_graficos/yogurt.obj',
    texture="brick",
    color=color.blue,
    collider='box',
    position=(0, 5, 5),
    scale=0.3
)

# Crear recolectables
recolectable_bottle = Recolectable(
    parent=scene,
    model='./modelos_graficos/yogurt.obj',
    color=color.blue,
    origin_y=-.5,
    position=(3, 0, 3),
    collider='box',
    scale=(.2, .2, .2)
    
)

recolectable_bottle_2 = Recolectable(
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

# Crear un cielo
sky = Sky()

# Función para aplicar gravedad a los objetos soltados
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