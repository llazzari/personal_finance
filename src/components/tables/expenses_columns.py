import i18n

from src.data.schema import DataSchema
from src.data.categorize.expenses_categories import CATEGORIES
from .columns import (
    Column,
    set_column,
    set_number_column,
    set_column_with_dropdown,
)


def set_columns() -> list[Column]:
    """
    Generates a list of columns for a table displaying expenses data.

    Returns:
        list[Column]: A list of Column objects representing the columns of the table.
            The columns include:
            - year: A number column representing the year of the expense.
            - month: A number column representing the month of the expense.
            - amount: A number column representing the amount of the expense.
            - recurrent: A dropdown column representing whether the expense is recurrent.
            - category: A dropdown column representing the category of the expense.
            - subcategory: A dropdown column representing the subcategory of the expense.
            - bank: A column representing the bank of the expense.
            - description: A column representing the description of the expense.
    """
    year: Column = set_number_column(DataSchema.YEAR)
    year["checkboxSelection"] = True
    year["headerCheckboxSelection"] = True
    year["lockPosition"] = "left"
    year["width"] = 150
    year["minWidth"] = 150

    month: Column = set_number_column(DataSchema.MONTH)
    month["width"] = 120
    month["minWidth"] = 120

    amount: Column = set_number_column(DataSchema.AMOUNT)
    amount["valueFormatter"] = {"function": "d3.format('.2f')(params.value)"}
    amount["width"] = 150
    amount["minWidth"] = 150

    recurrent: Column = set_column_with_dropdown(
        DataSchema.RECURRENT,
        [i18n.t(f"general.recurrent_{option}") for option in ["yes", "no"]],
    )
    recurrent["width"] = 150
    recurrent["minWidth"] = 150

    categories = categories_according_to_locale()
    category: Column = set_column_with_dropdown(
        DataSchema.CATEGORY, list(categories.keys())
    )
    category["width"] = 200
    category["minWidth"] = 200

    subcategory: Column = set_column_with_dropdown(DataSchema.SUBCATEGORY, [])
    subcategory["cellEditorParams"] = {
        "function": f"dynamicOptions(params, {categories})"
    }
    subcategory["width"] = 200
    subcategory["minWidth"] = 200

    bank: Column = set_column(DataSchema.BANK)
    bank["width"] = 130
    bank["minWidth"] = 130

    description: Column = set_column(DataSchema.DESCRIPTION)
    description["editable"] = True
    description["minWidth"] = 500

    return [year, month, amount, recurrent, category, subcategory, bank, description]


def categories_according_to_locale() -> dict[str, list[str]]:
    """
    Generates a dictionary of categories according to the current locale.

    Returns:
        dict[str, list[str]]: A dictionary where each key is a localized category name and each value is a list of localized subcategory names.
    """
    return {
        i18n.t(f"category.{k}"): [i18n.t(f"subcategory.{v}") for v in vs]
        for k, vs in CATEGORIES.items()
    }
