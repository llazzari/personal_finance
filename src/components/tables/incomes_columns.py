import i18n

from src.data.categorize.incomes_categories import INC_CATEGORIES
from src.data.schema import DataSchema
from .columns import Column, set_column_with_dropdown
from .expenses_columns import set_columns


def set_income_columns() -> list[Column]:
    """
    Generate a list of income columns with specific modifications and return it.
    """
    inc_columns: list[Column] = set_columns()
    inc_columns.pop(4)  # remove subcategories

    inc_categories: list[str] = categories_according_to_locale()

    inc_columns[4] = set_column_with_dropdown(DataSchema.CATEGORY, inc_categories)
    inc_columns[4]["minWidth"] = 200
    inc_columns[4]["width"] = 200

    return inc_columns


def categories_according_to_locale() -> list[str]:
    """
    Returns a list of categories according to the locale.
    """
    return [i18n.t(f"inc_category.{cat}") for cat in INC_CATEGORIES]
