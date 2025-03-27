from ursina import *
from dron import *
from recolectable import *
from utilities import *
app = Ursina()

# Variable para rastrear si la botella fue reciclada
reciclado = False
dron = Dron()
dron.position = (0, 10, 0)
# Crear la botella
botella = Recolectable(
    dron,
    parent=scene,
    model='cube',  # Cambia esto por el modelo de tu botella
    texture='white_cube',
    scale=0.5,
    position=(0, 1, 0),
    collider='box'  # Habilitar colisiones
)
botella2 = Recolectable(
    dron,
    parent=scene,
    model='cube',  # Cambia esto por el modelo de tu botella
    texture='white_cube',
    scale=0.5,
    position=(0, 1, 1),
    collider='box'  # Habilitar colisiones
)
botella3 = Recolectable(
    dron,
    parent=scene,
    model='cube',  # Cambia esto por el modelo de tu botella
    texture='white_cube',
    scale=0.5,
    position=(0, 1, 2),
    collider='box'  # Habilitar colisiones
)
ground = Entity(
    model='plane',
    texture='grass',
    collider='box',
    scale=(50, 1, 50)
)

# Crear la caneca de basura
caneca = Entity(
    model='cube',  # Cambia esto por el modelo de tu caneca
    color=color.green,
    scale=(2, 3, 2),
    position=(0, 0, 5),
    collider='box'  # Habilitar colisiones
)

def update():
    """
    Función principal de actualización que verifica colisiones.
    """
    global botella, caneca, reciclado
    apply_gravity()
    # Verificar si la botella colisiona con la caneca
    verificate_collition_with_trash_can(caneca,dron)
# Ejecutar la aplicación
app.run()