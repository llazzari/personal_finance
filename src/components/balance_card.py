from dash import html, callback, Input, Output, State
import dash_bootstrap_components as dbc
import i18n

from src.data.source import DataSource
from . import ids


def render() -> html.Div:
    return html.Div(id=ids.BALANCE_CARD)


@callback(
    Output(ids.BALANCE_CARD, "children"),
    [
        Input(ids.MONTH_DROPDOWN, "value"),
        Input(ids.YEAR_DROPDOWN, "value"),
        Input(ids.EXPENSES_TABLE, "cellValueChanged"),
        Input(ids.INCOMES_TABLE, "cellValueChanged"),
    ],
    [
        State(ids.EXPENSES_TABLE, "rowData"),
        State(ids.INCOMES_TABLE, "rowData"),
    ],
)
def update_card(
    month: int, year: int, _, __, expenses: list[dict], incomes: list[dict]
) -> html.Div:
    """
    Updates the balance card with the given month, year, expenses, and incomes.

    Args:
        month (int): The month for which the balance is being calculated.
        year (int): The year for which the balance is being calculated.
        expenses (list[dict]): The expenses for the given month and year.
        incomes (list[dict]): The incomes for the given month and year.

    Returns:
        html.Div: The updated balance card as an html.Div element.
    """
    incomes_source = DataSource(incomes)
    expenses_source = DataSource(expenses)
    total_income: float = incomes_source.total_month_amount(year, month)
    total_expense: float = expenses_source.total_month_amount(year, month)
    balance: float = total_income - total_expense

    return html.Div(
        dbc.Card(
            [
                dbc.CardHeader(
                    [
                        html.I(
                            className="bi bi-cash-coin",
                        ),
                        html.B(i18n.t("general.balance")),
                    ],
                    class_name="bal-card-header",
                ),
                dbc.CardBody(
                    html.P(html.B(f"{i18n.t('general.money')} {balance:.2f}"))
                ),
            ],
            outline=True,
            color="primary",
        )
    )
