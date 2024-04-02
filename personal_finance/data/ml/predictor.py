import joblib
import numpy as np
import pandas as pd
from scipy.sparse import spmatrix
from typing import Protocol

from data.raw.cleaner import clean_descriptions
from data.schema import DataSchema
from data.ml.trainer import (
    SUBCAT_MODEL_FILE,
    SUBCAT_VECTORIZER_FILE,
)


class MLModel(Protocol):
    def predict(self, X: np.ndarray | spmatrix) -> np.ndarray: ...


class Vectorizer(Protocol):
    def transform(self, X: np.ndarray) -> spmatrix: ...


def separate_data(df: pd.DataFrame) -> list[pd.DataFrame]:
    categorized_df: pd.DataFrame = df.loc[df[DataSchema.SUBCATEGORY].notna(), :]
    uncategorized_df: pd.DataFrame = df.loc[df[DataSchema.SUBCATEGORY].isna(), :]
    return [categorized_df, uncategorized_df]


def predict_subcategories(uncategorized_df: pd.DataFrame) -> pd.DataFrame:

    df: pd.DataFrame = clean_descriptions([], uncategorized_df)

    model: MLModel = joblib.load(SUBCAT_MODEL_FILE)
    vectorizer: Vectorizer = joblib.load(SUBCAT_VECTORIZER_FILE)
    X_vectorized: spmatrix = vectorizer.transform(
        df[DataSchema.CLEANED_DESCRIPTION].to_numpy(dtype="<U50")
    )
    df.loc[:, DataSchema.SUBCATEGORY] = model.predict(X_vectorized)

    return df
