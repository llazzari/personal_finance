from pathlib import Path
import pandas as pd

from data.categorize.finder import find_category, find_recurrences
from data.raw.cleaner import clean_descriptions
from data.schema import DataSchema
from data.ml.randomforestclassifier import load_model, load_vectorizer, predict

MODEL_FILE: Path = Path.cwd() / 'data' / 'ml' / 'model.joblib'
VECTORIZER_FILE: Path = Path.cwd() / 'data' / 'ml' / 'vectorizer.joblib'


def separate_data(df: pd.DataFrame) -> list[pd.DataFrame]:
    categorized_df = df.loc[df[DataSchema.SUBCATEGORY].notna(), :]
    uncategorized_df = df.loc[df[DataSchema.SUBCATEGORY].isna(), :]
    return [categorized_df, uncategorized_df]


def predict_subcategories(uncategorized_df: pd.DataFrame) -> pd.DataFrame:

    df = clean_descriptions([], uncategorized_df)

    model = load_model(MODEL_FILE)
    vectorizer = load_vectorizer(VECTORIZER_FILE)
    df.loc[:, DataSchema.SUBCATEGORY] = predict(
        df[DataSchema.CLEANED_DESCRIPTION].to_numpy(dtype='<U21'),
        model,
        vectorizer
    )

    df.loc[:, DataSchema.CATEGORY] = df[DataSchema.SUBCATEGORY].apply(
        find_category)

    df.loc[:, DataSchema.RECURRENT] = df[DataSchema.SUBCATEGORY].apply(
        find_recurrences
    )

    return df
