from dash import html, callback, Output, Input
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
import i18n

from src.components import ids
from src.components.dropdowns import years_dropdown_evolution
from src.components.figures import (
    monthly_evolution_bar_chart,
    expenses_evolution_per_category,
    yearly_evolution_line_chart,
)


def render() -> html.Div:
    return html.Div(id=ids.EVOLUTION_TAB)


@callback(
    Output(ids.EVOLUTION_TAB, "children"),
    [Input(ids.EXPENSES_TABLE, "rowData"), Input(ids.INCOMES_TABLE, "rowData")],
)
def update_tab(expenses: list[dict], incomes: list[dict]) -> html.Div:
    """
    A function to update the tab based on expenses and incomes data.

    Parameters:
    - expenses: a list of dictionaries representing expenses
    - incomes: a list of dictionaries representing incomes

    Returns:
    - html.Div: a Div component representing the updated tab content
    """
    if not expenses and not incomes:
        return html.Div(id=ids.EVOLUTION_TAB)
    return html.Div(
        [
            dbc.Row(
                [
                    dbc.Col(
                        html.H4(html.B(i18n.t("general.expenses_evolution"))),
                        width="auto",
                    ),
                    dbc.Col(
                        dmc.SegmentedControl(
                            data=[i18n.t("general.yearly"), i18n.t("general.monthly")],
                            value=i18n.t("general.monthly"),
                            id=ids.SEGMENTED_EVOLUTION,
                        )
                    ),
                ]
            ),
            html.Div(id=ids.EVOLUTION_CONTENT),
        ],
        id=ids.EVOLUTION_TAB,
        style={"margin": "10px"},
    )


@callback(
    Output(ids.EVOLUTION_CONTENT, "children"),
    Input(ids.SEGMENTED_EVOLUTION, "value"),
)
def update_content(segment: str) -> html.Div:
    if segment == i18n.t("general.yearly"):
        return html.Div(
            [
                yearly_evolution_line_chart.render(),
            ]
        )
    return html.Div(
        [
            years_dropdown_evolution.render(),
            monthly_evolution_bar_chart.render(),
            expenses_evolution_per_category.render(),
        ]
    )
