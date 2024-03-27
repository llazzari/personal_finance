from dash import callback, html, Output, Input
import dash_bootstrap_components as dbc
import i18n

from components import ids
from data.source import DataSource


def render() -> html.Div:
    return html.Div(id=ids.EXP_CARD)


@callback(
    Output(ids.EXP_CARD, "children"),
    [
        Input(ids.EXPENSES_TABLE, "rowData"),
        Input(ids.MONTH_DROPDOWN, "value"),
        Input(ids.YEAR_DROPDOWN, "value"),
    ],
)
def update_card(data: list[dict], month: int, year: int) -> html.Div:
    if not data:
        return html.Div(id=ids.EXP_CARD)
    source = DataSource(data)
    expenses: float = source.total_month_amount(year, month)

    return html.Div(
        dbc.Card(
            [
                dbc.CardHeader(
                    [
                        html.I(className="bi bi-coin"),
                        html.B(i18n.t("general.expenses")),
                    ],
                    class_name="exp-card-header",
                ),
                dbc.CardBody(
                    html.P(html.B(f"{i18n.t('general.money')} {expenses:.2f}"))
                ),
            ],
            outline=True,
            color="danger",
        ),
        id=ids.EXP_CARD,
        style={"margin-bottom": "5px"},
    )
