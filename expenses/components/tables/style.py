import pandas as pd
from data.schema import DataSchema

ConditionalData = dict[str, str | dict[str, str]]


HEADER: dict[str, str] = {'fontWeight': 'bold'}
CELL: dict[str, str | int] = {'text-align': 'left'}
CELL_CONDITIONAL: list[dict[str, str | int | dict[str, str]]] = [
    {
        'if': {'column_type': 'numeric'},
        'textAlign': 'right',
    },
    {
        'if': {'column_id': DataSchema.AMOUNT},
        'padding-right': '5px',
    },
    {
        'if': {'column_id': DataSchema.DESCRIPTION},
        'overflow': 'hidden',
        'textOverflow': 'ellipsis',
    }
]
CELL_CONDITIONAL_INPUT: list[dict[str, str | dict[str, str]]] = [
    {
        'if': {'column_id': DataSchema.AMOUNT},
        'textAlign': 'right',
        'padding-right': '5px',
    },
]
DATA: dict[str, str] = {
    # 'whiteSpace': 'normal',
    # 'height': 'auto',
}
DATA_CONDITIONAL: list[dict[str, str | dict[str, str]]] = [
    {
        'if': {'column_id': id},
        'width': width, 'minWidth': width, 'maxWidth': width,
        # 'overflow': 'auto',
        # 'textOverflow': 'ellipsis',
    }
    for id, width in zip(
        [
            DataSchema.YEAR,
            DataSchema.MONTH,
            DataSchema.AMOUNT,
            DataSchema.BANK,
            DataSchema.CATEGORY,
            DataSchema.SUBCATEGORY,
            DataSchema.RECURRENT,
            DataSchema.DESCRIPTION
        ],
        ['30px', '20px', '30px', '80px', '150px', '150px', '20px', '50px']
    )
]


def tooltip_data(df: pd.DataFrame) -> list[dict]:
    return [
        {
            column: {'value': str(value), 'type': 'markdown'}
            for column, value in row.items()
        } for row in df.to_dict('records')
    ]


TABLE = {'overflowX': 'auto'}
