from dataclasses import dataclass
import pandas as pd


@dataclass
class DataSource:
    _data: pd.DataFrame

    @property
    def table_data(self) -> list[dict]:
        return self._data.to_dict('records')
