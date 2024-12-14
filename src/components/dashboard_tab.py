from dash import html, callback, Output, Input
import dash_bootstrap_components as dbc

from .cards import balance_card, expenses_card, incomes_card, dropdowns_card

from . import ids
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
                    [
                        dbc.Row(
                            [
                                dbc.Col(
                                    dropdowns_card.render(),
                                    width=4,
                                ),
                                dbc.Col(
                                    dbc.Card(
                                        monthly_expenses_sunburst_chart.render(),
                                        body=True,
                                        outline=True,
                                        # class_name="",
                                        # color="primary",
                                    ),
                                    width=8,
                                ),
                            ],
                            justify="start",
                            align="top",
                        ),
                        dbc.Row(
                            [
                                dbc.Col(
                                    dbc.Card(
                                        monthly_incomes_bar_chart.render(),
                                        body=True,
                                        outline=True,
                                        class_name="dbc dbc-card mt-2 mb-2",
                                    ),
                                    width=12,
                                ),
                            ],
                            justify="center",
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
                                    class_name="mb-2",
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
