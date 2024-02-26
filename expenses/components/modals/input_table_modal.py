from dash import Dash, html
import i18n

from components import ids
from components.modals.factories import ModalBuilder, modal_with_no_data
from components.tables import input_table


def render(app: Dash) -> html.Div:
    modal_builder = ModalBuilder(
        i18n.t('general.input_table'),
        input_table.render(app),
        ids.INSERT_MANUAL_DATA,
        ids.CLOSE_EXPENSES,
        ids.EXPENSES_MODAL,
        options={},
        fullscreen=True,
    )
    return modal_with_no_data(app, modal_builder)
