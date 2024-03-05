from dash import callback, html, Output, Input
import dash_bootstrap_components as dbc
import i18n

from components import ids
from components.dropdowns import months_dropdown, years_dropdown
from components.figures import sunburst_chart, bar_chart
from components import expenses_card
from data.source import DataSource


def render() -> dbc.Collapse:
    return dbc.Collapse(
        [
            _monthly_sunburst_chart(),
            html.Hr(),
            _evolution_bar_chart(),
        ],
        is_open=False,
        id=ids.COLLAPSE_GRAPHS
    )


@callback(
    Output(ids.COLLAPSE_GRAPHS, 'is_open'),
    Input(ids.EXPENSES_TABLE, 'rowData'),
)
def toggle_collapse(data: list[dict]):
    source = DataSource(data)
    if source.is_empty:
        return False
    return True


def _monthly_sunburst_chart() -> html.Div:
    return html.Div([
        dbc.Row(
            [
                dbc.Col(
                    html.Div([
                        html.H4(html.B(i18n.t(  # type: ignore
                            'general.monthly_expenses'
                        ))),
                        dbc.Row(
                            [
                                dbc.Col(
                                    years_dropdown.render(),
                                    width='auto',
                                    style={'margin-right': '10px'}
                                ),
                                dbc.Col(
                                    months_dropdown.render(),
                                    width='auto'
                                ),
                            ],
                            style={'margin': '10px'},
                        ),
                    ]),
                ),
                dbc.Col(expenses_card.render(), width='auto')
            ],
            justify='between',
            style={'margin': '10px'},
        ),
        html.Div(
            [
                # bar_polar_chart.render(app),
                sunburst_chart.render(),
            ],
            style={'justify': 'center'}
        ),
    ])


def _evolution_bar_chart() -> html.Div:
    return html.Div(
        [
            html.H4(html.B(i18n.t(  # type: ignore
                'general.expenses_evolution'
            ))),
            bar_chart.render(),
        ],
    )
