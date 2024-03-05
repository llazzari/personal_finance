from functools import partial
from typing import Any
import pandas as pd

from components import ids
from data.raw.cleaner import (
    Preprocessor,
    clean_descriptions,
    compose,
    correct_amount_sign,
    correct_installments_date,
    create_bank_column,
    remove_ccbill_payment
)
from data.raw.reader import Reader
from data.schema import DataSchema


class BBStatement:
    patterns: list[str] = [
        '\\d+/\\d+/\\d+',
        '([\\w|\\W]+:)\\d+',
        '\\d+\\s{1}',
        '\\d{2}[\\w|\\W]+\\s{1}\\d{2}h\\d{2}min'
    ]

    @property
    def reader(self) -> Reader:
        return Reader(
            description='Histórico',
            encoding='latin-1',
            encoding_errors='replace'
        )

    def drop_1st_and_last_row(self, df: pd.DataFrame) -> pd.DataFrame:
        # These rows correspond to the balance of the bank account
        return df.iloc[1:-1]

    @property
    def cleaner(self) -> Preprocessor:
        return compose(
            partial(
                clean_descriptions,
                self.patterns,
            ),
            partial(create_bank_column, 'Banco do Brasil'),
            self.drop_1st_and_last_row
        )


class NuStatement:
    patterns: list[str] = ['^.*?-', '-.*$']

    @property
    def reader(self) -> Reader:
        return Reader()

    @property
    def cleaner(self) -> Preprocessor:
        return compose(
            partial(clean_descriptions, self.patterns),
            partial(create_bank_column, 'Nubank'),
            partial(remove_ccbill_payment, 'Pagamento de fatura')
        )


class InterStatement:
    patterns: list[str] = [
        '^.*?estabelecimento\\s{1}',
        '^Pix .*-',
        '-.*$',
        'inter pre \\d{1,}gb mensal',
        'redes sociais'
    ]

    @property
    def reader(self) -> Reader:
        return Reader(
            date='Data Lançamento',
            sep=';',
            skiprows=4,
            decimal=',',
            thousands='.'
        )

    @property
    def cleaner(self) -> Preprocessor:
        return compose(
            partial(clean_descriptions, self.patterns),
            partial(create_bank_column, 'Inter')
        )


class CoraStatement:
    @property
    def reader(self) -> Reader:
        return Reader(description='Identificação')

    @property
    def cleaner(self) -> Preprocessor:
        return compose(
            partial(clean_descriptions, []),
            partial(create_bank_column, 'Cora'),
        )


class C6CreditCard:
    payment_description: str = 'Inclusao de Pagamento    '

    @property
    def reader(self) -> Reader:
        return Reader(
            date='Data de Compra',
            amount='Valor (em R$)',
            # installment='Parcela',
            sep=';',
        )

    @property
    def cleaner(self) -> Preprocessor:
        return compose(
            correct_amount_sign,
            partial(correct_installments_date, self.payment_description),
            partial(remove_ccbill_payment, self.payment_description),
            partial(create_bank_column, 'C6'),
        )


class NuCreditCard:
    patterns: list[str] = [
        'Pg \\*',
        '\\d+/\\d$',
        'Intersho$',
    ]
    payment_description: str = 'Pagamento recebido'

    @property
    def reader(self) -> Reader:
        return Reader(
            date='date',
            amount='amount',
            description='title',
            dayfirst=False,
        )

    @property
    def cleaner(self) -> Preprocessor:
        return compose(
            partial(clean_descriptions, self.patterns),
            correct_amount_sign,
            partial(correct_installments_date, self.payment_description),
            partial(remove_ccbill_payment, self.payment_description),
            partial(create_bank_column, 'Nubank'),
        )


class SicrediCreditCard():
    payment_description: str = 'PAGAMENTO DEBITO EM'

    @property
    def reader(self) -> Reader:
        return Reader(
            date=' Data ',
            amount=' Valor ',
            amount_type=str,
            description=' Estabelecimento ',
            sep=';',
            skiprows=18,
        )

    def change_amount_to_float(self, df: pd.DataFrame) -> pd.DataFrame:
        for text in ['R$', '.']:
            df.loc[DataSchema.AMOUNT] = df[DataSchema.AMOUNT].str.replace(
                text, ''
            )
        df.loc[DataSchema.AMOUNT] = df[DataSchema.AMOUNT].str.replace(
            '- ', '-')
        df.loc[DataSchema.AMOUNT] = df[
            DataSchema.AMOUNT].str.strip().str.replace(',', '.')
        df.loc[DataSchema.AMOUNT] = df[DataSchema.AMOUNT].astype(float)
        return df

    @property
    def cleaner(self) -> Preprocessor:
        return compose(
            self.change_amount_to_float,
            correct_amount_sign,
            partial(correct_installments_date, self.payment_description),
            partial(remove_ccbill_payment, self.payment_description),
            partial(create_bank_column, 'Sicredi')
        )


class BradescoCreditCard():
    @property
    def reader(self) -> Reader:
        return Reader(
            description='Histórico',
            amount='Valor(R$)',
            encoding='latin-1',
            encoding_errors='replace',
            sep=';',
            decimal=',',
            skiprows=5,
        )

    @property
    def cleaner(self) -> Preprocessor:
        return partial(clean_descriptions, [])


BANKS: dict[str, dict[str, Any]] = {
    ids.STATEMENT_MODAL: {
        'Banco do Brasil': BBStatement(),
        'Nubank': NuStatement(),
        'Inter': InterStatement(),
        'Cora': CoraStatement(),
    },
    ids.CCBILL_MODAL: {
        'C6': C6CreditCard(),
        'Nubank': NuCreditCard(),
        'Sicredi': SicrediCreditCard(),
        # 'Bradesco': BradescoCreditCard(),
    }
}
