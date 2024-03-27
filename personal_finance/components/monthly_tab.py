from dash import html
import dash_bootstrap_components as dbc
import i18n

from components import incomes_card, expenses_card, balance_card
from components.dropdowns import years_dropdown, months_dropdown
from components.figures import (
    monthly_expenses_sunburst_chart,
    monthly_incomes_bar_chart,
)


def render() -> html.Div:
    return html.Div(
        [
            dbc.Row(
                [
                    dbc.Col(
                        html.Div(
                            [
                                html.H4(
                                    html.B(i18n.t("general.monthly_expenses")),
                                    className="right-header",
                                ),
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            years_dropdown.render(),
                                            width="auto",
                                            style={"margin-right": "10px"},
                                        ),
                                        dbc.Col(months_dropdown.render(), width="auto"),
                                    ],
                                    justify="end",
                                ),
                            ]
                        ),
                        width=12,
                    ),
                ],
                justify="start",
                style={"margin-bottom": "10px"},
            ),
            dbc.Row(
                [
                    dbc.Col(
                        [
                            incomes_card.render(),
                            expenses_card.render(),
                            balance_card.render(),
                        ],
                        width=2,
                    ),
                    dbc.Col(
                        monthly_incomes_bar_chart.render(),
                        width=5,
                    ),
                    dbc.Col(monthly_expenses_sunburst_chart.render(), width=5),
                ],
                justify="end",
            ),
        ],
        style={"margin": "10px"},
    )
