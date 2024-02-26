from dataclasses import dataclass
from typing import Optional


@dataclass
class Reader:
    date: str = 'Data'
    amount: str = 'Valor'
    amount_type: type = float
    description: str = 'Descrição'
    dayfirst: bool = True
    sep: str = ','
    decimal: str = '.'
    encoding_errors: str = 'strict'
    encoding: str = 'utf-8'
    skiprows: Optional[int | list[int]] = None
    thousands: Optional[str] = None

    @property
    def date_parser(self) -> list[str]:
        return [self.date]

    @property
    def cols_to_use(self) -> list[str]:
        cols_to_use = [self.date, self.description, self.amount]
        return cols_to_use

    @property
    def cols_dtypes(self) -> dict[str, type]:
        cols_dtypes = {
            self.date: str,
            self.description: str,
            self.amount: self.amount_type
        }
        return cols_dtypes
