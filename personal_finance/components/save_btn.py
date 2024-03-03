from dash import Dash, html, Output, Input
import dash_bootstrap_components as dbc
import i18n

from components import ids


def render(app: Dash) -> html.Div:
    @app.callback(
        Output(ids.CONFIRM_SAVE, 'displayed'),
        Input(ids.SAVE_BTN, 'n_clicks'),
        prevent_initial_call=True
    )
    def display_confirm(n: int) -> bool:
        return True
    return html.Div(
        dbc.Button(
            i18n.t('general.save'),  # type: ignore
            id=ids.SAVE_BTN,
            class_name='main_buttons left_buttons'
        ),
    )
