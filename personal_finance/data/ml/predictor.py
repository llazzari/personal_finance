from pathlib import Path
from typing import Protocol
import joblib
import numpy as np
import pandas as pd
from scipy.sparse import spmatrix

from data.raw.cleaner import clean_descriptions
from data.schema import DataSchema

MODEL_FILE: Path = Path.cwd() / 'data' / 'ml' / 'model.joblib'
VECTORIZER_FILE: Path = Path.cwd() / 'data' / 'ml' / 'vectorizer.joblib'


class MLModel(Protocol):
    def predict(self, X: np.ndarray | spmatrix) -> np.ndarray:
        ...


class Vectorizer(Protocol):
    def transform(self, X: np.ndarray) -> spmatrix:
        ...


def separate_data(df: pd.DataFrame) -> list[pd.DataFrame]:
    categorized_df = df.loc[df[DataSchema.SUBCATEGORY].notna(), :]
    uncategorized_df = df.loc[df[DataSchema.SUBCATEGORY].isna(), :]
    return [categorized_df, uncategorized_df]


def predict_subcategories(uncategorized_df: pd.DataFrame) -> pd.DataFrame:

    df = clean_descriptions([], uncategorized_df)

    model: MLModel = joblib.load(MODEL_FILE)
    vectorizer: Vectorizer = joblib.load(VECTORIZER_FILE)
    X_vectorized: spmatrix = vectorizer.transform(
        df[DataSchema.CLEANED_DESCRIPTION].to_numpy(dtype='<U21')
    )
    df.loc[:, DataSchema.SUBCATEGORY] = model.predict(X_vectorized)

    return df
