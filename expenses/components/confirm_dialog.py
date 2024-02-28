from dash import Dash, html, Input, Output, State, dcc
import i18n
import pandas as pd

from components import ids
from data.loader import DATA_PATH


def render(app: Dash) -> html.Div:
    @app.callback(
        Output(ids.SAVE_MODAL, 'is_open'),
        [
            Input(ids.CONFIRM_SAVE, 'submit_n_clicks'),
            Input(ids.CLOSE_SAVE, 'n_clicks')
        ],
        [
            State(ids.SAVE_MODAL, 'is_open'),
            State(ids.EXPENSES_TABLE, 'rowData'),
        ],
        prevent_initial_call=True
    )
    def confirm_save(n1: int, n2: int, is_open: bool, data: dict) -> bool:
        if n1:
            df = pd.DataFrame.from_records(data)
            df.to_csv(DATA_PATH, index=False, float_format='%.2f')
            return not is_open
        if n2:
            return not is_open
        return is_open
    return html.Div(
        dcc.ConfirmDialog(
            id=ids.CONFIRM_SAVE,
            message=i18n.t('general.confirm')  # type: ignore
        )
    )
