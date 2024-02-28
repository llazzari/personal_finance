from dash import html, Dash
import dash_bootstrap_components as dbc

from components import (
    save_btn,
    confirm_dialog,
    upper_buttons
)
from components.tables import expenses_aggrid
from components.modals import (
    statement_modal,
    credit_card_modal,
    save_modal
)
from data.source import DataSource
from components import collapsed_graphs


def render(app: Dash, source: DataSource) -> dbc.Container:
    return dbc.Container(
        [
            html.H1(app.title),

            html.Hr(),
            upper_buttons.render(app),
            expenses_aggrid.render(app, source.table_data),
            save_btn.render(app),

            html.Hr(),
            collapsed_graphs.render(app),

            html.Hr(),

            save_modal.render(),
            confirm_dialog.render(app),
            statement_modal.render(app),
            credit_card_modal.render(app),
            # add_data_manually_modal.render(app),
            html.Div(style={'margin': '20px'})
        ],
        class_name='dbc',
        fluid=True,
    )
