from dash import Dash, html, Output, Input
import dash_bootstrap_components as dbc
import i18n

from components import ids
from data.source import DataSource


def render(app: Dash) -> html.Div:
    @app.callback(
        Output(ids.EXP_CARD, 'children'),
        [
            Input(ids.EXPENSES_TABLE, 'rowData'),
            Input(ids.MONTH_DROPDOWN, 'value'),
            Input(ids.YEAR_DROPDOWN, 'value'),
        ],
    )
    def update_card(data: list[dict], month: int, year: int) -> html.Div:
        if not data:
            return html.Div(id=ids.EXP_CARD)
        source = DataSource(data)
        expenses: float = source.total_month_expense(year, month)

        return html.Div(
            dbc.Card([
                dbc.CardHeader(html.B(i18n.t(  # type: ignore
                    'general.total_monthly_exp'
                ))),
                dbc.CardBody(
                    html.P(html.B(f"{i18n.t('general.money')} {expenses:.2f}"))
                )
            ]),
            id=ids.EXP_CARD
        )
    return html.Div(id=ids.EXP_CARD)
