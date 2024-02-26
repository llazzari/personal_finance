from dash import Dash, html, dcc, Output, Input
import i18n
import pandas as pd

from components import ids
from data.schema import DataSchema


def render(app: Dash) -> html.Div:
    @app.callback(
        [
            Output(ids.CATEGORIES_DROPDOWN, 'options'),
            Output(ids.CATEGORIES_DROPDOWN, 'value'),
        ],
        [
            Input(ids.YEAR_DROPDOWN, 'value'),
            Input(ids.EXPENSES_TABLE, 'data'),
        ],
    )
    def update_dropdown(year: int, data: dict) -> tuple[list[int], int]:
        df = pd.DataFrame.from_records(data)
        if df.empty:
            return [], 1
        df_year = df.loc[df[DataSchema.YEAR] == year, :]
        months: list[int] = df_year[DataSchema.MONTH].unique().tolist()
        return months, months[0]
    return html.Div([
        html.H6(i18n.t("general.month")),
        dcc.Dropdown(
            id=ids.MONTH_DROPDOWN,
            placeholder=i18n.t("general.month")
        )
    ])
