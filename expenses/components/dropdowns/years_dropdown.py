from dash import Dash, html, dcc, Input, Output
import i18n

from components import ids
from data.source import DataSource


def render(app: Dash) -> html.Div:
    @app.callback(
        [
            Output(ids.YEAR_DROPDOWN, 'options'),
            Output(ids.YEAR_DROPDOWN, 'value'),
        ],
        Input(ids.EXPENSES_TABLE, 'rowData')
    )
    def update_dropdown(data: list[dict]) -> tuple[list[int], int]:
        source = DataSource(data)
        years: list[int] = source.unique_years
        return years, years[0]
    return html.Div(
        [
            html.H6(i18n.t("general.year")),  # type: ignore
            dcc.Dropdown(
                id=ids.YEAR_DROPDOWN,
                placeholder=i18n.t("general.year"),  # type: ignore
            ),
        ],
    )
