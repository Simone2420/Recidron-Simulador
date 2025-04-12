from ursina import *
from dron import *
from data_base import *
class Recolectable(Button):
    def __init__(self, player, object_type= "Not specified", **kwargs):
        super().__init__(**kwargs)
        self.disabled = False
        self.player = player
        self.on_click = self.get_recolectable
        self.weight = 1
        self.object_type = object_type
        self.date_registered = None
        self.assigned_zone = 1
        self.initial_position = list(self.position)
        self.position_printed = False
    def determine_asigned_zone(self):
        # Implementa la lógica para determinar la zona asignada
        # Puedes utilizar la posición del objeto para asignarlo a una zona específica
        # Por ejemplo, puedes asignar una zona basada en la posición en el eje X
        pass
    def reclycle(self):
        pass
    def register_data_to_database(self):
        pass
    def get_recolectable(self):
        if self.player.gun is None:
            self.parent = camera
            self.position = Vec3(0, 0, 3)
            self.player.gun = self
            