import os
import io
import base64
import google.generativeai as genai
import pandas as pd
from google.generativeai.types.generation_types import GenerateContentResponse

from data.raw.cleaner import Bank, extract_expenses, extract_incomes
from data.ml.json_extractor import extract_json

GOOGLE_API_KEY: str | None = os.getenv("GOOGLE_API_KEY")


def read(decoded_data: str) -> str:
    model = genai.GenerativeModel("gemini-pro")
    text: str = (
        f"""Limpe os dados de acordo com as instruções a seguir e retorne um objeto JSON com os campos 'date', 'description', 'amount' e 'bank'. Mantenha somente as colunas Data, Histórico e Valor. Remova a primeira e a última linha. Renomeie as colunas: Data para date, Valor para amount, Histórico para description. Crie uma coluna chamada bank e preencha-a com o valor 'Banco do Brasil'. Faça com que o tipo da coluna 'amount' seja float. Organize os dados em ordem cronológica. Dados: {decoded_data}"""
    )
    response: GenerateContentResponse = model.generate_content(text)
    return response.text


def decode(content: str, bank: Bank) -> str:
    _, content_string = content.split(",")
    return base64.b64decode(content_string).decode(bank.encoding)


def parse(content: str, bank: Bank) -> pd.DataFrame:
    decoded_data: str = decode(content, bank)
    response_data: str = read(decoded_data)
    json_data: dict[str, list[str | float]] = extract_json(response_data)
    df: pd.DataFrame = pd.DataFrame(json_data)
    return df


def upload_bank_data(bank: Bank, contents: list[str]) -> tuple[pd.DataFrame, ...]:

    df: pd.DataFrame = pd.concat(
        [bank.cleaner(parse(content, bank)) for content in contents]
    )
    return extract_expenses(df), extract_incomes(df)
