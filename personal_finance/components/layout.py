from dash import html, Dash
import dash_bootstrap_components as dbc
import i18n

from components import (
    save_btn,
    confirm_dialog,
    collapsed_graphs,
    remove_rows_btn,
)
from components.tables import expenses_aggrid
from components.modals import (
    statement_modal,
    credit_card_modal,
    save_modal
)
from data.source import DataSource
from components.alerts import (
    bank_error_alert,
    prediction_alert,
    remove_rows_alert
)
from components import predict_btn
from components.dropdowns.menus import upload_dd_menu


def render(app: Dash, source: DataSource) -> dbc.Container:
    return dbc.Container(
        [
            html.H1(html.B(app.title)),
            # html.Hr(),
            # html.Div(
            #     html.H2(html.B(i18n.t('general.incomes'))),  # type: ignore
            # ),


            html.Hr(),
            html.Div(
                html.H2(html.B(i18n.t('general.expenses'))),  # type: ignore
                style={'text-align': 'right'},
            ),

            bank_error_alert.render(),
            upload_dd_menu.render(),
            expenses_aggrid.render(source.table_data),
            dbc.Row(
                [
                    dbc.Col(save_btn.render(), width='auto'),
                    dbc.Col(remove_rows_btn.render(), width='auto'),
                    dbc.Col(predict_btn.render(), width='auto')
                ],
                class_name='buttons_row'
            ),
            prediction_alert.render(),
            remove_rows_alert.render(),
            confirm_dialog.render(),


            html.Hr(),
            collapsed_graphs.render(),

            html.Hr(),

            save_modal.render(),
            statement_modal.render(app),
            credit_card_modal.render(app),
            html.Div(style={'margin': '20px'})
        ],
        class_name='dbc',
        fluid=True,
    )
