from dash import callback, html, Output, Input
import dash_bootstrap_components as dbc
import i18n

from . import ids


def render() -> html.Div:
    return html.Div(
        dbc.Button(
            [html.I(className="bi bi-save"), i18n.t("general.save")],
            id=ids.SAVE_BTN,
            class_name="main_buttons",
        ),
    )


@callback(
    Output(ids.CONFIRM_SAVE, "displayed"),
    Input(ids.SAVE_BTN, "n_clicks"),
    prevent_initial_call=True,
)
def display_confirm(_) -> bool:
    return True
