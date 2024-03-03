from typing import Any
from dash import Dash, html, Output, Input, State, no_update
import dash_bootstrap_components as dbc
import i18n
import pandas as pd

from components import ids
from data.predictor import predict_subcategories, separate_uncategorized_data


def render(app: Dash) -> html.Div:
    @app.callback(
        Output(ids.EXPENSES_TABLE, 'rowData', allow_duplicate=True),
        Output(ids.PREDICT_ERROR_ALERT, 'is_open'),
        Input(ids.PREDICT_BTN, 'n_clicks'),
        State(ids.EXPENSES_TABLE, 'rowData'),
        prevent_initial_call=True
    )
    def on_click(_, data: dict) -> tuple[list[dict] | Any, bool]:
        old_df = pd.DataFrame.from_records(data)
        if old_df.empty:
            return no_update, True
        categorized_df, uncategorized_df = separate_uncategorized_data(old_df)

        if uncategorized_df.empty:
            return no_update, True

        newly_categorized_df = predict_subcategories(uncategorized_df)

        df = pd.concat([newly_categorized_df, categorized_df])

        return df.to_dict('records'), False

    return html.Div(
        dbc.Button(
            i18n.t('general.predict'),
            id=ids.PREDICT_BTN,
            class_name='main_buttons right_buttons'
        )
    )
