from dash import html
import dash_bootstrap_components as dbc
import i18n

from .. import ids


def render() -> html.Div:
    return html.Div(
        dbc.Alert(
            [
                html.I(className="bi bi-x-octagon-fill"),
                i18n.t("general.remove_data_error"),
            ],
            id=ids.REMOVE_DATA_ERROR_ALERT,
            is_open=False,
            duration=4000,
            color="danger",
        ),
    )
