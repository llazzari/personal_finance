import base64
import io
import pandas as pd

from data.raw.cleaner import (
    Bank,
    compose,
    create_category_column,
    create_recurrent_column,
    create_subcategory_column,
    extract_expenses,
    extract_incomes,
    create_month_column,
    create_year_column
)


def parse(content: str, bank: Bank) -> pd.DataFrame:
    _, content_string = content.split(',')
    decoded_data = base64.b64decode(content_string).decode(bank.encoding)
    df = bank.reader(io.StringIO(decoded_data))
    return df


def upload_bank_data(
    bank: Bank,
    contents: list[str]
) -> tuple[pd.DataFrame, ...]:
    preprocessor = compose(
        bank.cleaner,
        create_category_column,
        create_subcategory_column,
        create_year_column,
        create_month_column,
        create_recurrent_column,
    )

    df = pd.concat([
        preprocessor(parse(content, bank)) for content in contents
    ])
    return extract_expenses(df), extract_incomes(df)
