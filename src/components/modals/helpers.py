from typing import Any
from dash import html, dcc, no_update
import dash_bootstrap_components as dbc

from src.data.raw.cleaner import Bank
from src.data.raw.uploader import upload_bank_data
from src.components.tables.uploader import upload_data


def buttons_row(options: dict[str, str], upload: bool = False) -> html.Div:
    def create_button(label: str, id_: str, upload: bool) -> html.Div:
        if upload:
            return html.Div(dcc.Upload(dbc.Button(label), id=id_, multiple=True))
        return html.Div(dbc.Button(label, id=id_))

    return html.Div(
        dbc.Row(
            [
                dbc.Col(
                    create_button(label, id, upload),
                    width="auto",
                )
                for label, id in options.items()
            ]
        )
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
    bank_selector: dict[str, Bank],
) -> tuple[bool, dict | Any, dict | Any, bool]:
    """Toggle modal and uploads the data to the tables accordingly."""

    bank_name: str = triggered["prop_id"].split(".")[0].split("_")[0]

    is_open: bool = toggle_modal(inputs[:-2])

    if bank_name not in bank_options:
        return is_open, no_update, no_update, False

    uploaded_contents: list[str] = triggered["value"]
    bank: Bank = bank_selector[bank_name]

    old_expenses: list[dict] = inputs[-2]
    old_incomes: list[dict] = inputs[-1]

    try:
        new_expenses, new_incomes = upload_bank_data(bank, uploaded_contents)
    except ValueError:
        return False, no_update, no_update, True
    add_exp: dict[str, Any] = upload_data(old_expenses, new_expenses)
    add_inc: dict[str, Any] = upload_data(old_incomes, new_incomes)

    return is_open, add_exp, add_inc, False


def footer(label: str, close_id: str) -> html.Div:
    return html.Div(dbc.Button(label, id=close_id, className="ms-auto"))
