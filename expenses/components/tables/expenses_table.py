from typing import Any, Hashable
from dash import Dash, html, dash_table, Output, Input
import pandas as pd
import i18n

from data.schema import DataSchema
from components import ids
from components.tables import style, dropdown, helpers
from components.tables.columns import TableColumns


def render(app: Dash) -> html.Div:
    @app.callback(
        Output(ids.TABLE_CONTAINER, 'children'),
        Input(ids.TABLE_DATA, 'data'),
        # prevent_initial_call=True
    )
    def update_table(df_records: list[dict[Hashable, Any]]):
        df = pd.DataFrame.from_records(df_records)
        if df.empty:
            return html.Div(
                html.H3(i18n.t("general.no_data")),  # type: ignore
                id=ids.TABLE_CONTAINER
            )

        table_columns = TableColumns()
        categories: list[str] = helpers.get_categories_names()
        recurrent_options: list[str] = helpers.get_recurrent_options()

        return html.Div(
            dash_table.DataTable(
                data=df_records,
                columns=table_columns.set_columns(),
                id=ids.EXPENSES_TABLE,
                row_deletable=True,
                sort_action='native',
                dropdown={
                    DataSchema.CATEGORY: dropdown.set_dropdown_for(categories),
                    DataSchema.RECURRENT: dropdown.set_dropdown_for(
                        recurrent_options
                    )
                },
                dropdown_conditional=dropdown.set_conditional_dropdown_for_subcategories(),
                style_as_list_view=True,
                page_size=10,
                style_header=style.HEADER,
                style_cell=style.CELL,
                style_cell_conditional=style.CELL_CONDITIONAL,
                style_data_conditional=style.DATA_CONDITIONAL,
                style_data=style.DATA,
                filter_action='native',
                # style_table=style.TABLE,
                tooltip_data=style.tooltip_data(df),
                tooltip_duration=None
            ),
            style={
                'textAlign': 'center',
                "margin": "20px",
            },
            id=ids.TABLE_CONTAINER,
            className='dbc dbc-row-selectable',
        )

    return html.Div(id=ids.TABLE_CONTAINER)
