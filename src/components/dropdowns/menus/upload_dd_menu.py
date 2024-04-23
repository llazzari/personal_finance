from typing import Any
from dash import html, Output, Input, State, dcc, callback, no_update
import dash_bootstrap_components as dbc
import i18n

from src.data.raw.uploader import upload_bank_data
from src.data.raw.banks import PersonalTable
from ... import ids
from ...tables.uploader import upload_data


def render() -> html.Div:
    return html.Div(
        [
            dbc.DropdownMenu(
                [
                    dbc.DropdownMenuItem(
                        dbc.Row(
                            [
                                dbc.Col(
                                    html.I(className="bi bi-filetype-csv"), width="auto"
                                ),
                                dbc.Col(
                                    dcc.Upload(
                                        i18n.t("general.input_table"),
                                        id=ids.INPUT_TABLE_UPLOAD,
                                        multiple=True,
                                    ),
                                    width="auto",
                                ),
                            ],
                            class_name="g-0",
                        ),
                        id=ids.INPUT_TABLE_DATA_BTN,
                        n_clicks=0,
                    ),
                    dbc.DropdownMenuItem(divider=True),
                    dbc.DropdownMenuItem(
                        [
                            html.I(className="bi bi-filetype-csv"),
                            i18n.t("general.statement"),  # type: ignore
                        ],
                        id=ids.OPEN_STATEMENT_MODAL,
                    ),
                    dbc.DropdownMenuItem(
                        [
                            html.I(className="bi bi-filetype-csv"),
                            i18n.t("general.credit-card-bill"),  # type: ignore
                        ],
                        id=ids.OPEN_CCBILL_MODAL,
                    ),
                ],
                label=i18n.t("general.upload"),  # type: ignore
                align_end=True,
                color="secondary",
                style={"margin-bottom": "10px"},
            ),
        ]
    )


@callback(
    Output(ids.EXPENSES_TABLE, "rowTransaction", allow_duplicate=True),
    Output(ids.INCOMES_TABLE, "rowTransaction", allow_duplicate=True),
    Output(ids.INPUT_TABLE_ALERT, "is_open"),
    Input(ids.INPUT_TABLE_UPLOAD, "contents"),
    [
        State(ids.EXPENSES_TABLE, "rowData"),
        State(ids.INCOMES_TABLE, "rowData"),
    ],
    prevent_initial_call=True,
)
def input_table(
    contents: list[str], old_expenses: list[dict], old_incomes: list[dict]
) -> tuple[dict[str, Any] | Any, dict[str, Any] | Any, bool]:
    """
    A function that processes the input table contents and updates the expenses and incomes tables. It takes the table contents, old expenses, and old incomes as input parameters and returns a tuple of updated expenses, updated incomes, and a boolean indicating if an alert should be shown.
    """
    bank = PersonalTable()
    try:
        new_expenses, new_incomes = upload_bank_data(bank, contents)
    except ValueError:
        return no_update, no_update, True

    return (
        upload_data(old_expenses, new_expenses),
        upload_data(old_incomes, new_incomes),
        False,
    )
