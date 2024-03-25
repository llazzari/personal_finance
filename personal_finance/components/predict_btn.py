from typing import Any
from dash import html, Output, Input, State, no_update, callback
import dash_bootstrap_components as dbc
import i18n
import pandas as pd

from components import ids
from data.ml.predictor import predict_subcategories, separate_data
from data.source import DataSource
from data.raw.cleaner import Preprocessor, compose
from data.categorize.finder import find_categories, find_recurrences


def render() -> html.Div:
    return html.Div(
        dbc.Button(
            [html.I(className="bi bi-star"), i18n.t("general.predict")],
            id=ids.PREDICT_BTN,
            class_name="main_buttons",
        )
    )


@callback(
    Output(ids.EXPENSES_TABLE, "rowData", allow_duplicate=True),
    Output(ids.PREDICT_ERROR_ALERT, "is_open"),
    Input(ids.PREDICT_BTN, "n_clicks"),
    State(ids.EXPENSES_TABLE, "rowData"),
    prevent_initial_call=True,
)
def on_click(_, expenses: list[dict]) -> tuple[list[dict] | Any, bool]:
    source_expenses = DataSource(expenses)
    if source_expenses.is_empty:
        return no_update, True

    categorized_df, uncategorized_df = separate_data(source_expenses.dataframe)

    if uncategorized_df.empty:
        return no_update, True

    categorizer: Preprocessor = compose(
        predict_subcategories,
        find_categories,
        find_recurrences,
    )
    newly_categorized_df = categorizer(uncategorized_df)

    df: pd.DataFrame = pd.concat([newly_categorized_df, categorized_df])

    return df.to_dict("records"), False
