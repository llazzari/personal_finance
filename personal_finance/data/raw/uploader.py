import base64
from functools import partial
import io
import pandas as pd

from data.raw.cleaner import (
    Bank,
    compose,
    create_category_column,
    create_recurrent_column,
    create_subcategory_column,
    extract_expenses,
    rename_columns,
    create_month_column,
    create_year_column
)
from data.raw.reader import Reader


def parse(content: str, reader: Reader) -> pd.DataFrame:
    _, content_string = content.split(',')
    decoded_data = base64.b64decode(content_string).decode(reader.encoding)

    df = pd.read_csv(
        io.StringIO(decoded_data),
        usecols=reader.cols_to_use,
        dtype=reader.cols_dtypes,
        parse_dates=reader.date_parser,
        dayfirst=reader.dayfirst,
        sep=reader.sep,
        skiprows=reader.skiprows,  # type: ignore
        decimal=reader.decimal,
        thousands=reader.thousands,
        encoding=reader.encoding,
        encoding_errors=reader.encoding_errors,
    )
    return df


def upload_bank_data(bank: Bank, contents: list[str]) -> pd.DataFrame:
    preprocessor = compose(
        create_category_column,
        create_subcategory_column,
        partial(rename_columns, bank.reader),
        create_year_column,
        create_month_column,
        create_recurrent_column,
        bank.cleaner,
        extract_expenses,
    )

    return pd.concat([
        preprocessor(parse(content, bank.reader)) for content in contents
    ])


def upload_personal_table_data(contents: list[str]) -> pd.DataFrame:
    reader = Reader(bank='Banco')
    preprocessor = compose(
        create_category_column,
        create_subcategory_column,
        partial(rename_columns, reader),
        create_year_column,
        create_month_column,
        create_recurrent_column,
        extract_expenses,
    )
    return pd.concat([
        preprocessor(parse(content, reader)) for content in contents
    ])
