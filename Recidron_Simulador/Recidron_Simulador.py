"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import reflex as rx
from Recidron_Simulador.utilities import *
from Recidron_Simulador.styles import *
from Recidron_Simulador.stucture import *
from data_base import *
from rxconfig import config
import random
with DataBaseConnector() as db:
    data = db.get_all_records()
    print(data)
    objects_types = db.get_objects_types()
    print(objects_types)
    total_weigth_of_object_type = calculate_concentration_by_object_type(random.choice(objects_types), db)
    print(total_weigth_of_object_type)
class State(rx.State):
    """The app state."""

    ...


def index() -> rx.Component:
    # Welcome Page (Index)
    return rx.container(
        rx.color_mode.button(position="top-right"),
        rx.hstack(
            rx.heading("Estadistical report from Recidron", size="9", width="100%"),
            spacing="5",
            justify="between",
            
        ),
        rx.spacer(),
        rx.spacer(),
        rx.vstack(
            object_type_pie_chart(),
            material_pie_chart(),
            zone_bar_chart(),
            
        ),
        width="100%",
        padding="10px"
    )


app = rx.App()
app.add_page(index)
