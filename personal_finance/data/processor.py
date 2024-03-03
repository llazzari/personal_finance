from functools import reduce
from typing import Callable
import pandas as pd

from data.schema import DataSchema


Preprocessor = Callable[[pd.DataFrame], pd.DataFrame]


def sort_by_date(df: pd.DataFrame) -> pd.DataFrame:
    df.sort_values(
        by=[DataSchema.YEAR, DataSchema.MONTH],
        ascending=False,
        inplace=True
    )
    return df


def compose(*functions: Preprocessor) -> Preprocessor:
    return reduce(lambda f, g: lambda x: g(f(x)), functions)


def process(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df
    processor = compose(
        sort_by_date,
    )
    return processor(df)
