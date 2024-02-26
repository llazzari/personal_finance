from dash import Dash, html
import i18n

from components.modals.factories import (
    ModalBuilder,
    bank_buttons_row,
    upload_bank_files
)
from components import ids
from data.raw.banks import BANKS


def render(app: Dash) -> html.Div:
    options: dict[str, str] = {
        bank: f'{bank}_statement' for bank in BANKS[ids.STATEMENT_MODAL].keys()
    }
    modal_builder = ModalBuilder(
        i18n.t('general.select_bank_statement'),
        bank_buttons_row(options, upload=True),
        ids.OPEN_STATEMENT,
        ids.CLOSE_STATEMENT,
        ids.STATEMENT_MODAL,
        options,
        data_id=ids.STATEMENT_DATA,
    )
    return upload_bank_files(app, modal_builder)
