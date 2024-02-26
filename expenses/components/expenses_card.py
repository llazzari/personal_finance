from dash import Dash, html, Output, Input
import dash_bootstrap_components as dbc
import i18n
import pandas as pd

from components import ids
from data.schema import DataSchema


def render(app: Dash) -> html.Div:
    @app.callback(
        Output(ids.EXP_CARD, 'children'),
        [
            Input(ids.EXPENSES_TABLE, 'data'),
            Input(ids.MONTH_DROPDOWN, 'value'),
            Input(ids.YEAR_DROPDOWN, 'value'),
        ],
    )
    def update_card(data: dict, month: int, year: int) -> html.Div:
        df = pd.DataFrame.from_records(data)
        if df.empty:
            return html.Div(i18n.t('general.no_data'))
        df_year = df.loc[df[DataSchema.YEAR] == year, :]
        df_month = df_year.loc[df_year[DataSchema.MONTH] == month, :]

        expenses: float = df_month[DataSchema.AMOUNT].sum()
        return html.Div(
            dbc.Card([
                dbc.CardHeader(html.B(i18n.t('general.total_monthly_exp'))),
                dbc.CardBody(
                    html.P(html.B(f"{i18n.t('general.money')} {expenses:.2f}"))
                )
            ]),
            id=ids.EXP_CARD
        )
    return html.Div(id=ids.EXP_CARD)
