from dash import html, Dash
import dash_bootstrap_components as dbc

from components import predict_btn
from components.dropdowns.menus import upload_dd_menu


def render(app: Dash) -> html.Div:
    return html.Div(
        dbc.Row(
            [
                dbc.Col(upload_dd_menu.render(app), width='auto'),
                dbc.Col(predict_btn.render(app),  width='auto'),
            ],
            justify='end',
            class_name='buttons_row',
        ),
    )
