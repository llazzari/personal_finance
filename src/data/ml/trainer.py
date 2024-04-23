from pathlib import Path
import pandas as pd

from ..schema import DataSchema
from .randomforestclassifier import train_and_test

ML_PATH: Path = Path.cwd() / "database" / "ml"
SUBCAT_MODEL_FILE: Path = ML_PATH / "subcat_model.joblib"
SUBCAT_VECTORIZER_FILE: Path = ML_PATH / "subcat_vectorizer.joblib"
INCOME_MODEL_FILE: Path = ML_PATH / "income_model.joblib"
INCOME_VECTORIZER_FILE: Path = ML_PATH / "income_vectorizer.joblib"

expenses: pd.DataFrame = pd.read_csv(f"{ML_PATH}/train_expenses_data.csv")
incomes: pd.DataFrame = pd.read_csv(f"{ML_PATH}/train_incomes_data.csv")


def train_subcategories_model() -> None:
    train_and_test(
        X=expenses[DataSchema.CLEANED_DESCRIPTION].to_numpy(dtype="<U50"),
        y=expenses[DataSchema.SUBCATEGORY].to_numpy(dtype="<U50"),
        save_model_file=str(SUBCAT_MODEL_FILE),
        save_vectorizer_file=str(SUBCAT_VECTORIZER_FILE),
    )


def train_incomes_model() -> None:
    train_and_test(
        X=incomes[DataSchema.CLEANED_DESCRIPTION].to_numpy(dtype="<U50"),
        y=incomes[DataSchema.CATEGORY].to_numpy(dtype="<U50"),
        save_model_file=str(INCOME_MODEL_FILE),
        save_vectorizer_file=str(INCOME_VECTORIZER_FILE),
    )
