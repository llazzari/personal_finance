import pandas as pd
from pathlib import Path

from data.schema import DataSchema


def load_data(file_path: Path) -> pd.DataFrame:
    if not file_path.exists():
        return pd.DataFrame()
    dtype: dict[str, type] = {
        DataSchema.YEAR: int,
        DataSchema.MONTH: int,
        DataSchema.AMOUNT: float,
        DataSchema.BANK: str,
        DataSchema.CATEGORY: str,
        DataSchema.SUBCATEGORY: str,
        DataSchema.RECURRENT: str,
        DataSchema.DESCRIPTION: str,
    }
    df: pd.DataFrame = pd.read_csv(
        file_path,
        dtype=dtype,
        usecols=list(dtype.keys()),
    )
    df["id"] = df.index
    return sort_by_date(df)


def sort_by_date(df: pd.DataFrame) -> pd.DataFrame:
    df.sort_values(
        by=[DataSchema.YEAR, DataSchema.MONTH],
        ascending=False,
        inplace=True,
    )
    return df
