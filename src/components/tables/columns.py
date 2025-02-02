import i18n

Column = dict[str, str | int | bool | dict[str, str | list[str]]]
ColumnTypes = dict[str, dict[str, str | int | bool]]

column_types: ColumnTypes = {
    "number_column": {"filter": "agNumberColumnFilter", "editable": False},
}

DEFAULT_COLUMN_DEFINITION: dict[str, str | bool] = {
    "sortable": False,
    "filter": "agTextColumnFilter",
    "floatingFilter": True,
    "editable": False,
}


def set_column(column: str) -> Column:
    return {
        "field": column,
        "headerName": i18n.t(f"columns.{column}"),
    }


def set_column_with_dropdown(column: str, values: list[str]) -> Column:
    column_defs: Column = set_column(column)
    column_defs["cellEditor"] = "agSelectCellEditor"
    column_defs["cellEditorParams"] = {"values": values}  # type: ignore
    column_defs["editable"] = True
    return column_defs


def set_number_column(column: str) -> Column:
    column_defs: Column = set_column(column)
    column_defs["type"] = "numericColumn"
    column_defs["filter"] = "agNumberColumnFilter"
    column_defs["sortable"] = True
    column_defs["valueParser"] = {"function": "Number(params.newValue)"}
    return column_defs
