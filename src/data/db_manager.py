import sqlite3
from functools import lru_cache
from pathlib import Path

from src.data.schema import Transaction

db_path = Path.cwd() / "database"
sql_queries_path: Path = db_path / "sql_queries"
create_transactions_table: str = Path(
    sql_queries_path / "create_transactions_table.sql"
).read_text()
get_transactions_query: str = Path(
    sql_queries_path / "get_transactions.sql"
).read_text()
insert_transaction_query: str = Path(
    sql_queries_path / "insert_transaction.sql"
).read_text()


def create_tables() -> None:
    with sqlite3.connect(db_path / "transactions.db") as connection:
        cursor = connection.cursor()
        # cursor.execute(create_users_table)
        cursor.execute(create_transactions_table)
        connection.commit()


@lru_cache()
def get_transactions() -> list[Transaction]:
    with sqlite3.connect(db_path / "transactions.db") as connection:
        cursor = connection.cursor()
        transactions_from_db = cursor.execute(get_transactions_query, ()).fetchall()
        transactions = [
            Transaction(
                description=transaction[1],
                amount=transaction[2],
                year=transaction[3],
                month=transaction[4],
                bank=transaction[5],
            )
            for transaction in transactions_from_db
        ]
    return transactions


def insert_transaction(transaction: Transaction) -> None:
    with sqlite3.connect(db_path / "transactions.db") as connection:
        cursor = connection.cursor()
        cursor.execute(
            insert_transaction_query,
            (
                transaction.user_id,
                transaction.description,
                transaction.amount,
                transaction.year,
                transaction.month,
                transaction.bank,
            ),
        )
        connection.commit()
