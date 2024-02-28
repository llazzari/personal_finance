from dash import Dash, html, dcc, Input, Output
import i18n
import pandas as pd

from components import ids
from data.schema import DataSchema


def render(app: Dash) -> html.Div:
    @app.callback(
        [
            Output(ids.YEAR_DROPDOWN, 'options'),
            Output(ids.YEAR_DROPDOWN, 'value'),
        ],
        Input(ids.EXPENSES_TABLE, 'rowData')
    )
    def update_dropdown(data: dict) -> tuple[list[int] | None, int | None]:
        df = pd.DataFrame.from_records(data)
        if df.empty:
            return [], 1
        years: list[int] = df[DataSchema.YEAR].unique().tolist()
        return years, years[0]
    return html.Div(
        [
            html.H6(i18n.t("general.year")),
            dcc.Dropdown(
                id=ids.YEAR_DROPDOWN,
                placeholder=i18n.t("general.year"),
            ),
        ],
    )
