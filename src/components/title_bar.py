import dash_mantine_components as dmc
from dash_iconify import DashIconify
from dash import html

from . import ids


def render(title: str) -> dmc.Grid:
    return dmc.Grid(
        [
            dmc.Col(
                html.H3(html.B(title), style={"margin-top": "20px"}),
                span="content",
            ),
            dmc.Col(
                dmc.ActionIcon(
                    DashIconify(icon="mdi:account", width=50, height=50),
                    variant="subtle",
                    radius="xl",
                    size=60,
                    style={"margin-top": "10px"},
                    id=ids.PROFILE_BTN,
                ),
                span="content",
            ),
        ],
        justify="space-between",
        align="center",
    )
