import pandas as pd

from data.categorize.finder import find_category, find_recurrences
from data.ml import randomforestclassifier
from data.raw.cleaner import clean_descriptions
from data.schema import DataSchema


def separate_uncategorized_data(df: pd.DataFrame) -> list[pd.DataFrame]:
    mask: pd.Series[bool] = df[DataSchema.SUBCATEGORY].isna()
    categorized_df = df.dropna()
    uncategorized_df = df.loc[mask, :]
    return [categorized_df, uncategorized_df]


def predict_subcategories(uncategorized_df: pd.DataFrame) -> pd.DataFrame:

    df = clean_descriptions([], uncategorized_df)

    df[DataSchema.SUBCATEGORY] = randomforestclassifier.predict(
        df[DataSchema.CLEANED_DESCRIPTION]
    )

    df[DataSchema.CATEGORY] = df[DataSchema.SUBCATEGORY].apply(find_category)

    df[DataSchema.RECURRENT] = df[DataSchema.SUBCATEGORY].apply(
        find_recurrences
    )

    return df
