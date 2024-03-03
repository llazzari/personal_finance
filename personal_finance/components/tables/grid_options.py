import os
from typing import Any
import i18n

from data.schema import DataSchema
from data.categorize.base_categories import CATEGORIES
from components.tables.locale_text import get_locale_text


Column = dict[str, str | int | bool | dict[str, str | list[str]]]
ColumnTypes = dict[str, dict[str, str | int | bool]]

column_types: ColumnTypes = {
    'number_column': {
        'filter': 'agNumberColumnFilter',
        'editable': False
    },
}

DEFAULT_COLUMN_DEFINITION: dict[str, str | bool] = {
    "sortable": False,
    "filter": "agTextColumnFilter",
    "floatingFilter": True,
    "editable": False
}

DASH_GRID_OPTIONS: dict[str, Any] = {
    'pagination': True,
    'alwaysMultiSort': True,
    'singleClickEdit': True,
    'suppressMaintainUnsortedOrder': True,
    'rowDragManaged': True,
    'rowDragEntireRow': True,
    'suppressRowTransform': True,
    'rowSelection': 'multiple'
}


def set_column(column: str) -> Column:
    return {'field': column, 'headerName': i18n.t(f'columns.{column}'), 'flex': 1}


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


def set_dash_grid_options() -> dict[str, Any]:
    if os.getenv('LOCALE') is not None:
        if os.getenv('LOCALE') != 'en':
            DASH_GRID_OPTIONS['localeText'] = get_locale_text(
                os.environ['LOCALE']
            )

    return DASH_GRID_OPTIONS


def set_number_column(column: str) -> Column:
    column_defs: Column = set_column(column)
    column_defs['type'] = 'numericColumn'
    column_defs['filter'] = 'agNumberColumnFilter'
    column_defs['sortable'] = True
    return column_defs


def set_column_with_dropdown(column: str, values: list[str]) -> Column:
    column_defs: Column = set_column(column)
    column_defs['cellEditor'] = 'agSelectCellEditor'
    column_defs['cellEditorParams'] = {'values': values}  # type: ignore
    column_defs['editable'] = True
    return column_defs


def categories_according_to_locale() -> dict[str, list[str]]:
    return {
        i18n.t(f'category.{k}'): [i18n.t(f'subcategory.{v}') for v in vs]
        for k, vs in CATEGORIES.items()
    }
