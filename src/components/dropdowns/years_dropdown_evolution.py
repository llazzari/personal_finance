from dash import callback, html, dcc, Input, Output, State
import i18n

from src.components import ids
from src.data.source import DataSource


def render() -> html.Div:
    return html.Div(
        [
            html.H6(i18n.t("general.year")),  # type: ignore
            dcc.Dropdown(
                id=ids.YEAR_DROPDOWN_EVOLUTION,
                placeholder=i18n.t("general.year"),  # type: ignore
                style={"margin-bottom": "10px", "width": "30%"},
            ),
        ],
    )


@callback(
    [
        Output(ids.YEAR_DROPDOWN_EVOLUTION, "options"),
        Output(ids.YEAR_DROPDOWN_EVOLUTION, "value"),
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
