from dataclasses import dataclass
import io
from functools import reduce
from typing import Callable, Optional, Protocol
from unidecode import unidecode
import i18n
import pandas as pd
import nltk
from nltk.stem import RSLPStemmer

from ..schema import DataSchema

nltk.download("punkt")
nltk.download("stopwords")
nltk.download("rslp")


@dataclass
class Columns:
    """Defines the columns of a DataFrame."""

    date: str = "Data"
    amount: str = "Valor"
    description: str = "Descrição"
    bank: Optional[str] = None

    def to_use(self) -> list[str]:
        return [self.date, self.description, self.amount]

    def dtype(self) -> dict[str, type]:
        return {self.date: str, self.amount: float, self.description: str}


Preprocessor = Callable[[pd.DataFrame], pd.DataFrame]


class Bank(Protocol):
    """Protocol interface for Bank classes."""

    @property
    def encoding(self) -> str: ...

    @property
    def columns(self) -> Columns: ...

    def reader(self, data: io.StringIO) -> pd.DataFrame: ...

    @property
    def cleaner(self) -> Preprocessor: ...


def compose(*functions: Preprocessor) -> Preprocessor:
    """
    Composes multiple preprocessing functions into a single preprocessing function.

    Args:
        *functions (Preprocessor): Variable number of preprocessing functions to be composed.

    Returns:
        Preprocessor: A single preprocessing function that applies all the input preprocessing
        functions in sequence.
    """
    return reduce(lambda f, g: lambda x: g(f(x)), functions)


def tokenize(text: str) -> str:
    """Tokenizes, stems, and cleans text into a list of tokens (words)."""

    # Initialize the stemmer for Portuguese
    stemmer = RSLPStemmer()

    # Tokenize into words
    words: list[str] = nltk.word_tokenize(text)

    # Set of unimportant words for fast lookup
    unimportant_words = set(
        [
            "pix",
            "enviado",
            "enviada",
            "transferencia",
            "cobranca",
            "referente",
            "pacote",
            "servicos",
            "pagamento",
            "banco",
            "bol",
            "ltda",
            "conta",
            "compra",
            "cartao",
            "pagto",
            "pgto",
            "estabelecimento",
            "cp",
            "bra",
            "sa",
            "pag",
            "pelotas",
            "ifd",
            "marketplace",
            "6produto",
            "br",
        ]
        + nltk.corpus.stopwords.words("portuguese")
    )

    # Remove unimportant words and apply stemming
    stemmed_words = [
        stemmer.stem(word) for word in words if word not in unimportant_words
    ]

    # Remove duplicates while preserving order
    unique_words = list(dict.fromkeys(stemmed_words))

    return " ".join(unique_words)


def clean_descriptions(patterns: list[str], df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans the descriptions in the DataFrame by lowercasing, stripping, removing accents,
    applying specific patterns, removing punctuation, whitespaces, single letters,
    numbers, and then tokenizing the text.
    """
    df[DataSchema.CLEANED_DESCRIPTION] = (
        df[DataSchema.DESCRIPTION].str.lower().str.strip().astype(str)
    )

    # Remove accents
    df[DataSchema.CLEANED_DESCRIPTION] = df[DataSchema.CLEANED_DESCRIPTION].apply(
        unidecode
    )

    # Apply user-defined patterns
    for p in patterns:
        df[DataSchema.CLEANED_DESCRIPTION] = df[
            DataSchema.CLEANED_DESCRIPTION
        ].str.replace(p, "", regex=True, case=False)

    # General patterns
    general_patterns = [
        "\\b\\d{1,2}[-/.]\\d{1,2}[-/.]\\d{2,4}\\b",  # Remove dates
        "[^a-z0-9 ]+",  # Remove punctuation
        "[ ]{2,}",  # Remove extra whitespaces
        "\\b\\w{1}\\b",  # Remove single letters
        "\\b\\d+\\b",  # Remove isolated numbers
        "\\s{0,}\\d{3,}\\s{0,}",  # Remove long numbers (like transaction IDs)
        "\\b(r\$|usd|brl)\\b",  # Remove currency symbols
        "([\\w|\\W]+:)\\d+",
        "\\d{2}[\\w|\\W]+\\s{1}\\d{2}h\\d{2}min",
        "^.*?estabelecimento\\s{1}",
        "^Pix .*-",
        "-.*$",
        "\\d{1,}gb mensal",
        "redes sociais",
    ]
    for gp in general_patterns:
        df[DataSchema.CLEANED_DESCRIPTION] = df[
            DataSchema.CLEANED_DESCRIPTION
        ].str.replace(gp, " ", regex=True)

    # Final cleanup and tokenization
    df[DataSchema.CLEANED_DESCRIPTION] = (
        df[DataSchema.CLEANED_DESCRIPTION].str.strip().apply(tokenize)
    )

    return df


def correct_amount_sign(df: pd.DataFrame) -> pd.DataFrame:
    """Correct amount sign for credit cards."""
    df.loc[:, DataSchema.AMOUNT] *= -1
    return df


def rename_columns(columns: Columns, df: pd.DataFrame) -> pd.DataFrame:
    """
    Renames the columns of a DataFrame based on the provided mapping.

    Args:
        columns (Columns): An object that contains the current column names.
        df (pd.DataFrame): The DataFrame to be modified.

    Returns:
        pd.DataFrame: The modified DataFrame with renamed columns.
    """
    df.rename(
        columns={
            columns.amount: DataSchema.AMOUNT,
            columns.date: DataSchema.DATE,
            columns.description: DataSchema.DESCRIPTION,
            columns.bank: DataSchema.BANK,
        },
        inplace=True,
        errors="ignore",
    )
    return df


def extract_incomes(df: pd.DataFrame) -> pd.DataFrame:
    return df[df[DataSchema.AMOUNT] > 0]


def extract_expenses(df: pd.DataFrame) -> pd.DataFrame:
    df = df[df[DataSchema.AMOUNT] < 0]
    df.loc[:, DataSchema.AMOUNT] *= -1
    return df


def create_category_column(df: pd.DataFrame) -> pd.DataFrame:
    df[DataSchema.CATEGORY] = None
    return df


def create_subcategory_column(df: pd.DataFrame) -> pd.DataFrame:
    df[DataSchema.SUBCATEGORY] = None
    return df


def create_year_column(df: pd.DataFrame) -> pd.DataFrame:
    df[DataSchema.YEAR] = df[DataSchema.DATE].dt.year.astype(int)
    return df


def create_month_column(df: pd.DataFrame) -> pd.DataFrame:
    df[DataSchema.MONTH] = df[DataSchema.DATE].dt.month.astype(int)
    return df


def create_bank_column(bank_name: str, df: pd.DataFrame) -> pd.DataFrame:
    df[DataSchema.BANK] = bank_name
    return df


def create_recurrent_column(df: pd.DataFrame) -> pd.DataFrame:
    df[DataSchema.RECURRENT] = i18n.t("general.recurrent_no")  # type: ignore
    return df


def correct_installments_date(descript: str, df: pd.DataFrame) -> pd.DataFrame:
    """Sets the installment month to the month where it is charged,
    that is, the month after the previous payment."""
    previous_payment_date: pd.Series = df[df[DataSchema.DESCRIPTION] == descript][
        DataSchema.DATE
    ]

    if not previous_payment_date.empty:
        correct_date = previous_payment_date.iloc[0]
        correct_month: int = correct_date.month + 1

        df[DataSchema.MONTH] = correct_installments_month(correct_month)

        df[DataSchema.YEAR] = correct_installments_year(
            correct_month, correct_date.year
        )
    return df


def create_columns() -> tuple[Preprocessor, ...]:
    return (
        create_category_column,
        create_subcategory_column,
        create_year_column,
        create_month_column,
        create_recurrent_column,
    )


def correct_installments_month(month: int) -> int:
    if month > 12:
        month -= 12
    return month


def correct_installments_year(month: int, year: int) -> int:
    if month > 12:
        year += 1
    return year


def remove_ccbill_payment(description: str, df: pd.DataFrame) -> pd.DataFrame:
    return df.loc[df[DataSchema.DESCRIPTION] != description, :]
