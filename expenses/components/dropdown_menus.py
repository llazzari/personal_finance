from typing import Any
from dash import html
import dash_bootstrap_components as dbc
import i18n

from components import ids


def create_dropdown_menu(label: str, options: list[str]) -> html.Div:

    return html.Div([
        dbc.DropdownMenu(
            [
                dbc.DropdownMenuItem(i18n.t(f'general.{option}'), id=option)
                for option in options
            ],
            label=i18n.t(f'general.{label}'),
            align_end=True,
            size='lg',
            color='secondary',
        )
    ])


def upload() -> html.Div:
    options: list[str | Any] = [ids.OPEN_STATEMENT, ids.OPEN_CCBILL]
    return create_dropdown_menu('upload', options)


def add_data_manually() -> html.Div:
    options: list[str] = [ids.OPEN_MANUAL_EXP]  # , ids.OPEN_MANUAL_INC]
    return create_dropdown_menu('add', options)
