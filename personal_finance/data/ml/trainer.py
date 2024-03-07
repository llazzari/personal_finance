from pathlib import Path
import pandas as pd

from data.schema import DataSchema
from data.ml.randomforestclassifier import train_and_test

ML_PATH: Path = Path.cwd() / 'data' / 'ml'
SUBCAT_MODEL_FILE: Path = ML_PATH / 'subcat_model.joblib'
SUBCAT_VECTORIZER_FILE: Path = ML_PATH / 'subcat_vectorizer.joblib'
INCOME_MODEL_FILE: Path = ML_PATH / 'income_model.joblib'
INCOME_VECTORIZER_FILE: Path = ML_PATH / 'income_vectorizer.joblib'

expenses = pd.read_csv(f'{ML_PATH}/train_expenses_data.csv')
incomes = pd.read_csv(f'{ML_PATH}/train_incomes_data.csv')


def train_subcategories_model() -> None:
    train_and_test(
        X=expenses[DataSchema.CLEANED_DESCRIPTION].to_numpy(dtype='<U21'),
        y=expenses[DataSchema.SUBCATEGORY].to_numpy(dtype='<U21'),
        save_model_file=str(SUBCAT_MODEL_FILE),
        save_vectorizer_file=str(SUBCAT_VECTORIZER_FILE)
    )


def train_incomes_model() -> None:
    train_and_test(
        X=incomes[DataSchema.CLEANED_DESCRIPTION].to_numpy(dtype='<U21'),
        y=incomes[DataSchema.CATEGORY].to_numpy(dtype='<U21'),
        save_model_file=str(INCOME_MODEL_FILE),
        save_vectorizer_file=str(INCOME_VECTORIZER_FILE)
    )
