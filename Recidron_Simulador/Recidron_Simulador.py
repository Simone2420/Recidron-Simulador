"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import reflex as rx

from rxconfig import config


class State(rx.State):
    """The app state."""

    ...

def try_pie_chart() -> rx.Component:
    return rx.recharts.pie_chart(
        rx.recharts.pie(
            data=[
                {"name": "Group A", "value": 400, "fill": "#FF6B6B"},
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
