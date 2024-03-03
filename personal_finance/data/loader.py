import pandas as pd
from pathlib import Path

from data.schema import DataSchema
from data.processor import sort_by_date

DATA_PATH = Path.cwd() / "data" / "expenses.csv"


def expenses_file_exists() -> bool:
    return DATA_PATH.exists()


def load_data() -> pd.DataFrame:
    if not expenses_file_exists():
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
    df = pd.read_csv(
        DATA_PATH,
        dtype=dtype,
        usecols=list(dtype.keys()),
    )
    df['id'] = df.index
    return sort_by_date(df)


def set_table_data(new_df: pd.DataFrame) -> pd.DataFrame:
    old_df: pd.DataFrame = load_data()

    df = pd.concat([new_df, old_df])
    if not df.empty:
        df.to_csv(DATA_PATH, index=False, float_format='%.2f')
    return df
