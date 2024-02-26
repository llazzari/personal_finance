from dash import html, Dash, dcc
import dash_bootstrap_components as dbc
# import i18n

from components import (
    ids,
    save_btn,
    confirm_dialog,
    dropdown_menus,
    predict_btn
)
from components.tables import expenses_table, input_table
from components.modals import (
    statement_modal,
    credit_card_modal,
    add_data_manually_modal,
    input_table_modal,
    save_modal
)
from data.source import DataSource
from components import collapsed_graphs


def render(app: Dash, source: DataSource) -> dbc.Container:
    return dbc.Container(
        [
            dcc.Store(
                id=ids.TABLE_DATA,
                data=source.table_data
            ),
            html.H1(app.title),

            html.Hr(),
            dbc.Row(
                [
                    dbc.Col(
                        dropdown_menus.upload(),
                        width='auto',
                        style={'margin-right': '10px'}
                    ),
                    dbc.Col(
                        dropdown_menus.add_data_manually(),
                        width='auto',
                        style={'margin-right': '10px'}
                    ),
                    dbc.Col(predict_btn.render(app),  width='auto'),
                ],
                justify='end',
                style={'margin': '10px'},
            ),
            expenses_table.render(app),
            save_btn.render(app),

            html.Hr(),
            collapsed_graphs.render(app),
            # html.H4(i18n.t('general.bar_chart_title')),
            # dbc.Row(
            #     [
            #         dbc.Col(
            #             years_dropdown.render(app),
            #             width=2,
            #             style={'margin-right': '10px'}
            #         ),
            #         dbc.Col(months_dropdown.render(app), width=2),
            #     ],
            #     style={'margin': '10px'}
            # ),
            # bar_chart.render(app),

            html.Hr(),

            save_modal.render(),
            confirm_dialog.render(app),
            statement_modal.render(app),
            credit_card_modal.render(app),
            add_data_manually_modal.render(app),
            input_table_modal.render(app),
            input_table.save_data(app),
            html.Div(style={'margin': '20px'})
        ],
        class_name='dbc',
        fluid=True,
    )
