from dataclasses import dataclass
from typing import Any, Hashable
import pandas as pd


DashData = list[dict[Hashable, Any]]


@dataclass
class DataSource:
    _data: pd.DataFrame

    @property
    def table_data(self) -> DashData:
        return self._data.to_dict('records')
