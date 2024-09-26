from dash import html
import dash_bootstrap_components as dbc
import i18n

from src.components import ids


def render() -> html.Div:
    return html.Div(
        dbc.Modal(
            [
                dbc.ModalBody(i18n.t("general.success_msg")),  # type: ignore
                dbc.ModalFooter(
                    dbc.Button(
                        i18n.t("general.close"),  # type: ignore
                        id=ids.CLOSE_SAVE_MODAL,
                        className="ms-auto",
                    ),
                ),
            ],
            id=ids.SAVE_MODAL,
            is_open=False,
        )
    )
