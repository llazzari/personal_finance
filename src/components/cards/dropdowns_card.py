import dash_bootstrap_components as dbc
from src.components.dropdowns import years_dropdown, months_dropdown


def render() -> dbc.Card:
    return dbc.Card(
        [
            years_dropdown.render(),
            months_dropdown.render(),
        ],
        body=True,
        outline=True,
        class_name="dbc dbc-card",
    )
