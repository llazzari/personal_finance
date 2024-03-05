import i18n

from components.tables.columns import (
    Column,
    set_column,
    set_number_column,
    set_column_with_dropdown,
)
from data.schema import DataSchema
from data.categorize.expenses_categories import CATEGORIES


def set_columns() -> list[Column]:
    year: Column = set_number_column(DataSchema.YEAR)
    year['checkboxSelection'] = True
    year['headerCheckboxSelection'] = True
    year['lockPosition'] = 'left'

    month: Column = set_number_column(DataSchema.MONTH)

    amount: Column = set_number_column(DataSchema.AMOUNT)
    amount["valueFormatter"] = {"function": "d3.format('.2f')(params.value)"}

    recurrent: Column = set_column_with_dropdown(
        DataSchema.RECURRENT,
        [i18n.t(f'general.recurrent_{option}') for option in ['yes', 'no']]
    )

    categories = categories_according_to_locale()
    category: Column = set_column_with_dropdown(
        DataSchema.CATEGORY,
        list(categories.keys())
    )
    subcategory: Column = set_column_with_dropdown(
        DataSchema.SUBCATEGORY,
        []
    )
    subcategory['cellEditorParams'] = {
        'function': f'dynamicOptions(params, {categories})'
    }

    bank: Column = set_column(DataSchema.BANK)

    description: Column = set_column(DataSchema.DESCRIPTION)
    description['editable'] = True

    return [
        year,
        month,
        amount,
        recurrent,
        category,
        subcategory,
        bank,
        description
    ]


def categories_according_to_locale() -> dict[str, list[str]]:
    return {
        i18n.t(f'category.{k}'): [i18n.t(f'subcategory.{v}') for v in vs]
        for k, vs in CATEGORIES.items()
    }
