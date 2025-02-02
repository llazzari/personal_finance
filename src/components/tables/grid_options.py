import os
from typing import Any

from .locale_text import get_locale_text


DASH_GRID_OPTIONS: dict[str, Any] = {
    "pagination": True,
    "alwaysMultiSort": True,
    "singleClickEdit": True,
    "suppressMaintainUnsortedOrder": True,
    "rowDragManaged": True,
    "rowDragEntireRow": True,
    "suppressRowTransform": True,
    "rowSelection": "multiple",
    # 'skipHeaderOnAutoSize': True,
    "suppressRowClickSelection": True,
    # 'animateRows': False,
}


def set_dash_grid_options() -> dict[str, Any]:
    if os.getenv("LOCALE") is not None:
        if os.getenv("LOCALE") != "en":
            DASH_GRID_OPTIONS["localeText"] = get_locale_text(os.environ["LOCALE"])

    return DASH_GRID_OPTIONS
