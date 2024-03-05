from typing import Any
from dash import html, Dash, Output, Input, State, dcc
import dash_bootstrap_components as dbc
import i18n

from components import ids
from data.raw.uploader import upload_personal_table_data


def render(app: Dash) -> html.Div:
    @app.callback(
        Output(ids.EXPENSES_TABLE, 'rowTransaction', allow_duplicate=True),
        Input(ids.INPUT_TABLE_UPLOAD, 'contents'),
        State(ids.EXPENSES_TABLE, 'rowData'),
        prevent_initial_call=True
    )
    def add_input_table(contents: list[str], old_data: list[dict]) -> dict[str, Any]:
        old_data_id: int = max([data['id'] for data in old_data])
        new_df = upload_personal_table_data(contents)
        new_df['id'] = range(old_data_id+1, old_data_id+1+len(new_df))
        return {'add': new_df.to_dict('records'), 'addIndex': 0}
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
            # class_name='bi bi-upload',
        ),
    ])
