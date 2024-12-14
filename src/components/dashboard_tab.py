from dash import html, callback, Output, Input
import dash_bootstrap_components as dbc

from . import ids, incomes_card, expenses_card, balance_card
from .dropdowns import years_dropdown, months_dropdown
from .figures import (
    monthly_expenses_sunburst_chart,
    monthly_incomes_bar_chart,
    monthly_evolution_bar_chart,
    yearly_evolution_line_chart,
    expenses_evolution_per_category,
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
        return html.Div("No data.")
    return html.Div(
        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        [
                            dbc.Row(
                                [
                                    dbc.Col(
                                        [
                                            years_dropdown.render(),
                                            months_dropdown.render(),
                                        ],
                                        width=4,
                                    ),
                                    dbc.Col(
                                        monthly_expenses_sunburst_chart.render(),
                                        width=8,
                                    ),
                                ],
                                justify="start",
                            ),
                            dbc.Row(
                                [
                                    dbc.Col(
                                        monthly_incomes_bar_chart.render(),
                                        width=12,
                                    ),
                                ],
                                justify="center",
                                className="mt-2",
                            ),
                            dbc.Row(
                                [
                                    dbc.Col(incomes_card.render(), width=4),
                                    dbc.Col(expenses_card.render(), width=4),
                                    dbc.Col(balance_card.render(), width=4),
                                ],
                                justify="space-between",
                            ),
                        ],
                        body=True,
                    ),
                    width=5,
                ),
                dbc.Col(
                    [
                        dbc.Row(
                            dbc.Col(
                                dbc.Card(
                                    dbc.CardBody(
                                        expenses_evolution_per_category.render()
                                    ),
                                    class_name="mt-2 mb-2",
                                ),
                                width="spam",
                            )
                        ),
                        dbc.Row(
                            [
                                dbc.Col(
                                    dbc.Card(
                                        dbc.CardBody(
                                            monthly_evolution_bar_chart.render()
                                        ),
                                    ),
                                    width=7,
                                ),
                                dbc.Col(
                                    dbc.Card(
                                        dbc.CardBody(
                                            yearly_evolution_line_chart.render()
                                        ),
                                    ),
                                    width=5,
                                ),
                            ],
                            class_name="w-100",
                        ),
                    ],
                    width=7,
                ),
            ],
            justify="center",
        ),
        className="mt-2 w-100 major-card",
        id=ids.MONTHLY_TAB,
    )
