import pandas as pd

from data.categorize.finder import find_category, find_recurrences
from data.ml import randomforestclassifier
from data.raw.cleaner import clean_descriptions
from data.schema import DataSchema


def separate_data(df: pd.DataFrame) -> list[pd.DataFrame]:
    categorized_df = df.loc[df[DataSchema.SUBCATEGORY].notna(), :]
    uncategorized_df = df.loc[df[DataSchema.SUBCATEGORY].isna(), :]
    return [categorized_df, uncategorized_df]


def predict_subcategories(uncategorized_df: pd.DataFrame) -> pd.DataFrame:

    df = clean_descriptions([], uncategorized_df)

    df.loc[:, DataSchema.SUBCATEGORY] = randomforestclassifier.predict(
        df[DataSchema.CLEANED_DESCRIPTION]
    )

    df.loc[:, DataSchema.CATEGORY] = df[DataSchema.SUBCATEGORY].apply(
        find_category)

    df.loc[:, DataSchema.RECURRENT] = df[DataSchema.SUBCATEGORY].apply(
        find_recurrences
    )

    return df
