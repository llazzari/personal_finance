import dash_bootstrap_components as dbc
from dash import Dash, html

from src.components import tabs
from src.data.schema import Transaction

from . import ids, title_bar
from .modals import (
    credit_card_modal,
    save_modal,
    statement_modal,
)


def render(app: Dash, transactions: list[Transaction]) -> dbc.Container:
    return dbc.Container(
        [
            title_bar.render(app.title),
            html.Div(id=ids.MAINBODY),
            save_modal.render(),
            statement_modal.render(),
            credit_card_modal.render(),
            tabs.render(transactions),
            html.Div(style={"margin": "20px"}),
        ],
        class_name="dbc dbc-container tabs-container",
        fluid=True,
    )
