from dash import Dash, html
import dash_bootstrap_components as dbc
import i18n

from components import ids


def render(app: Dash) -> html.Div:
    return html.Div(
        dbc.Alert(
            i18n.t('general.prediction_error'),
            id=ids.PREDICT_ERROR_ALERT,
            is_open=False,
            duration=4000,
            color='danger',
        ),
        style={'width': 'auto', 'margin-right': 0, 'margin-left': 'auto'},
    )
