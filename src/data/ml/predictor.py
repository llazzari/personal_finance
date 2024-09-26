from typing import Protocol
import joblib
import numpy as np
import pandas as pd
from scipy.sparse import spmatrix

from ..raw.cleaner import clean_descriptions
from ..schema import DataSchema
from .trainer import (
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
    """
    Perform subcategory prediction on the given DataFrame using a pre-trained ML model.

    Parameters:
    - uncategorized_df: pd.DataFrame, the DataFrame containing uncategorized data to predict
    subcategories for.

    Returns:
    - pd.DataFrame, the DataFrame with predicted subcategories.
    """
    df: pd.DataFrame = clean_descriptions([], uncategorized_df)

    model: MLModel = joblib.load(SUBCAT_MODEL_FILE)
    vectorizer: Vectorizer = joblib.load(SUBCAT_VECTORIZER_FILE)
    X_vectorized: spmatrix = vectorizer.transform(
        df[DataSchema.CLEANED_DESCRIPTION].to_numpy(dtype="<U50")
    )
    df.loc[:, DataSchema.SUBCATEGORY] = model.predict(X_vectorized)

    return df
