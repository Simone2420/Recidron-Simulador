from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

# Inicializar la ventana
simulation = Ursina()

class Dron(FirstPersonController):
    def __init__(self, **kwargs):
        super().__init__()
        self.vertical_speed = 5  # Velocidad de movimiento vertical
        self.collider = 'box'
        self.gravity = 0.005
        # self.scale = self.scale + Vec3(1, 1, 1)

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
                distance=10,  # Distancia máxima de detección
                ignore=(self,)  # Ignorar al propio jugador
            )
            if hit_info.hit:
                # Colocar el objeto encima de la entidad detectada
                target = hit_info.entity
                self.gun.parent = scene
                self.gun.position = target.position + (0, target.scale_y // 2 + self.gun.scale_y // 2, 0)
            else:
                # Soltar el objeto normalmente
                self.gun.parent = scene
                self.gun.position = self.position + self.forward
                # Agregar gravedad al objeto soltado
                self.gun.velocity_y = 0  # Inicializar la velocidad vertical
                self.gun.apply_gravity = True  # Indicador para aplicar gravedad
            self.gun = None

class GeneralEntity:
    pass
class EspecificTrash(Entity):
    def __init__(self, model, collider, color, **kwargs):
        self.model = model
        self.collider = collider
        self.color = color


class Bottle(EspecificTrash):
    def __init__(self, model, collider, color, **kwargs):
        super().__init__(model, collider, color, **kwargs)


class TrashBag(EspecificTrash):
    def __init__(self, model, collider, color, **kwargs):
        super().__init__(model, collider, color, **kwargs)


class BottlesFactory:
    pass


class TrashCan(Entity):
    pass


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


class Recolectable(Button):
    def get_recolectable(self):
        self.parent = camera
        self.position = Vec3(.3, 0, .3)
        player.gun = self


recolectable_bottle = Recolectable(
    parent=scene,
    model='./modelos_graficos/yogurt.obj',
    color=color.blue,
    origin_y=-.5,
    position=(3, 0, 3),
    collider='box',
    scale=(.2, .2, .2)
)
recolectable_bottle.on_click = recolectable_bottle.get_recolectable

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