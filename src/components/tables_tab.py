from dash import html
import dash_bootstrap_components as dbc
import i18n

from .tables import expenses_aggrid, incomes_aggrid
from .alerts import (
    input_table_alert,
    bank_error_alert,
    prediction_alert,
    remove_rows_alert,
)
from . import confirm_dialog, predict_btn, remove_rows_btn, save_btn
from .dropdowns.menus import upload_dd_menu


def render(expenses: list[dict], incomes: list[dict]) -> dbc.Container:
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
