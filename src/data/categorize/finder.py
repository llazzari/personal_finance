import functools
from pathlib import Path
import pandas as pd
import yaml
import i18n

from .expenses_categories import CATEGORIES, RECURRENT_SUBCATEGORIES
from ..schema import DataSchema

PATH: Path = Path.cwd() / "locale" / "subcategory.pt.yml"


@functools.lru_cache
def set_subcategories_from_yaml() -> dict[str, str]:
    """
    A function to set subcategories from a YAML file and return them as a dictionary.
    """
    with open(PATH, "r", encoding="utf-8") as f:
        subcategories_yaml: dict[str, dict[str, str]] = yaml.safe_load(f)
    subcategories_pt: dict[str, str] = subcategories_yaml["pt"]
    return {v: k for k, v in subcategories_pt.items()}


@functools.lru_cache
def get_subcategory(subcategory_label: str) -> str | None:
    subcategories: dict[str, str] = set_subcategories_from_yaml()

    return subcategories.get(subcategory_label)


@functools.lru_cache
def find_category(subcategory_label: str) -> str | None:
    subcategory: str | None = get_subcategory(subcategory_label)

    if not subcategory:
        return None

    category: str = list(
        filter(lambda c: subcategory in CATEGORIES[c], CATEGORIES.keys())
    )[0]
    return i18n.t(f"category.{category}")


def find_categories(df: pd.DataFrame) -> pd.DataFrame:
    df.loc[:, DataSchema.CATEGORY] = df[DataSchema.SUBCATEGORY].apply(find_category)
    return df


@functools.lru_cache
def find_recurrency(subcategory_label: str) -> str:
    is_recurrent: str = "no"

    subcategory: str | None = get_subcategory(subcategory_label)

    if subcategory in RECURRENT_SUBCATEGORIES:
        is_recurrent: str = "yes"
    return i18n.t(f"general.recurrent_{is_recurrent}")


def find_recurrences(df: pd.DataFrame) -> pd.DataFrame:
    df.loc[:, DataSchema.RECURRENT] = df[DataSchema.SUBCATEGORY].apply(find_recurrency)
    return df
