from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

class Dron(FirstPersonController):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.vertical_speed = 5  # Velocidad de movimiento vertical
        self.collider = BoxCollider(self, center=Vec3(0, 0, 0), size=Vec3(1, 1, 1))
        self.gravity = 0.005
        self.gun = None
        self.traverse_target = scene
        self.ignore_list = [self, ]  # Ignorar al propio dron en las colisiones
        self.previous_position = self.position  # Guardar la posición anterior

    def update(self):
        super().update()

        # Guardar la posición anterior antes de moverse
        self.previous_position = self.position

        # Calcular la dirección de movimiento
        self.direction = Vec3(
            self.forward * (held_keys['w'] - held_keys['s'])
            + self.right * (held_keys['d'] - held_keys['a'])
            + self.up * (held_keys['up arrow'] - held_keys['down arrow'])  # Movimiento vertical
        ).normalized()

        MAX_SPEED = 2  # Velocidad máxima permitida
        move_amount = self.direction * min(self.speed, MAX_SPEED) * time.dt

        # Verificar colisiones antes de moverse
        feet_ray = raycast(self.position + Vec3(0, 0.5, 0), self.direction, traverse_target=self.traverse_target, ignore=self.ignore_list, distance=0.5)
        head_ray = raycast(self.position + Vec3(0, self.height - 0.1, 0), self.direction, traverse_target=self.traverse_target, ignore=self.ignore_list, distance=0.5)

        if not feet_ray.hit and not head_ray.hit:
            # Verificar colisiones laterales
            if raycast(self.position + Vec3(0, 1, 0), Vec3(1, 0, 0), distance=0.5, traverse_target=self.traverse_target, ignore=self.ignore_list).hit:
                move_amount[0] = min(move_amount[0], 0)
            if raycast(self.position + Vec3(0, 1, 0), Vec3(-1, 0, 0), distance=0.5, traverse_target=self.traverse_target, ignore=self.ignore_list).hit:
                move_amount[0] = max(move_amount[0], 0)
            if raycast(self.position + Vec3(0, 1, 0), Vec3(0, 0, 1), distance=0.5, traverse_target=self.traverse_target, ignore=self.ignore_list).hit:
                move_amount[2] = min(move_amount[2], 0)
            if raycast(self.position + Vec3(0, 1, 0), Vec3(0, 0, -1), distance=0.5, traverse_target=self.traverse_target, ignore=self.ignore_list).hit:
                move_amount[2] = max(move_amount[2], 0)
            self.position += move_amount
        else:
            self.position = self.previous_position

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