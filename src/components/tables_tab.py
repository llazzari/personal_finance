import dash_bootstrap_components as dbc
import i18n
from dash import html

from src.data.schema import Transaction

from . import confirm_dialog, predict_btn, remove_rows_btn, save_btn
from .alerts import (
    bank_error_alert,
    input_table_alert,
    prediction_alert,
    remove_rows_alert,
)
from .dropdowns.menus import upload_dd_menu
from .tables import expenses_aggrid, incomes_aggrid


def render(transactions: list[Transaction]) -> dbc.Container:
    expenses: list[dict] = [
        transaction.model_dump()
        for transaction in transactions
        if transaction.amount < 0
    ]
    incomes: list[dict] = [
        transaction.model_dump()
        for transaction in transactions
        if transaction.amount > 0
    ]

    return dbc.Container(
        [
            input_table_alert.render(),
            bank_error_alert.render(),
            prediction_alert.render(),
            remove_rows_alert.render(),
            confirm_dialog.render(),
            dbc.Row(
                [
                    dbc.Col(upload_dd_menu.render(), width="auto"),
                    dbc.Col(save_btn.render(), width="auto"),
                    dbc.Col(remove_rows_btn.render(), width="auto"),
                    dbc.Col(predict_btn.render(), width="auto"),
                ],
                class_name="buttons_row",
                justify="end",
            ),
            html.H4(html.B(i18n.t("general.expenses"))),
            expenses_aggrid.render(expenses),
            html.H4(html.B(i18n.t("general.incomes"))),
            incomes_aggrid.render(incomes),
        ],
        className="dbc dbc-container",
        fluid=True,
    )
