from typing import Any
from dash import callback, html, Output, Input, State, no_update
import dash_bootstrap_components as dbc
import i18n

from components import ids


def render() -> html.Div:
    return html.Div(
        dbc.Button(
            [
                html.I(className='bi bi-file-x'),
                i18n.t('general.delete_rows'),
            ],
            id=ids.DELETE_ROWS_BTN,
            class_name='main_buttons'
        ),
    )


@callback(
    Output(ids.EXPENSES_TABLE, 'rowTransaction', allow_duplicate=True),
    Output(ids.INCOMES_TABLE, 'rowTransaction', allow_duplicate=True),
    Output(ids.REMOVE_DATA_ERROR_ALERT, 'is_open'),
    Input(ids.DELETE_ROWS_BTN, 'n_clicks'),
    State(ids.EXPENSES_TABLE, 'selectedRows'),
    State(ids.INCOMES_TABLE, 'selectedRows'),
    prevent_initial_call=True
)
def remove(
    _,
    selected_expenses: list[dict],
    selected_incomes: list[dict]
) -> tuple[dict[str, list[dict]] | Any, dict[str, list[dict]] | Any, bool]:
    if not selected_expenses:
        if not selected_incomes:
            return no_update, no_update, True
        return no_update, {'remove': selected_incomes}, False
    elif not selected_incomes:
        return {'remove': selected_expenses}, no_update, False

    return {'remove': selected_expenses}, {'remove': selected_incomes}, False
