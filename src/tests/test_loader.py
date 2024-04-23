from pathlib import Path
import pandas as pd
from hypothesis import given
from hypothesis.strategies import integers, lists

from src.data.schema import DataSchema
from src.data.loader import load_data, sort_by_date


# Test cases for load_data function


def test_load_data_with_existing_file(tmp_path: Path) -> None:
    # Create a temporary CSV file with some data
    file_path: Path = tmp_path / "test_data.csv"
    df = pd.DataFrame(
        {
            DataSchema.YEAR: [2021, 2021, 2021],
            DataSchema.MONTH: [1, 2, 3],
            DataSchema.AMOUNT: [100.0, 200.0, 300.0],
            DataSchema.BANK: ["A", "A", "A"],
            DataSchema.CATEGORY: ["B", "B", "B"],
            DataSchema.SUBCATEGORY: ["C", "C", "C"],
            DataSchema.RECURRENT: ["D", "D", "D"],
            DataSchema.DESCRIPTION: ["E1", "E2", "E3"],
        }
    )
    df.to_csv(file_path, index=False)

    # Call load_data and check the returned DataFrame
    expected_df = pd.DataFrame(
        {
            DataSchema.YEAR: [2021, 2021, 2021],
            DataSchema.MONTH: [1, 2, 3],
            DataSchema.AMOUNT: [100.0, 200.0, 300.0],
            DataSchema.BANK: ["A", "A", "A"],
            DataSchema.CATEGORY: ["B", "B", "B"],
            DataSchema.SUBCATEGORY: ["C", "C", "C"],
            DataSchema.RECURRENT: ["D", "D", "D"],
            DataSchema.DESCRIPTION: ["E1", "E2", "E3"],
            "id": [0, 1, 2],
        }
    )
    expected_df: pd.DataFrame = expected_df.sort_values(
        by=[DataSchema.YEAR, DataSchema.MONTH], ascending=False
    )
    actual_df: pd.DataFrame = load_data(file_path)
    pd.testing.assert_frame_equal(actual_df, expected_df)


def test_load_data_with_nonexistent_file(tmp_path: Path) -> None:
    # Create a temporary directory with no file
    file_path: Path = tmp_path / "nonexistent.csv"

    # Call load_data and check the returned DataFrame
    expected_df = pd.DataFrame()
    actual_df: pd.DataFrame = load_data(file_path)
    pd.testing.assert_frame_equal(actual_df, expected_df)


# Test cases for sort_by_date function


@given(data=lists(integers(), min_size=1))
def test_sort_by_date(data: list[int]) -> None:
    # Generate random data with sort_column as the column to sort by
    df = pd.DataFrame({DataSchema.YEAR: data, DataSchema.MONTH: data})
    expected_df: pd.DataFrame = df.sort_values(
        by=[DataSchema.YEAR, DataSchema.MONTH], ascending=False
    )

    # Call sort_by_date and check if the DataFrame is sorted correctly
    actual_df: pd.DataFrame = sort_by_date(df)
    pd.testing.assert_frame_equal(actual_df, expected_df)


# Test case to check if sort_by_date is idempotent
@given(data=lists(integers(), min_size=1))
def test_sort_by_date_idempotent(data: list[int]) -> None:
    # Generate random data with sort_column as the column to sort by
    df = pd.DataFrame({DataSchema.YEAR: data, DataSchema.MONTH: data})

    # Call sort_by_date twice and check if the DataFrame remains unchanged
    sorted_df_once: pd.DataFrame = sort_by_date(df)
    sorted_df_twice: pd.DataFrame = sort_by_date(sorted_df_once)
    pd.testing.assert_frame_equal(sorted_df_once, sorted_df_twice)
