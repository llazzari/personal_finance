from dash import html, Dash
import dash_bootstrap_components as dbc
import i18n

from components import (
    save_btn,
    confirm_dialog,
    collapsed_graphs,
    remove_rows_btn,
)
from components.tables import expenses_aggrid, incomes_aggrid
from components.modals import (
    statement_modal,
    credit_card_modal,
    save_modal
)
from components.alerts import (
    bank_error_alert,
    prediction_alert,
    remove_rows_alert,
    input_table_alert
)
from components import predict_btn
from components.dropdowns.menus import upload_dd_menu


def render(
    app: Dash,
    expenses: list[dict],
    incomes: list[dict]
) -> dbc.Container:
    return dbc.Container(
        [
            html.H1(html.B(app.title)),
            # html.Hr(),
            # html.Div(
            #     html.H2(html.B(i18n.t('general.incomes'))),  # type: ignore
            # ),


            html.Hr(),

            input_table_alert.render(),
            bank_error_alert.render(),
            prediction_alert.render(),
            remove_rows_alert.render(),
            confirm_dialog.render(),

            dbc.Row(
                [
                    dbc.Col(upload_dd_menu.render(), width='auto'),
                    dbc.Col(save_btn.render(), width='auto'),
                    dbc.Col(remove_rows_btn.render(), width='auto'),
                    dbc.Col(predict_btn.render(), width='auto'),
                ],
                class_name='buttons_row',
                justify='end',
            ),
            html.H2(html.B(i18n.t('general.expenses'))),
            expenses_aggrid.render(expenses),

            html.H2(html.B(i18n.t('general.incomes'))),
            incomes_aggrid.render(incomes),

            html.Hr(),
            collapsed_graphs.render(),

            html.Hr(),

            save_modal.render(),
            statement_modal.render(),
            credit_card_modal.render(),
            html.Div(style={'margin': '20px'})
        ],
        class_name='dbc',
        fluid=True,
    )
