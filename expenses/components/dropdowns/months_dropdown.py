from dash import Dash, html, dcc, Output, Input
import i18n

from components import ids
from data.source import DataSource


def render(app: Dash) -> html.Div:
    @app.callback(
        [
            Output(ids.MONTH_DROPDOWN, 'options'),
            Output(ids.MONTH_DROPDOWN, 'value'),
        ],
        [
            Input(ids.YEAR_DROPDOWN, 'value'),
            Input(ids.EXPENSES_TABLE, 'rowData'),
        ],
    )
    def update_dropdown(year: int, data: list[dict]) -> tuple[list[int], int]:
        source = DataSource(data)
        months: list[int] = source.unique_months_from_year(year)
        return months, max(months)
    return html.Div([
        html.H6(i18n.t("general.month")),  # type: ignore
        dcc.Dropdown(
            id=ids.MONTH_DROPDOWN,
            placeholder=i18n.t("general.month")  # type: ignore
        )
    ])
