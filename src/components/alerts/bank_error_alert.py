from dash import html
import dash_bootstrap_components as dbc
import i18n

from .. import ids


def render() -> html.Div:
    return html.Div(
        dbc.Alert(
            [html.I(className="bi bi-x-octagon-fill"), i18n.t("general.bank_error")],
            id=ids.BANK_ERROR_ALERT,
            is_open=False,
            duration=4000,
            color="danger",
        ),
    )
