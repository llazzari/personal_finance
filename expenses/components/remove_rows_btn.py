from dash import Dash, html, Output, Input, State
import dash_bootstrap_components as dbc
import i18n

from components import ids


def render(app: Dash) -> html.Div:
    @app.callback(
        Output(ids.EXPENSES_TABLE, 'rowTransaction', allow_duplicate=True),
        Input(ids.DELETE_ROWS_BTN, 'n_clicks'),
        State(ids.EXPENSES_TABLE, 'selectedRows'),
        prevent_initial_call=True
    )
    def delete(_, selection: list[dict]) -> dict[str, list[dict]]:
        return {'remove': selection}
    return html.Div(
        dbc.Button(
            i18n.t('general.delete_rows'),
            id=ids.DELETE_ROWS_BTN,
            color='secondary',
            size='lg',
        ),
        style={'margin-left': '10px'}
    )
