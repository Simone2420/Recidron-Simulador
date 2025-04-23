from ursina import *
from recolectable import Recolectable
from data_base import DataBaseConnector
import datetime

def apply_gravity():
    for entity in scene.entities:
        if hasattr(entity, 'apply_gravity') and entity.apply_gravity:
            if not entity.intersects().hit:
                entity.velocity_y -= 9.81 * time.dt  
                entity.y += entity.velocity_y * time.dt  
            else:
                entity.velocity_y = 0
                entity.apply_gravity = False
def desintegrate(entity):
    """
    Función para animar la desintegración de una entity.
    """
    # Animar la opacidad hasta que sea invisible
    entity.animate('color', color.rgba(255, 255, 255, 0), duration=1)
    if isinstance(entity, Recolectable) and not entity.position_printed:
        print("¡Un objeto ha sido reciclado!")
        reclycle(entity)
        entity.position_printed = True
    destroy(entity, delay=1)
def verificate_collition_with_trash_can(trash_can,player):
    for entity in scene.entities:
        # Verificar si la entidad tiene un collider y no es la caneca
        if entity.collider and (entity != trash_can and entity != player):
            # Verificar colisión con la caneca
            if entity.intersects(trash_can).hit:
                # Verificar que la colisión sea por la parte superior
                if entity.y > trash_can.y:  # Solo colisiones por arriba
                    desintegrate(entity)  # Animar la desintegración
def reclycle(entity):
    print(f"The asigned zone for the object is {entity.assigned_zone}")
    print(f"The material of the object is {entity.object_material}")
    print(f"The type of the object is {entity.object_type}")
    print(f"The weight of the object is {entity.weight}")
    register_data_to_database(entity)
def register_data_to_database(entity):
    with DataBaseConnector() as data_base_register:
        date_register = datetime.datetime.now()
        object_type = entity.object_type
        object_material = entity.object_material
        weight = entity.weight
        assigned_zone = entity.assigned_zone
        data_base_register.register_object(date_register,object_type,object_material,weight,assigned_zone)
def end_simulation(simulation):
    try:
        simulation.close()
    except:
        print("Simulation already closed")
    finally:
        print("Simulation closed")
        raise KeyboardInterrupt