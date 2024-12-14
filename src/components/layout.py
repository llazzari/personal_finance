from dash import html, Dash
import dash_bootstrap_components as dbc

from . import title_bar, ids
from .modals import statement_modal, credit_card_modal, save_modal, profile_modal
from .modals.profile_modal import User


def render(app: Dash, users: list[User]) -> dbc.Container:
    return dbc.Container(
        [
            title_bar.render(app.title),
            html.Div(id=ids.MAINBODY),
            save_modal.render(),
            statement_modal.render(),
            credit_card_modal.render(),
            profile_modal.render(users),
            html.Div(style={"margin": "20px"}),
        ],
        class_name="dbc dbc-container tabs-container",
        fluid=True,
    )
