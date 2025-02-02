"""Uploads the data to the Dash AgGrids."""

from typing import Any
import pandas as pd


def get_old_data_id(old_data: list[dict]) -> int:
    """
    Get the maximum ID value from a list of dictionaries.

    Args:
        old_data (list[dict]): A list of dictionaries containing "id" keys.

    Returns:
        int: The maximum ID value from the list of dictionaries. If the list is empty, -1 is returned.
    """

    if not old_data:
        return -1
    return max([data["id"] for data in old_data])


def upload_data(old_data: list[dict], new_df: pd.DataFrame) -> dict[str, Any]:
    """
    Uploads new data to an existing dataset by combining it with old data.

    Args:
        old_data (list[dict]): The existing dataset in the form of a list of dictionaries.
        new_df (pd.DataFrame): The new data to be uploaded as a pandas DataFrame.

    Returns:
        dict[str, Any]: A dictionary containing the uploaded data. The dictionary has two keys:
            - "add": A list of dictionaries representing the new data.
            - "addIndex": An integer representing the index at which the new data should be added.
    """
    old_data_id: int = get_old_data_id(old_data) + 1
    new_df["id"] = range(old_data_id, old_data_id + len(new_df))

    return {"add": new_df.to_dict("records"), "addIndex": 0}
