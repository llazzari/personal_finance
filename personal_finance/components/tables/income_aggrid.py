from dash import html
import dash_ag_grid as dag

from components import ids
from components.tables import grid_options


def render(data: list[dict]) -> html.Div:

    return html.Div(
        dag.AgGrid(
            rowData=data,
            columnDefs=grid_options.set_columns(),
            defaultColDef=grid_options.DEFAULT_COLUMN_DEFINITION,
            columnSize='responsiveSizeToFit',
            dashGridOptions=grid_options.set_dash_grid_options(),
            getRowId='params.data.id',
            id=ids.INCOMES_TABLE,
        ),
        className='dbc dbc-ag-grid'
    )
