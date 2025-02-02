import i18n
from dash import html, Input, Output, State, dcc, callback

from src.data.user import DATABASE_PATH
from src.data.source import DataSource
from . import ids


def render() -> html.Div:
    return html.Div(
        dcc.ConfirmDialog(
            id=ids.CONFIRM_SAVE, message=i18n.t("general.confirm")  # type: ignore
        )
    )


@callback(
    Output(ids.SAVE_MODAL, "is_open"),
    # Output(ids.EXPENSES_TABLE, 'getRowStyle'),
    [
        Input(ids.CONFIRM_SAVE, "submit_n_clicks"),
        Input(ids.CLOSE_SAVE_MODAL, "n_clicks"),
    ],
    [
        State(ids.SAVE_MODAL, "is_open"),
        State(ids.EXPENSES_TABLE, "rowData"),
        State(ids.INCOMES_TABLE, "rowData"),
        State(ids.ACTIVE_USER, "data"),
    ],
    prevent_initial_call=True,
)
def save(
    n1: int,
    n2: int,
    is_open: bool,
    expenses: list[dict],
    incomes: list[dict],
    active_user: str,
) -> bool:
    """
    This function is a callback that handles the opening and closing of the save modal. It takes in three inputs: `n1`, `n2`, and `is_open`. `n1` and `n2` are the submit and close click counts respectively, while `is_open` is a boolean indicating whether the save modal is open or not. The function also takes in two states: `expenses` and `incomes`, which are lists of dictionaries representing expense and income data respectively.

    If `n1` is not zero, the function saves the expense and income data to their respective files and returns the negation of `is_open`. If `n2` is not zero, the function also returns the negation of `is_open`. Otherwise, it returns the value of `is_open`.

    The function returns a boolean indicating whether the save modal should be open or closed.
    """
    if n1:
        source_exp = DataSource(expenses)
        source_exp.save_data(f"{DATABASE_PATH}/{active_user.lower()}_expenses.csv")
        source_inc = DataSource(incomes)
        source_inc.save_data(f"{DATABASE_PATH}/{active_user.lower()}_incomes.csv")
        return not is_open
    if n2:
        return not is_open
    return is_open
