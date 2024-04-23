from dash import callback, html, dcc, Input, Output, State
import i18n

from src.data.source import DataSource
from src.components import ids


def render() -> html.Div:
    return html.Div(
        [
            html.H6(i18n.t("general.year")),  # type: ignore
            dcc.Dropdown(
                id=ids.YEAR_DROPDOWN,
                placeholder=i18n.t("general.year"),  # type: ignore
            ),
        ],
    )


@callback(
    [
        Output(ids.YEAR_DROPDOWN, "options"),
        Output(ids.YEAR_DROPDOWN, "value"),
    ],
    Input(ids.EXPENSES_TABLE, "cellValueChanged"),
    State(ids.EXPENSES_TABLE, "rowData"),
)
def update_dropdown(_, data: list[dict]) -> tuple[list[int], int]:
    if not data:
        return [], 1
    source = DataSource(data)
    years: list[int] = source.unique_years
    return years, years[0]
