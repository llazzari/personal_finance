from typing import Any
from dash import Dash, html, Output, Input, State, no_update
import dash_bootstrap_components as dbc
import i18n

from components import ids


def render(app: Dash) -> html.Div:
    @app.callback(
        Output(ids.EXPENSES_TABLE, 'rowTransaction', allow_duplicate=True),
        Output(ids.REMOVE_DATA_ERROR_ALERT, 'is_open'),
        Input(ids.DELETE_ROWS_BTN, 'n_clicks'),
        State(ids.EXPENSES_TABLE, 'selectedRows'),
        prevent_initial_call=True
    )
    def remove(
        _,
        selection: list[dict]
    ) -> tuple[dict[str, list[dict]] | Any, bool]:
        if not selection:
            return no_update, True
        return {'remove': selection}, False
    return html.Div(
        dbc.Button(
            i18n.t('general.delete_rows'),
            id=ids.DELETE_ROWS_BTN,
            color='secondary',
            size='lg',
        ),
        style={'margin-left': '10px'}
    )
