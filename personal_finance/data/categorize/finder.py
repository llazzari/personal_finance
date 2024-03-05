import functools
import yaml
import i18n
from pathlib import Path

from data.categorize.expenses_categories import (
    CATEGORIES,
    RECURRENT_SUBCATEGORIES
)

PATH = Path.cwd() / 'locale' / 'subcategory.pt.yml'


@functools.lru_cache
def set_subcategories_from_yaml() -> dict[str, str]:
    with open(PATH, 'r') as f:
        subcategories_yaml: dict[str, dict[str, str]] = yaml.safe_load(f)
    subcategories_pt: dict[str, str] = subcategories_yaml['pt']
    return {v: k for k, v in subcategories_pt.items()}


def find_category(subcategory_label: str) -> str:
    subcategories: dict[str, str] = set_subcategories_from_yaml()

    subcategory: str = subcategories[subcategory_label]

    category: str = list(
        filter(
            lambda c: subcategory in CATEGORIES[c], CATEGORIES.keys()
        )
    )[0]
    return i18n.t(f'category.{category}')


def find_recurrences(subcategory_label: str) -> str:
    is_recurrent: str = 'no'

    subcategories: dict[str, str] = set_subcategories_from_yaml()
    subcategory: str = subcategories[subcategory_label]

    if subcategory in RECURRENT_SUBCATEGORIES:
        is_recurrent: str = 'yes'
    return i18n.t(f'general.recurrent_{is_recurrent}')
