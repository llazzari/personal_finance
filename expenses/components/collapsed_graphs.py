from dash import Dash, html, Output, Input
import dash_bootstrap_components as dbc
import pandas as pd
import i18n

from components import ids
from components.dropdowns import months_dropdown, years_dropdown
from components.figures import sunburst_chart, bar_chart
from components import expenses_card


def render(app: Dash) -> dbc.Collapse:
    @app.callback(
        Output(ids.COLLAPSE_GRAPHS, 'is_open'),
        Input(ids.EXPENSES_TABLE, 'rowData'),
    )
    def toggle_collapse(data: dict):
        df = pd.DataFrame.from_records(data)
        if df.empty:
            return False
        return True
    return dbc.Collapse(
        [
            _monthly_sunburst_chart(app),
            html.Hr(),
            _evolution_bar_chart(app),
        ],
        is_open=False,
        id=ids.COLLAPSE_GRAPHS
    )


def _monthly_sunburst_chart(app: Dash) -> html.Div:
    return html.Div([
        dbc.Row(
            [
                dbc.Col(
                    html.Div([
                        html.H4(html.B(i18n.t('general.monthly_expenses'))),
                        dbc.Row(
                            [
                                dbc.Col(
                                    years_dropdown.render(app),
                                    width='auto',
                                    style={'margin-right': '10px'}
                                ),
                                dbc.Col(months_dropdown.render(
                                        app), width='auto'),
                            ],
                            style={'margin': '10px'},
                        ),
                    ]),
                ),
                dbc.Col(expenses_card.render(app), width='auto')
            ],
            justify='between',
            style={'margin': '10px'},
        ),
        html.Div(
            [
                # bar_polar_chart.render(app),
                sunburst_chart.render(app),
            ],
            style={'justify': 'center'}
        ),
    ])


def _evolution_bar_chart(app: Dash) -> html.Div:
    return html.Div(
        [
            html.H4(html.B(i18n.t('general.expenses_evolution'))),
            bar_chart.render(app),
        ],
    )
