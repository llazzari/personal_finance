from typing import Any
from dash import callback, html, Output, Input, State, ctx
import dash_bootstrap_components as dbc
import i18n

from src.data.raw.banks import BANKS
from src.components import ids
from src.components.modals.helpers import buttons_row, footer, toggle_and_upload


BANK_OPTIONS: dict[str, str] = {
    bank: f"{bank}_ccbill" for bank in BANKS[ids.CCBILL_MODAL].keys()
}


def render() -> html.Div:
    return html.Div(
        [
            dbc.Modal(
                [
                    dbc.ModalHeader(i18n.t("general.select_bank_statement")),
                    dbc.ModalBody(buttons_row(BANK_OPTIONS, upload=True)),
                    dbc.ModalFooter(
                        footer(i18n.t("general.close"), ids.CLOSE_CCBILL_MODAL)
                    ),
                ],
                id=ids.CCBILL_MODAL,
                is_open=False,
            )
        ]
    )


@callback(
    Output(ids.CCBILL_MODAL, "is_open"),
    Output(ids.EXPENSES_TABLE, "rowTransaction", allow_duplicate=True),
    Output(ids.INCOMES_TABLE, "rowTransaction", allow_duplicate=True),
    Output(ids.BANK_ERROR_ALERT, "is_open", allow_duplicate=True),
    [
        Input(ids.OPEN_CCBILL_MODAL, "n_clicks"),
        Input(ids.CLOSE_CCBILL_MODAL, "n_clicks"),
        *[Input(option, "contents") for option in BANK_OPTIONS.values()],
    ],
    [
        State(ids.CCBILL_MODAL, "is_open"),
        State(ids.EXPENSES_TABLE, "rowData"),
        State(ids.INCOMES_TABLE, "rowData"),
    ],
    prevent_initial_call=True,
)
def toggle_modal_and_upload(*inputs) -> tuple[bool, Any, Any, bool]:
    triggered = ctx.triggered[0]
    return toggle_and_upload(
        triggered, inputs, list(BANK_OPTIONS.keys()), BANKS[ids.CCBILL_MODAL]
    )
