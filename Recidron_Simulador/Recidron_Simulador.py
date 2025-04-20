"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import reflex as rx
from Recidron_Simulador.utilities import *
from data_base import *
from rxconfig import config
from utilities import *
import random
db = DataBaseConnector()
data = db.get_all_records()
print(data)
objects_types = db.get_objects_types()
print(objects_types)
total_weigth_of_object_type= calculate_concentration_by_object_type(random.choice(objects_types),db)
print(total_weigth_of_object_type)
class State(rx.State):
    """The app state."""

    ...

def try_pie_chart() -> rx.Component:
    print(generate_random_color_hex())
    return rx.recharts.pie_chart(
        rx.recharts.pie(
            data=[
                {"name": "Group A", "value": 400, "fill": generate_random_color_hex()},
                {"name": "Group B", "value": 300, "fill": "#4ECDC4"},
                {"name": "Group C", "value": 300, "fill": "#45B7D1"},
                {"name": "Group D", "value": 200, "fill": "#96CEB4"},
            ],
            name_key="name",
            data_key="value",
            label=True,
        ),
        width="100%",
        height=300,
    )
def pie_chart_2() -> rx.Component:
    return rx.recharts.pie_chart(
        rx.recharts.pie(
            data=[
                {"name": "Group A", "value": 400, "fill": "#FF6B6B"},
                {"name": "Group B", "value": 300, "fill": "#4ECDC4"}, 
            ],
            name_key="name",
            data_key="value",
            label=True, 
        ),
        width="100%",
        height=300
    )
def index() -> rx.Component:
    # Welcome Page (Index)
    return rx.container(
        rx.color_mode.button(position="top-right"),
        rx.vstack(
            rx.heading("Estadistical report from Recidron", size="9"),
            spacing="5",
            justify="center",
            min_height="85vh",
        ),
        rx.spacer(),
        rx.vstack(
            try_pie_chart(),
            pie_chart_2(),
            rx.link(
                rx.button("Recidron Simulation", color_scheme="green", variant="solid"),
                href="https://reflex.dev/docs/getting-started/introduction/",
                button=True,
                is_external=True,
            )
        ),
        rx.logo(),
        width="100%",
        padding="20px"
    )


app = rx.App()
app.add_page(index)
