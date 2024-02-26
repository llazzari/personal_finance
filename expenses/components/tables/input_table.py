from typing import Any, Hashable
from dash import Dash, html, Output, Input, State, dash_table
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import i18n
import pandas as pd

from components import ids
from data.schema import DataSchema
from data.loader import set_table_data
from components.tables import style, columns, dropdown, helpers


DashData = list[dict[Hashable, Any]]


class InputTableColumns(columns.TableColumns):
    def set_column(self, column: str) -> dict[str, Any]:
        column_options = super().set_column(column)
        column_options['editable'] = True
        return column_options

    def year_column(self) -> dict[str, Any]:
        year_column = super().year_column()
        year_column['presentation'] = 'dropdown'
        return year_column

    def month_column(self) -> dict[str, Any]:
        month_column = super().month_column()
        month_column['presentation'] = 'dropdown'
        return month_column


def render(app: Dash) -> html.Div:
    @app.callback(
        Output(ids.EXPENSES_MODAL_BODY, 'children'),
        Input(ids.INSERT_MANUAL_DATA, 'n_clicks'),
        State(ids.NUMBER_ADD, 'value'),
        prevent_initial_call=True
    )
    def new_rows(_, n_rows: int) -> html.Div:
        if n_rows is None:
            return html.Div()
        table_columns = InputTableColumns()

        categories: list[str] = helpers.get_categories_names()
        recurrent: list[str] = helpers.get_recurrent_options()

        return html.Div([
            dash_table.DataTable(
                data=[{} for _ in range(n_rows)],
                columns=table_columns.set_columns(),
                id=ids.ADD_EXPENSES_TABLE,
                editable=True,
                dropdown={
                    DataSchema.CATEGORY: dropdown.set_dropdown_for(categories),
                    DataSchema.YEAR: dropdown.set_dropdown_for(
                        helpers.get_year_options()
                    ),
                    DataSchema.MONTH: dropdown.set_dropdown_for(
                        helpers.get_month_options()
                    ),
                    DataSchema.RECURRENT: dropdown.set_dropdown_for(recurrent)
                },
                dropdown_conditional=dropdown.set_conditional_dropdown_for_subcategories(),
                style_header=style.HEADER,
                style_cell=style.CELL,
                style_cell_conditional=style.CELL_CONDITIONAL_INPUT,
            ),
            dbc.Button(
                i18n.t('general.save'),  # type: ignore
                id=ids.SAVE_ADDED_DATA,
                style={'margin': '10px'},
            ),
        ],
            className='dbc dbc-row-selectable',
        )
    return html.Div(id=ids.EXPENSES_MODAL_BODY)


def save_data(app: Dash) -> None:
    @app.callback(
        [Output(ids.TABLE_DATA, 'data', allow_duplicate=True),
         Output(ids.EXPENSES_MODAL, 'is_open', allow_duplicate=True)],
        Input(ids.SAVE_ADDED_DATA, 'n_clicks'),
        State(ids.ADD_EXPENSES_TABLE, 'data'),
        prevent_initial_call=True,
    )
    def update_table(
        n: int | None,
        data: DashData,
    ) -> tuple[DashData, bool]:
        if n is None:
            raise PreventUpdate
        new_df = pd.DataFrame.from_records(data)
        df: pd.DataFrame = set_table_data(new_df)

        return df.to_dict('records'), False
