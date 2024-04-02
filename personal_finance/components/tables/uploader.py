from typing import Any
import pandas as pd


def get_old_data_id(old_data: list[dict]) -> int:
    if not old_data:
        return -1
    return max([data["id"] for data in old_data])


def upload_data(old_data: list[dict], new_df: pd.DataFrame) -> dict[str, Any]:

    old_data_id: int = get_old_data_id(old_data)
    new_df["id"] = range(old_data_id + 1, old_data_id + 1 + len(new_df))

    return {"add": new_df.to_dict("records"), "addIndex": 0}
