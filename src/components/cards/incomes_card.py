from dash import callback, html, Output, Input, State
import dash_bootstrap_components as dbc
import i18n

from src.data.source import DataSource
from .. import ids


def render() -> html.Div:
    return html.Div(id=ids.INC_CARD)


@callback(
    Output(ids.INC_CARD, "children"),
    [
        Input(ids.INCOMES_TABLE, "cellValueChanged"),
        Input(ids.MONTH_DROPDOWN, "value"),
        Input(ids.YEAR_DROPDOWN, "value"),
    ],
    State(ids.INCOMES_TABLE, "rowData"),
)
def update_card(_, month: int, year: int, data: list[dict]) -> html.Div:
    """
    Update the income card with the total income for a given month and year.

    Parameters:
        _ (Any): Placeholder for the cell value that has changed, triggering the callback.
        month (int): The month for which the income is calculated.
        year (int): The year for which the income is calculated.
        data (list[dict]): The row data from the incomes table.

    Returns:
        html.Div: The updated income card as a Div element.
    """
    if not data:
        return html.Div(id=ids.INC_CARD)
    source = DataSource(data)
    incomes: float = source.total_month_amount(year, month)

    return html.Div(
        dbc.Card(
            [
                dbc.CardBody(
                    [
                        html.P(
                            i18n.t("general.incomes"),
                            className="card-title",
                        ),
                        html.H6(
                            html.B(f"{i18n.t('general.money')} {incomes:.2f}"),
                            className="card-body",
                        ),
                    ]
                ),
            ],
            color="primary",
            outline=True,
            className="monthly-card",
        ),
        id=ids.INC_CARD,
        style={"margin-bottom": "5px"},
    )
