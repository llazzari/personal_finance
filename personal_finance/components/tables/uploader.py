from typing import Any

from data.raw.uploader import upload_personal_table_data


def get_old_data_id(old_data: list[dict]) -> int:
    if not old_data:
        return -1
    return max([data['id'] for data in old_data])


def upload_data(old_data: list[dict], contents: list[str]) -> dict[str, Any]:

    old_data_id = get_old_data_id(old_data)
    new_df = upload_personal_table_data(contents)
    new_df['id'] = range(old_data_id+1, old_data_id+1+len(new_df))

    return {'add': new_df.to_dict('records'), 'addIndex': 0}
