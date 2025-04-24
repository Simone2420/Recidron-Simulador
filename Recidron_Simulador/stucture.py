import reflex as rx
from data_base import *
from Recidron_Simulador.utilities import *
from Recidron_Simulador.styles import *

def subtitle(mensaje):
    return rx.text(
        mensaje,
        font_size="1.5em",
        font_weight="bold",
        text_align="center",
        margin_bottom="1em",
    )
def object_type_pie_chart() -> rx.Component:
    with DataBaseConnector() as db:
        object_types = db.get_objects_types()
        data = [
        {
            "name": object_type,
            "value": calculate_concentration_by_object_type(object_type, db),
            "fill": generate_random_color_hex()
        }
        for object_type in object_types
    ]
    return rx.hstack(
        subtitle("Concentration by Object Type"),
        rx.recharts.pie_chart(
            rx.recharts.pie(
                data=data,
                name_key="name",
                data_key="value",
                label=True,
            ),
            rx.recharts.graphing_tooltip(),
            width="100%",
            height=300,
        ),
        rx.vstack(
            *[
                rx.hstack(
                    rx.box(
                        background_color=item["fill"],
                        width="20px",
                        height="20px",
                        border_radius="sm",
                    ),
                    rx.text(f"{item['name']}: {item['value']} kg"),
                    spacing="2",
                )
                for item in data
            ],
            spacing="2",
            align_items="start",
        ),
        spacing="8",
    )
    
def material_pie_chart() -> rx.Component:
    with DataBaseConnector() as db:
        object_types = db.get_objects_materials()
        data = [
        {
            "name": object_type,
            "value": calculate_concentration_by_material(object_type, db),
            "fill": generate_random_color_hex()
        }
        for object_type in object_types
    ]
    return rx.hstack(
        subtitle("Concentration by Material"),
        rx.recharts.pie_chart(
            rx.recharts.pie(
                data=data,
                name_key="name",
                data_key="value",
                label=True,
            ),
            rx.recharts.graphing_tooltip(),
            width="100%",
            height=300,
        ),
        rx.vstack(
            *[
                rx.hstack(
                    rx.box(
                        background_color=item["fill"],
                        width="20px",
                        height="20px",
                        border_radius="sm",
                    ),
                    rx.text(f"{item['name']}: {item['value']} kg"),
                    spacing="2",
                )
                for item in data
            ],
            spacing="2",
            align_items="start",
        ),
        spacing="2",
    )
def zone_bar_chart() -> rx.Component:
    with DataBaseConnector() as db:
        assiged_area = db.get_assined_area()
        data = [
        {
            "name": area,
            "value": calculate_concentration_assigned_area(area, db),
            "fill": generate_random_color_hex()
        }
        for area in assiged_area
    ]
    return rx.hstack(
        subtitle("Concentration by Zone"),
        rx.recharts.bar_chart(
        rx.recharts.bar(
            data_key="value",
            stroke=rx.color("accent", 9),
            fill=rx.color("accent", 8),
        ),
        rx.recharts.x_axis(data_key="name"),
        rx.recharts.y_axis(),
        data=data,
        width="100%",
        height=250,
    ),
    rx.vstack(
        *[
            rx.hstack(
                rx.box(
                    background_color=item["fill"],
                    width="20px",
                    height="20px",
                    border_radius="sm",
                ),
                rx.text(f"Zona {item['name']}: {item['value']} kg"),
                spacing="2",
            )
            for item in data
        ]
    )
    )