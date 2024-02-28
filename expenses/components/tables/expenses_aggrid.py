import os
from typing import Any
from dash import Dash, html
import dash_ag_grid as dag
import i18n

from components import ids
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

default_column_definition: dict[str, str | bool] = {
    "sortable": False,
    "filter": "agTextColumnFilter",
    "floatingFilter": True,
    "editable": False
}

dash_grid_options: dict[str, Any] = {
    'pagination': True,
    'alwaysMultiSort': True,
    "singleClickEdit": True,
    'suppressMaintainUnsortedOrder': True,
    "rowDragManaged": True,
    "rowDragEntireRow": True,
    'suppressRowTransform': True,
}


def set_column(column: str) -> Column:
    return {'field': column, 'headerName': i18n.t(f'columns.{column}'), 'flex': 1}


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


def render(app: Dash, data: list[dict]) -> html.Div:
    year: Column = set_number_column(DataSchema.YEAR)

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

    column_defs: list[Column] = [
        year,
        month,
        amount,
        recurrent,
        category,
        subcategory,
        bank,
        description
    ]

    if os.getenv('LOCALE') is not None:
        if os.getenv('LOCALE') != 'en':
            dash_grid_options["localeText"] = get_locale_text(
                os.environ['LOCALE']
            )

    return html.Div(
        dag.AgGrid(
            rowData=data,
            columnDefs=column_defs,
            defaultColDef=default_column_definition,
            columnSize="responsiveSizeToFit",
            dashGridOptions=dash_grid_options,
            id=ids.EXPENSES_TABLE,
        ),
        className='dbc dbc-ag-grid'
    )
