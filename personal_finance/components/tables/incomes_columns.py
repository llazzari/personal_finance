import i18n

from components.tables.columns import Column, set_column_with_dropdown
from components.tables.expenses_columns import set_columns
from data.categorize.incomes_categories import INC_CATEGORIES
from data.schema import DataSchema


def set_income_columns() -> list[Column]:
    inc_columns = set_columns()
    inc_columns.pop(4)  # remove subcategories
    inc_categories = categories_according_to_locale()
    inc_columns[4] = set_column_with_dropdown(
        DataSchema.CATEGORY,
        inc_categories
    )
    return inc_columns


def categories_according_to_locale() -> list[str]:
    return [i18n.t(f'inc_category.{cat}') for cat in INC_CATEGORIES]
