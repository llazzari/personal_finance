from dash import html, Input, Output, State, dcc, callback
import i18n
import os

from components import ids
from data.source import DataSource


def render() -> html.Div:
    return html.Div(
        dcc.ConfirmDialog(
            id=ids.CONFIRM_SAVE,
            message=i18n.t('general.confirm')  # type: ignore
        )
    )


@callback(
    Output(ids.SAVE_MODAL, 'is_open'),
    # Output(ids.EXPENSES_TABLE, 'getRowStyle'),
    [
        Input(ids.CONFIRM_SAVE, 'submit_n_clicks'),
        Input(ids.CLOSE_SAVE_MODAL, 'n_clicks')
    ],
    [
        State(ids.SAVE_MODAL, 'is_open'),
        State(ids.EXPENSES_TABLE, 'rowData'),
        State(ids.INCOMES_TABLE, 'rowData'),
    ],
    prevent_initial_call=True
)
def save(
    n1: int,
    n2: int,
    is_open: bool,
    expenses: list[dict],
    incomes: list[dict]
) -> bool:
    if n1:
        source_exp = DataSource(expenses)
        source_exp.save_data(os.environ['EXPENSES_PATH'])
        source_inc = DataSource(incomes)
        source_inc.save_data(os.environ['INCOMES_PATH'])
        return not is_open
    if n2:
        return not is_open
    return is_open
