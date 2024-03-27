from dash import callback, html, Output, Input, State
import dash_bootstrap_components as dbc
import i18n

from components import ids
from data.source import DataSource


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
    if not data:
        return html.Div(id=ids.INC_CARD)
    source = DataSource(data)
    incomes: float = source.total_month_amount(year, month)

    return html.Div(
        dbc.Card(
            [
                dbc.CardHeader(
                    [
                        html.I(
                            className="bi bi-cash",
                        ),
                        html.B(i18n.t("general.incomes")),
                    ],
                    class_name="inc-card-header",
                ),
                dbc.CardBody(
                    html.P(html.B(f"{i18n.t('general.money')} {incomes:.2f}"))
                ),
            ],
            color="success",
            outline=True,
        ),
        id=ids.INC_CARD,
        style={"margin-bottom": "5px"},
    )
