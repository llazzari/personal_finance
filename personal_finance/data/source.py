from dataclasses import dataclass
from datetime import datetime
import os
import babel.dates
import pandas as pd

from data.loader import DATA_PATH
from data.schema import DataSchema
from data.categorize.finder import find_category


@dataclass
class DataSource:
    _data: list[dict]

    @property
    def table_data(self) -> list[dict]:
        return self._data

    @property
    def dataframe(self) -> pd.DataFrame:
        return pd.DataFrame.from_records(self.table_data)

    def drop_columns(self) -> None:
        columns_to_drop: list[str] = [
            DataSchema.DATE,
            DataSchema.CLEANED_DESCRIPTION
        ]
        self.dataframe.drop(
            columns=columns_to_drop,
            inplace=True,
            errors='ignore'
        )

    def save_data(self) -> None:
        self.drop_columns()
        self.dataframe.to_csv(DATA_PATH, index=False, float_format='%.2f')

    @property
    def is_empty(self) -> bool:
        return self.dataframe.empty

    @property
    def unique_years(self) -> list[int]:
        return self.dataframe[DataSchema.YEAR].unique().tolist()

    def filter_year(self, year: int) -> pd.DataFrame:
        return self.dataframe.query('year == @year')

    def unique_months_from_year(self, year: int) -> list[int]:
        df = self.filter_year(year)
        return df[DataSchema.MONTH].unique().tolist()

    def filter_month_and_year(self, year: int, month: int) -> pd.DataFrame:
        df = self.filter_year(year)
        return df.query('month == @month')

    def total_month_expense(self, year: int, month: int) -> float:
        df = self.filter_month_and_year(year, month)
        return df[DataSchema.AMOUNT].sum()

    def month_expense_by_category(self, year: int, month: int) -> pd.DataFrame:
        df_month = self.filter_month_and_year(year, month)
        df_month_sum = df_month.groupby(
            by=DataSchema.SUBCATEGORY
        ).sum().reset_index().sort_values(by=DataSchema.AMOUNT)
        df_month_sum.loc[:, DataSchema.CATEGORY] = df_month_sum[
            DataSchema.SUBCATEGORY
        ].apply(find_category)
        return df_month_sum

    def expense_evolution(self) -> pd.DataFrame:
        df = self.dataframe.groupby(
            [DataSchema.YEAR, DataSchema.MONTH, DataSchema.RECURRENT]
        ).sum(numeric_only=True)
        df.reset_index(inplace=True)
        df[DataSchema.MONTH] = df[DataSchema.MONTH].apply(
            self.convert_month_locale
        )
        return df

    def convert_month_locale(self, month_number: int) -> str:
        date = datetime(2000, int(month_number), 1)
        locale: str = os.environ['LOCALE']
        month: str = babel.dates.format_date(date, format='MMM', locale=locale)
        return month.capitalize().strip('.')
