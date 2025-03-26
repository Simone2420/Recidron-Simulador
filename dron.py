
from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
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
