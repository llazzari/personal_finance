import base64
import io
import pandas as pd

from src.data.raw.cleaner import (
    Bank,
    extract_expenses,
    extract_incomes,
)


def parse(content: str, bank: Bank) -> pd.DataFrame:
    """
    Parse the content to extract a string, decode the data using the bank's encoding, and create a pandas DataFrame.

    Args:
        content (str): The content to be parsed.
        bank (Bank): The bank object used for decoding.

    Returns:
        pd.DataFrame: The parsed data as a pandas DataFrame.
    """
    _, content_string = content.split(",")
    decoded_data: str = base64.b64decode(content_string).decode(bank.encoding)
    df: pd.DataFrame = bank.reader(io.StringIO(decoded_data))
    return df


def upload_bank_data(bank: Bank, contents: list[str]) -> tuple[pd.DataFrame, ...]:
    """
    Uploads bank data as a tuple of pandas DataFrames containing expenses and incomes.

    Args:
        bank (Bank): The bank object representing the bank from which the data is being uploaded.
        contents (list[str]): A list of strings containing the contents of the bank data.

    Returns:
        tuple[pd.DataFrame, ...]: A tuple containing two pandas DataFrames: one for expenses and one for incomes.
    """
    df: pd.DataFrame = pd.concat(
        [bank.cleaner(parse(content, bank)) for content in contents]
    )
    return extract_expenses(df), extract_incomes(df)
