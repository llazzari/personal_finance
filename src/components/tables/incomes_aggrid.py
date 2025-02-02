from dash import html
import dash_ag_grid as dag

from .. import ids
from . import grid_options, columns, incomes_columns


def render(data: list[dict]) -> html.Div:
    return html.Div(
        dag.AgGrid(
            rowData=data,
            columnDefs=incomes_columns.set_income_columns(),
            defaultColDef=columns.DEFAULT_COLUMN_DEFINITION,
            columnSize="sizeToFit",
            dashGridOptions=grid_options.set_dash_grid_options(),
            getRowId="params.data.id",
            id=ids.INCOMES_TABLE,
        ),
        className="dbc dbc-ag-grid",
    )
