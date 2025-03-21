from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from abc import ABC,abstractmethod
# Inicializar la ventana
app = Ursina()

class Dron(FirstPersonController):
    def __init__(self, **kwargs):
        super().__init__()
        self.vertical_speed = 5  # Velocidad de movimiento vertical
        self.collider = 'box'
        self.gravity = 0.005
    def update(self):
        super().update()
        self.direction = Vec3(
            self.forward * (held_keys['w'] - held_keys['s'])
            + self.right * (held_keys['d'] - held_keys['a'])
            + self.up * (held_keys['up arrow'] - held_keys['down arrow'])  # Movimiento vertical
        ).normalized()

        # Aplicar velocidad al movimiento
        self.position += self.direction * self.speed * time.dt

class GeneralEntity:pass
class EspecificTrash(Entity):
    def __init__(self,model,collider,color,**kwargs):
        self.model = model
        self.collider = collider
        self.color = color
class Bottle(EspecificTrash):
    def __init__(self,model,collider,color,**kwargs):
        super().__init__(model,collider,color,**kwargs)
class TrashBag(EspecificTrash): 
    def __init__(self,model,collider,color,**kwargs):
        super().__init__(model,collider,color,**kwargs)
class BottlesFactory:
    pass

# Configurar el jugador (primera persona)
player = Dron()  # Usamos la clase Dron personalizada
player.position = (0, 10, 0)  # Posición inicial (x, y, z)

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
    position=(0, 2, 5),
    scale=(5, 1, 5)
)

# Crear un obstáculo
obstacle = Entity(
    model='./modelos_graficos/yogurt.obj',
    color=color.red,
    collider='box',
    position=(0, 5, 5),
    scale=0.3
)

# Crear un cielo
sky = Sky()

# Función para detectar colisiones
def update():
    # Si el jugador toca el obstáculo, reiniciar posición
    if player.intersects(obstacle).hit:
        print("¡Chocaste con el obstáculo!")
        player.position = (0, 10, 0)  # Reiniciar posición del jugador

# Ejecutar el juego
app.run()