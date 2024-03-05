from typing import Any
from dash import html, dcc, no_update
import dash_bootstrap_components as dbc
import pandas as pd

from data.raw.cleaner import Bank
from data.raw.uploader import upload_bank_data
from components.tables.uploader import upload_data


def buttons_row(options: dict[str, str], upload: bool = False) -> html.Div:
    def create_button(label: str, id: str, upload: bool) -> html.Div:
        if upload:
            return html.Div(
                dcc.Upload(dbc.Button(label), id=id, multiple=True)
            )
        return html.Div(dbc.Button(label, id=id))
    return html.Div(
        dbc.Row([
            dbc.Col(
                create_button(label, id, upload),
                width='auto',
            )
            for label, id in options.items()
        ])
    )


def toggle_modal(inputs: tuple) -> bool:
    is_open: bool = inputs[-1]
    for n in inputs[:-1]:
        if n:
            return not is_open
    return is_open


def toggle_and_upload(
    triggered: dict,
    inputs: tuple,
    bank_options: list[str],
    bank_selector: dict[str, Bank]
) -> tuple[bool, dict | Any, bool]:

    bank_name: str = triggered['prop_id'].split('.')[0].split('_')[0]

    is_open: bool = toggle_modal(inputs[:-1])

    if bank_name not in bank_options:
        return is_open, no_update, False

    uploaded_contents: list[str] = triggered['value']
    bank: Bank = bank_selector[bank_name]

    old_data: list[dict] = inputs[-1]

    try:
        new_df: pd.DataFrame = upload_bank_data(bank, uploaded_contents)
    except ValueError:
        return False, no_update, True
    else:
        add_data = upload_data(old_data, new_df)

    return is_open, add_data, False


def footer(label: str, close_id: str) -> html.Div:
    return html.Div(
        dbc.Button(
            label,
            id=close_id,
            className="ms-auto"
        )
    )
