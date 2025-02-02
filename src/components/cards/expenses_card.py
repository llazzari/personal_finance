from dash import callback, html, Output, Input, State
import dash_bootstrap_components as dbc
import i18n

from src.data.source import DataSource
from .. import ids


def render() -> html.Div:
    return html.Div(id=ids.EXP_CARD)


@callback(
    Output(ids.EXP_CARD, "children"),
    [
        Input(ids.EXPENSES_TABLE, "cellValueChanged"),
        Input(ids.MONTH_DROPDOWN, "value"),
        Input(ids.YEAR_DROPDOWN, "value"),
    ],
    State(ids.EXPENSES_TABLE, "rowData"),
)
def update_card(_, month: int, year: int, data: list[dict]) -> html.Div:
    """
    Update the card with the total expenses for the given month and year based on the input data.

    Args:
        _: Placeholder for the cell value that has changed, triggering the callback.
        month (int): The month for which expenses are to be calculated.
        year (int): The year for which expenses are to be calculated.
        data (list[dict]): The data containing the expenses for each month and year.

    Returns:
        html.Div: A Div element containing the updated card with the total expenses.
    """
    if not data:
        return html.Div(id=ids.EXP_CARD)
    source = DataSource(data)
    expenses: float = source.total_month_amount(year, month)

    return html.Div(
        dbc.Card(
            [
                dbc.CardBody(
                    [
                        html.P(
                            i18n.t("general.expenses"),
                            className="card-title",
                        ),
                        html.H6(
                            f"{i18n.t('general.money')} {expenses:.2f}",
                            className="card-body",
                        ),
                    ]
                ),
            ],
            outline=True,
            color="primary",
            className="monthly-card",
        ),
        id=ids.EXP_CARD,
        style={"margin-bottom": "5px"},
    )
