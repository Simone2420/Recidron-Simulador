from ursina import *
from dron import *
from data_base import *
class Recolectable(Button):
    def __init__(self, player, object_type= "Not specified", object_material= "Not specified",**kwargs):
        super().__init__(**kwargs)
        self.disabled = False
        self.player = player
        self.on_click = self.get_recolectable
        self.weight = 1
        self.object_type = object_type
        self.object_material = object_material
        self.date_registered = None
        self.assigned_zone = 0
        self.initial_position = list(self.position)
        self.position_printed = False
        self.determine_asigned_zone()
    def determine_asigned_zone(self):
        if self.initial_position[0] < 0 and self.initial_position[2] > 0:
            self.assigned_zone = 1
        elif self.initial_position[0] > 0 and self.initial_position[2] > 0:
            self.assigned_zone = 2
        elif self.initial_position[0] < 0 and self.initial_position[2] < 0:
            self.assigned_zone = 3
        elif self.initial_position[0] > 0 and self.initial_position[2] < 0:
            self.assigned_zone = 4
    def determine_material(self): pass
    def reclycle(self):
        pass
    def register_data_to_database(self):
        pass
    def get_recolectable(self):
        if self.player.gun is None:
            self.parent = camera
            self.position = Vec3(0, 0, 3)
            self.player.gun = self
            