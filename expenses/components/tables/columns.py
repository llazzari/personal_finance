from typing import Any
import i18n

from data.schema import DataSchema


class TableColumns:

    def set_column(self, column: str) -> dict[str, Any]:
        return {
            'id': column,
            'name': i18n.t(f'columns.{column}'),
            'type': 'text'
        }

    def year_column(self) -> dict[str, Any]:
        year_column = self.set_column(DataSchema.YEAR)
        year_column['type'] = 'numeric'
        return year_column

    def month_column(self) -> dict[str, Any]:
        month_column = self.set_column(DataSchema.MONTH)
        month_column['type'] = 'numeric'
        return month_column

    def amount_column(self) -> dict[str, Any]:
        amount_column = self.set_column(DataSchema.AMOUNT)
        amount_column['type'] = 'numeric'
        amount_column['format'] = {
            'specifier': '.2f',
            'locale': {'decimal': i18n.t('general.decimal_sep')}
        }
        return amount_column

    def bank_column(self) -> dict[str, Any]:
        return self.set_column(DataSchema.BANK)

    def category_column(self) -> dict[str, Any]:
        category_column = self.set_column(DataSchema.CATEGORY)
        category_column['presentation'] = 'dropdown'
        category_column['editable'] = True
        return category_column

    def subcategory_column(self) -> dict[str, Any]:
        subcategory_column = self.set_column(DataSchema.SUBCATEGORY)
        subcategory_column['presentation'] = 'dropdown'
        subcategory_column['editable'] = True
        return subcategory_column

    def recurrent_column(self) -> dict[str, Any]:
        recurrent_column = self.set_column(DataSchema.RECURRENT)
        recurrent_column['presentation'] = 'dropdown'
        recurrent_column['editable'] = True
        return recurrent_column

    def description_column(self) -> dict[str, Any]:
        description_column = self.set_column(DataSchema.DESCRIPTION)
        description_column['editable'] = True
        return description_column

    def set_columns(self) -> list[dict[str, Any]]:
        return [
            self.year_column(),
            self.month_column(),
            self.amount_column(),
            self.bank_column(),
            self.category_column(),
            self.subcategory_column(),
            self.recurrent_column(),
            self.description_column()
        ]
