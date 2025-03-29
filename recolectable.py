from ursina import *
from dron import *

class Recolectable(Button):
    def __init__(self,player,**kwargs):
        super().__init__(**kwargs)
        self.disabled = False
        self.player = player
        self.on_click = self.get_recolectable
        self.weight = 1
        self.type = "No especified"
    def get_recolectable(self):
        if self.player.gun is None:
            self.parent = camera
            self.position = Vec3(0, 0, 3)
            self.player.gun = self
            