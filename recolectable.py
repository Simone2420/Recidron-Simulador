from ursina import *
from dron import *
from data_base import *
class Recolectable(Button):
    def __init__(self, player, object_type= "Not specified", object_material= "Not specified",weight=0,**kwargs):
        super().__init__(**kwargs)
        self.player = player
        self.on_click = self.get_recolectable
        self.weight = weight
        self.object_type = object_type
        self.object_material = object_material
        self.date_registered = None
        self.assigned_zone = 0
        self.initial_position = list(self.position)
        self.position_printed = False
        self.determine_asigned_zone()
        self.determine_material()
    def determine_asigned_zone(self):
        if self.initial_position[0] < 0 and self.initial_position[2] > 0:
            self.assigned_zone = 1
        elif self.initial_position[0] > 0 and self.initial_position[2] > 0:
            self.assigned_zone = 2
        elif self.initial_position[0] < 0 and self.initial_position[2] < 0:
            self.assigned_zone = 3
        elif self.initial_position[0] > 0 and self.initial_position[2] < 0:
            self.assigned_zone = 4
    def determine_material(self): 
        if self.object_type in ["bottle","corrugated_bottle","plastic_cup"]:
            self.object_material = "plastic"
        elif self.object_type == "can":
            self.object_material = "metal"
        elif self.object_type == "corrugated_paper":
            self.object_material = "paper"
        elif self.object_type in ["styrofoam_tray","styrofoam_can"]:
            self.object_material = "styrofoam"
    
    def get_recolectable(self):
        if self.player.gun is None:
            self.parent = camera
            self.position = (1, 0, 3)
            self.player.gun = self
            