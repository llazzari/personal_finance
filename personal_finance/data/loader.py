import pandas as pd
from pathlib import Path

from data.schema import DataSchema
from data.processor import sort_by_date


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
    df = pd.read_csv(
        file_path,
        dtype=dtype,
        usecols=list(dtype.keys()),
    )
    df['id'] = df.index
    return sort_by_date(df)
