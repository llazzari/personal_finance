from dash import callback, html, Output, Input
import dash_bootstrap_components as dbc
import i18n

from components import ids
from data.source import DataSource


def render() -> html.Div:
    return html.Div(id=ids.INC_CARD)


@callback(
    Output(ids.INC_CARD, 'children'),
    [
        Input(ids.INCOMES_TABLE, 'rowData'),
        Input(ids.MONTH_DROPDOWN, 'value'),
        Input(ids.YEAR_DROPDOWN, 'value'),
    ],
)
def update_card(data: list[dict], month: int, year: int) -> html.Div:
    if not data:
        return html.Div(id=ids.INC_CARD)
    source = DataSource(data)
    incomes: float = source.total_month_amount(year, month)

    return html.Div(
        dbc.Card([
            dbc.CardHeader(html.B(i18n.t(  # type: ignore
                'general.total_monthly_inc'
            ))),
            dbc.CardBody(
                html.P(html.B(f"{i18n.t('general.money')} {incomes:.2f}"))
            )
        ]),
        id=ids.INC_CARD
    )
