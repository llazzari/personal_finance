from functools import partial
import io
from typing import Any
import pandas as pd

from ...components import ids
from .cleaner import (
    Preprocessor,
    clean_descriptions,
    compose,
    correct_amount_sign,
    correct_installments_date,
    create_bank_column,
    create_columns,
    remove_ccbill_payment,
    Columns,
    rename_columns,
)


class BBStatement:
    """Statement manager for Banco do Brasil (BB)."""

    @property
    def encoding(self) -> str:
        return "latin-1"

    @property
    def columns(self) -> Columns:
        return Columns(description="Histórico")

    def reader(self, data: io.StringIO) -> pd.DataFrame:
        columns: Columns = self.columns
        return pd.read_csv(
            data,
            encoding=self.encoding,
            encoding_errors="replace",
            parse_dates=[columns.date],
            usecols=columns.to_use(),
            dtype=columns.dtype(),
            dayfirst=True,
        )

    def drop_1st_and_last_row(self, df: pd.DataFrame) -> pd.DataFrame:
        # These rows correspond to the balance of the bank account
        return df.iloc[1:-1]

    @property
    def cleaner(self) -> Preprocessor:
        return compose(
            self.drop_1st_and_last_row,
            partial(rename_columns, self.columns),
            *create_columns(),
            partial(create_bank_column, "Banco do Brasil"),
            partial(
                clean_descriptions,
                [],
            ),
        )


class BradescoStatement:
    """Statement manager for Bradesco."""

    patterns: list[str] = []

    @property
    def columns(self) -> Columns:
        return Columns(description="Histórico", amount="amount")

    @property
    def encoding(self) -> str:
        return "latin-1"

    def reader(self, data: io.StringIO) -> pd.DataFrame:
        return pd.read_csv(
            data,
            encoding=self.encoding,
            encoding_errors="replace",
            skiprows=1,
            skipfooter=30,
            engine="python",
            on_bad_lines="skip",
            sep=";",
            decimal=",",
            thousands=".",
            usecols=["Data", "Histórico", "Crédito (R$)", "Débito (R$)"],
            dtype={
                "Data": str,
                "Histórico": str,
                "Crédito (R$)": float,
                "Débito (R$)": float,
            },
        )

    def drop_1st_and_last_row(self, df: pd.DataFrame) -> pd.DataFrame:
        # These rows correspond to the balance of the bank account
        return df.iloc[1:-1]

    def drop_exceeding_lines(self, df: pd.DataFrame) -> pd.DataFrame:
        return df.loc[df["Data"].notna(), :]

    def create_amount_column(self, df: pd.DataFrame) -> pd.DataFrame:
        df["amount"] = df[["Crédito (R$)", "Débito (R$)"]].sum(axis=1)
        df.drop(columns=["Crédito (R$)", "Débito (R$)"], inplace=True)
        return df

    @property
    def cleaner(self) -> Preprocessor:
        return compose(
            self.drop_exceeding_lines,
            *create_columns(),
            self.create_amount_column,
            self.drop_1st_and_last_row,
            partial(rename_columns, self.columns),
            partial(
                clean_descriptions,
                self.patterns,
            ),
            partial(create_bank_column, "Bradesco"),
        )


class NuStatement:
    """Statement manager for Nubank."""

    patterns: list[str] = ["^.*?-", "-.*$"]

    @property
    def encoding(self) -> str:
        return "utf-8"

    @property
    def columns(self) -> Columns:
        return Columns()

    def reader(self, data: io.StringIO) -> pd.DataFrame:
        columns: Columns = self.columns
        return pd.read_csv(
            data,
            parse_dates=[columns.date],
            usecols=[columns.date, columns.amount, columns.description],
            dtype=columns.dtype(),
            dayfirst=True,
        )

    @property
    def cleaner(self) -> Preprocessor:
        return compose(
            partial(rename_columns, self.columns),
            *create_columns(),
            partial(clean_descriptions, self.patterns),
            partial(create_bank_column, "Nubank"),
            partial(remove_ccbill_payment, "Pagamento de fatura"),
        )


class InterStatement:
    """Statement manager for Inter."""

    patterns: list[str] = [
        "^.*?estabelecimento\\s{1}",
        "^Pix .*-",
        "-.*$",
        "\\d{1,}gb mensal",
        "redes sociais",
    ]

    @property
    def columns(self) -> Columns:
        return Columns(date="Data Lançamento")

    def reader(self, data: io.StringIO) -> pd.DataFrame:
        columns: Columns = self.columns
        return pd.read_csv(
            data,
            sep=";",
            skiprows=4,
            decimal=",",
            thousands=".",
            parse_dates=[columns.date],
            usecols=[columns.date, columns.amount, columns.description],
            dtype=columns.dtype(),
            dayfirst=True,
        )

    @property
    def encoding(self) -> str:
        return "utf-8"

    @property
    def cleaner(self) -> Preprocessor:
        return compose(
            partial(rename_columns, self.columns),
            *create_columns(),
            partial(clean_descriptions, self.patterns),
            partial(create_bank_column, "Inter"),
        )


class CoraStatement:
    """Statement manager for Cora."""

    @property
    def columns(self) -> Columns:
        return Columns(description="Identificação")

    @property
    def encoding(self) -> str:
        return "utf-8"

    def reader(self, data: io.StringIO) -> pd.DataFrame:
        columns: Columns = self.columns
        return pd.read_csv(
            data,
            parse_dates=[columns.date],
            usecols=[columns.date, columns.amount, columns.description],
            dtype=columns.dtype(),
            dayfirst=True,
        )

    @property
    def cleaner(self) -> Preprocessor:
        return compose(
            partial(rename_columns, self.columns),
            *create_columns(),
            partial(clean_descriptions, []),
            partial(create_bank_column, "Cora"),
        )


class C6CreditCard:
    """Credit card bill manager for C6."""

    payment_description: str = "Inclusao de Pagamento    "

    @property
    def columns(self) -> Columns:
        return Columns(date="Data de Compra", amount="Valor (em R$)")

    def reader(self, data: io.StringIO) -> pd.DataFrame:
        columns: Columns = self.columns
        return pd.read_csv(
            data,
            sep=";",
            parse_dates=[columns.date],
            usecols=[columns.date, columns.amount, columns.description],
            dtype=columns.dtype(),
            dayfirst=True,
        )

    @property
    def encoding(self) -> str:
        return "utf-8"

    @property
    def cleaner(self) -> Preprocessor:
        return compose(
            partial(rename_columns, self.columns),
            *create_columns(),
            correct_amount_sign,
            partial(correct_installments_date, self.payment_description),
            partial(remove_ccbill_payment, self.payment_description),
            partial(create_bank_column, "C6"),
            partial(clean_descriptions, []),
        )


class NuCreditCard:
    """Credit card bill manager for Nubank."""

    patterns: list[str] = [
        "Pg \\*",
        "\\d+/\\d$",
        "Intersho$",
    ]
    payment_description: str = "Pagamento recebido"

    @property
    def columns(self) -> Columns:
        return Columns(
            date="date",
            amount="amount",
            description="title",
        )

    @property
    def encoding(self) -> str:
        return "utf-8"

    def reader(self, data: io.StringIO) -> pd.DataFrame:
        columns: Columns = self.columns
        return pd.read_csv(
            data,
            dayfirst=False,
            parse_dates=[columns.date],
            usecols=[columns.date, columns.amount, columns.description],
            dtype=columns.dtype(),
        )

    @property
    def cleaner(self) -> Preprocessor:
        return compose(
            partial(rename_columns, self.columns),
            *create_columns(),
            partial(clean_descriptions, self.patterns),
            correct_amount_sign,
            partial(correct_installments_date, self.payment_description),
            partial(remove_ccbill_payment, self.payment_description),
            partial(create_bank_column, "Nubank"),
        )


class SicrediCreditCard:
    """Credit card bill manager for Sicredi."""

    payment_description: str = "PAGAMENTO DEBITO EM"

    @property
    def columns(self) -> Columns:
        return Columns(
            date=" Data ",
            amount=" Valor ",
            description=" Estabelecimento ",
        )

    def reader(self, data: io.StringIO) -> pd.DataFrame:
        columns: Columns = self.columns
        return pd.read_csv(
            data,
            sep=";",
            skiprows=18,
            dayfirst=True,
            parse_dates=[columns.date],
            usecols=[columns.date, columns.amount, columns.description],
            dtype={
                columns.date: str,
                columns.description: str,
                columns.amount: str,
            },
        )

    @property
    def encoding(self) -> str:
        return "utf-8"

    def change_amount_to_float(self, df: pd.DataFrame) -> pd.DataFrame:
        columns = self.columns
        for text in ["R$", "."]:
            df.loc[:, columns.amount] = df[columns.amount].str.replace(text, "")
        df.loc[:, columns.amount] = df[columns.amount].str.replace("- ", "-")
        df.loc[:, columns.amount] = df[columns.amount].str.strip().str.replace(",", ".")
        df.loc[:, columns.amount] = df[columns.amount].astype(float)

        return df

    @property
    def cleaner(self) -> Preprocessor:
        return compose(
            self.change_amount_to_float,
            partial(rename_columns, self.columns),
            *create_columns(),
            correct_amount_sign,
            partial(correct_installments_date, self.payment_description),
            partial(remove_ccbill_payment, self.payment_description),
            partial(create_bank_column, "Sicredi"),
        )


class PersonalTable:
    """Personal table manager."""

    @property
    def columns(self) -> Columns:
        return Columns(bank="Banco")

    @property
    def encoding(self) -> str:
        return "utf-8"

    @property
    def cleaner(self) -> Preprocessor:
        return compose(
            partial(rename_columns, self.columns),
            *create_columns(),
        )

    def reader(self, data: io.StringIO) -> pd.DataFrame:
        columns: Columns = self.columns
        dtype: dict[str, type] = columns.dtype()
        dtype[columns.bank] = str  # type: ignore
        return pd.read_csv(
            data,
            dayfirst=True,
            parse_dates=[columns.date],
            usecols=[columns.date, columns.amount, columns.description, columns.bank],
            dtype=dtype,
        )


# class BradescoCreditCard():
#     @property
#     def reader(self) -> Reader:
#         return Reader(
#             description='Histórico',
#             amount='Valor(R$)',
#             encoding='latin-1',
#             encoding_errors='replace',
#             sep=';',
#             decimal=',',
#             skiprows=5,
#         )

#     @property
#     def cleaner(self) -> Preprocessor:
#         return partial(clean_descriptions, [])


BANKS: dict[str, dict[str, Any]] = {
    ids.STATEMENT_MODAL: {
        "Banco do Brasil": BBStatement(),
        "Nubank": NuStatement(),
        "Inter": InterStatement(),
        "Cora": CoraStatement(),
        # 'Bradesco': BradescoStatement(),
    },
    ids.CCBILL_MODAL: {
        "C6": C6CreditCard(),
        "Nubank": NuCreditCard(),
        "Sicredi": SicrediCreditCard(),
        # 'Bradesco': BradescoCreditCard(),
    },
}
