from dash import html, Dash
import dash_bootstrap_components as dbc

from components import dropdown_menus, predict_btn


def render(app: Dash) -> html.Div:
    return html.Div(
        dbc.Row(
            [
                dbc.Col(
                    dropdown_menus.upload(),
                    width='auto',
                    style={'margin-right': '10px'}
                ),
                dbc.Col(
                    dropdown_menus.add_data_manually(),
                    width='auto',
                    style={'margin-right': '10px'}
                ),
                dbc.Col(predict_btn.render(app),  width='auto'),
            ],
            justify='end',
            style={'margin': '10px'},
        ),
    )
