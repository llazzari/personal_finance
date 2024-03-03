from dash import Dash, html
import dash_bootstrap_components as dbc
import i18n

from components import ids
from components.modals.factories import ModalBuilder, modal_with_no_data


def render(app: Dash) -> html.Div:
    modal_builder = ModalBuilder(
        i18n.t('general.add_manually'),  # type: ignore
        html.Div([
            dbc.Input(
                type='number',
                id=ids.NUMBER_ADD,
                min=1,
                max=30,
                step=1,
                style={'width': '100px', 'margin-bottom': '10px'}
            ),
        ]),
        ids.OPEN_MANUAL_EXP,
        ids.INSERT_MANUAL_DATA,
        ids.MANUAL_ADD_MODAL,
        options={},  # {ids.OPEN_MANUAL_INC: 'n_clicks'},
        custom_footer_label='general.insert_data_manually'
    )

    return modal_with_no_data(app, modal_builder)
