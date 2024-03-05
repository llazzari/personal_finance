from dataclasses import dataclass
from typing import Any, Optional
from dash import Dash, html, Output, Input, State, dcc, ctx, no_update
import dash_bootstrap_components as dbc
import i18n
import pandas as pd

from components import ids
from data.raw.banks import BANKS
from data.raw.uploader import upload_bank_data


@dataclass
class ModalBuilder:
    header: str
    body: html.Div
    open_id: str
    close_id: str
    modal_id: str
    options: dict[str, str]
    fullscreen: bool = False
    data_id: Optional[str] = None
    custom_footer_label: Optional[str] = None

    @property
    def footer(self) -> html.Div:
        label: str = self.custom_footer_label if self.custom_footer_label is not None else 'general.close'
        return html.Div(
            dbc.Button(
                i18n.t(label),  # type: ignore
                id=self.close_id,
                className="ms-auto"
            )
        )


def build_modal(modal_builder: ModalBuilder) -> html.Div:
    return html.Div([
        dbc.Modal(
            [
                dbc.ModalHeader(modal_builder.header),
                dbc.ModalBody(modal_builder.body),
                dbc.ModalFooter(modal_builder.footer)
            ],
            id=modal_builder.modal_id,
            is_open=False,
            fullscreen=modal_builder.fullscreen
        )
    ])


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
                style={'margin-right': '5px'},
            )
            for label, id in options.items()
        ])
    )


def toggle_modal(inputs) -> bool:
    is_open: bool = inputs[-1]
    for n in inputs[:-1]:
        if n:
            return not is_open
    return is_open


def upload_bank_files(app: Dash, modal_builder: ModalBuilder) -> html.Div:
    @app.callback(
        Output(modal_builder.modal_id, 'is_open'),
        Output(ids.EXPENSES_TABLE, 'rowTransaction', allow_duplicate=True),
        Output(ids.BANK_ERROR_ALERT, 'is_open', allow_duplicate=True),
        [
            Input(modal_builder.open_id, 'n_clicks'),
            Input(modal_builder.close_id, 'n_clicks'),
            *[
                Input(option, 'contents')
                for option in modal_builder.options.values()
            ],
        ],
        State(ids.EXPENSES_TABLE, 'rowData'),
        State(modal_builder.modal_id, 'is_open'),
        prevent_initial_call=True
    )
    def toggle(*inputs) -> tuple[bool, dict | Any, bool]:
        triggered = ctx.triggered[0]
        bank_name: str = triggered['prop_id'].split('.')[0].split('_')[0]

        is_open: bool = toggle_modal(inputs)

        if bank_name not in modal_builder.options.keys():
            return is_open, no_update, False

        uploaded_contents: list[str] = triggered['value']
        bank = BANKS[modal_builder.modal_id][bank_name]

        old_data: list[dict] = inputs[-2]
        old_data_id: int = max([data['id'] for data in old_data])

        try:
            new_df: pd.DataFrame = upload_bank_data(bank, uploaded_contents)
        except ValueError:
            return False, no_update, True
        else:
            new_df['id'] = range(old_data_id+1, old_data_id+1+len(new_df))
            data: list[dict] = new_df.to_dict('records')
            add_data = {'add': data, 'addIndex': 0}

        return is_open, add_data, False

    return build_modal(modal_builder)


def modal_with_no_data(app: Dash, modal_builder: ModalBuilder) -> html.Div:
    @app.callback(
        Output(modal_builder.modal_id, 'is_open', allow_duplicate=True),
        [
            Input(modal_builder.open_id, 'n_clicks'),
            Input(modal_builder.close_id, 'n_clicks'),
            *[
                Input(option, prop)
                for option, prop in modal_builder.options.items()
            ],
        ],
        State(modal_builder.modal_id, 'is_open'),
        prevent_initial_call=True
    )
    def toggle(*inputs) -> bool:
        return toggle_modal(inputs)

    return build_modal(modal_builder)
