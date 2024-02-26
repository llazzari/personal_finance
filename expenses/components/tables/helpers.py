from datetime import datetime
import i18n
import numpy as np

from data.categorize.base_categories import CATEGORIES


def get_categories_names() -> list[str]:
    return [i18n.t(f'category.{cat}') for cat in CATEGORIES.keys()]


def get_year_options() -> list[str]:
    today = datetime.now()
    current_year: int = today.year
    return [
        str(i)
        for i in np.arange(current_year - 5, current_year + 6)
    ]


def get_month_options() -> list[str]:
    return [str(i) for i in np.arange(1, 13)]


def get_recurrent_options() -> list[str]:
    return [i18n.t(f'general.recurrent_{option}') for option in ['yes', 'no']]
