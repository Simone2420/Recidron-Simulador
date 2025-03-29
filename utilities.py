from ursina import *
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

    # Eliminar la entity después de la animación
    destroy(entity, delay=1)
def verificate_collition_with_trash_can(trash_can,player):
    for entity in scene.entities:
        # Verificar si la entidad tiene un collider y no es la caneca
        if entity.collider and (entity != trash_can and entity != player):
            # Verificar colisión con la caneca
            if entity.intersects(trash_can).hit:
                # Verificar que la colisión sea por la parte superior
                if entity.y > trash_can.y:  # Solo colisiones por arriba
                    print("¡Un objeto ha sido reciclado!")
                    desintegrate(entity)  # Animar la desintegración