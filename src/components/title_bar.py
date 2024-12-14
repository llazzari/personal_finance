import dash_mantine_components as dmc
from dash_iconify import DashIconify
from dash import html

from . import ids


def render(title: str) -> dmc.Grid:
    return dmc.Grid(
        [
            dmc.Col(
                html.H5(html.B(title), style={"margin-top": "10px"}),
                span="content",
            ),
            dmc.Col(
                dmc.ActionIcon(
                    DashIconify(icon="mdi:account", width=30, height=30),
                    variant="subtle",
                    radius="xl",
                    size=30,
                    style={"margin-top": "10px"},
                    id=ids.PROFILE_BTN,
                ),
                span="content",
            ),
        ],
        justify="space-between",
        align="center",
    )
