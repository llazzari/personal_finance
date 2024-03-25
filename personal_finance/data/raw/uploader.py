import base64
import io
import pandas as pd

from data.raw.cleaner import (
    Bank,
    extract_expenses,
    extract_incomes,
)


def parse(content: str, bank: Bank) -> pd.DataFrame:
    _, content_string = content.split(",")
    decoded_data: str = base64.b64decode(content_string).decode(bank.encoding)
    df: pd.DataFrame = bank.reader(io.StringIO(decoded_data))
    return df


def upload_bank_data(bank: Bank, contents: list[str]) -> tuple[pd.DataFrame, ...]:

    df: pd.DataFrame = pd.concat(
        [bank.cleaner(parse(content, bank)) for content in contents]
    )
    return extract_expenses(df), extract_incomes(df)
