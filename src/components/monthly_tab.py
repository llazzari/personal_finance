from dash import html, callback, Output, Input
import dash_bootstrap_components as dbc
import i18n

from . import ids, incomes_card, expenses_card, balance_card
from .dropdowns import years_dropdown, months_dropdown
from .figures import (
    monthly_expenses_sunburst_chart,
    monthly_incomes_bar_chart,
)


def render() -> html.Div:
    return html.Div(id=ids.MONTHLY_TAB)


@callback(
    Output(ids.MONTHLY_TAB, "children"),
    [Input(ids.EXPENSES_TABLE, "rowData"), Input(ids.INCOMES_TABLE, "rowData")],
)
def update_tab_content(expenses: list[dict], incomes: list[dict]) -> html.Div:
    """
    Generates the content for the monthly tab based on the provided expenses and incomes data.

    Parameters:
        expenses (list[dict]): A list of dictionaries representing the expenses data.
        incomes (list[dict]): A list of dictionaries representing the incomes data.

    Returns:
        html.Div: The content for the monthly tab as a Div element.
    """
    if not expenses and not incomes:
        return html.Div()
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
        style={"margin": "5px"},
        id=ids.MONTHLY_TAB,
    )
