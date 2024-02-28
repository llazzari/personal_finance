from dash import Dash, html, Output, Input, State
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import i18n
import pandas as pd

from components import ids
from data.predictor import predict_subcategories, separate_uncategorized_data


def render(app: Dash) -> html.Div:
    @app.callback(
        Output(ids.EXPENSES_TABLE, 'rowData', allow_duplicate=True),
        Input(ids.PREDICT_BTN, 'n_clicks'),
        State(ids.EXPENSES_TABLE, 'rowData'),
        prevent_initial_call=True
    )
    def on_click(_, data: dict) -> list[dict]:
        old_df = pd.DataFrame.from_records(data)
        categorized_df, uncategorized_df = separate_uncategorized_data(old_df)

        if uncategorized_df.empty:
            raise PreventUpdate

        newly_categorized_df = predict_subcategories(uncategorized_df)

        df = pd.concat([newly_categorized_df, categorized_df])

        return df.to_dict('records')

    return html.Div(
        dbc.Button(
            i18n.t('general.predict'),
            id=ids.PREDICT_BTN,
            size='lg',
            color='secondary',
        )
    )
