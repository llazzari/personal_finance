import i18n

from data.categorize.base_categories import CATEGORIES
from data.schema import DataSchema


DropdownColumn = dict[str, list[dict[str, str]] | bool]
ConditionalDropdownColumns = list[
    dict[str, dict[str, str] | list[dict[str, str]] | bool]
]


def set_dropdown_for(values: list[str]) -> DropdownColumn:
    return {
        'options': [{'label': value, 'value': value} for value in values],
        'clearable': False
    }


def set_conditional_dropdown_for_subcategories() -> ConditionalDropdownColumns:
    def condition(category_name: str) -> dict[str, str]:
        return {
            'column_id': DataSchema.SUBCATEGORY,  # skip-id-check
            'filter_query': f'{{{DataSchema.CATEGORY}}} eq "{i18n.t(f"""category.{category_name}""")}"'
        }

    def option(subcategory_name: str) -> dict[str, str]:
        return {
            'label': i18n.t(  # type: ignore
                f'subcategory.{subcategory_name}'
            ),
            'value': i18n.t(  # type: ignore
                f'subcategory.{subcategory_name}'
            ),
        }
    return [
        {
            'if': condition(cat),
            'options': [option(subcat) for subcat in CATEGORIES[cat]],
            'clearable': True,
        }
        for cat in CATEGORIES.keys()
    ]
