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
        bank: f'{bank}_ccbill' for bank in BANKS[ids.CCBILL_MODAL].keys()
    }
    modal_builder = ModalBuilder(
        i18n.t('general.select_bank_ccbill'),
        bank_buttons_row(options, upload=True),
        ids.OPEN_CCBILL,
        ids.CLOSE_CCBILL,
        ids.CCBILL_MODAL,
        options,
        data_id=ids.CCBILL_DATA,
    )
    return upload_bank_files(app, modal_builder)
