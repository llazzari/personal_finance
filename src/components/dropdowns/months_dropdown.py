from dash import callback, html, dcc, Output, Input, State
import i18n

from src.components import ids
from src.data.source import DataSource


def render() -> html.Div:
    return html.Div(
        [
            html.H6(i18n.t("general.month")),  # type: ignore
            dcc.Dropdown(
                id=ids.MONTH_DROPDOWN,
                placeholder=i18n.t("general.month"),  # type: ignore
            ),
        ]
    )


@callback(
    [
        Output(ids.MONTH_DROPDOWN, "options"),
        Output(ids.MONTH_DROPDOWN, "value"),
    ],
    [
        Input(ids.EXPENSES_TABLE, "cellValueChanged"),
        Input(ids.YEAR_DROPDOWN, "value"),
    ],
    State(ids.EXPENSES_TABLE, "rowData"),
)
def update_dropdown(_, year: int, data: list[dict]) -> tuple[list[int], int]:
    if not data:
        return [], 1
    source = DataSource(data)
    months: list[int] = source.unique_months_from_year(year)
    return months, max(months)
