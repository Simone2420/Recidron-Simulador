from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

# Inicializar la ventana
app = Ursina()

# Configurar el jugador (primera persona)
player = FirstPersonController()
player.collider = 'box'
player.gravity = 0.001
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
    model='sphere',
    color=color.red,
    collider='sphere',
    position=(0, 5, 5),
    scale=2
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