from typing import Any
from dash import html, Output, Input, State, dcc, callback
import dash_bootstrap_components as dbc
import i18n

from components import ids
from components.tables.uploader import upload_data


def render() -> html.Div:
    return html.Div([
        dbc.DropdownMenu(
            [
                dbc.DropdownMenuItem(
                    dbc.Row(
                        [
                            dbc.Col(
                                html.I(className='bi bi-filetype-csv'),
                                width='auto'
                            ),
                            dbc.Col(
                                dcc.Upload(
                                    i18n.t('general.input_table'),
                                    id=ids.INPUT_TABLE_UPLOAD,
                                    multiple=True,
                                ),
                                width='auto'
                            )
                        ],
                        class_name='g-0'
                    ),
                    id=ids.INPUT_TABLE_DATA_BTN,
                    n_clicks=0,
                ),
                dbc.DropdownMenuItem(divider=True),
                dbc.DropdownMenuItem(
                    [
                        html.I(className='bi bi-filetype-csv'),
                        i18n.t(f'general.{ids.OPEN_STATEMENT}')
                    ],
                    id=ids.OPEN_STATEMENT,
                ),
                dbc.DropdownMenuItem(
                    [
                        html.I(className='bi bi-filetype-csv'),
                        i18n.t(f'general.{ids.OPEN_CCBILL}')
                    ],
                    id=ids.OPEN_CCBILL,
                ),
            ],
            label=i18n.t('general.upload'),
            align_end=True,
            color='secondary',
            style={'margin-bottom': '10px'},
        ),
    ])


@callback(
    Output(ids.EXPENSES_TABLE, 'rowTransaction', allow_duplicate=True),
    Input(ids.INPUT_TABLE_UPLOAD, 'contents'),
    State(ids.EXPENSES_TABLE, 'rowData'),
    prevent_initial_call=True
)
def add_input_table(contents: list[str], old_data: list[dict]) -> dict[str, Any]:
    return upload_data(old_data, contents)
