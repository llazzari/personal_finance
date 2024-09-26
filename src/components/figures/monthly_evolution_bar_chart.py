from dash import callback, html, Input, Output, dcc, State
from pandas import DataFrame
import plotly.express as px
import i18n
from plotly.graph_objs._figure import Figure

from src.components import ids
from src.data.schema import DataSchema
from src.data.source import DataSource


def render() -> html.Div:
    return html.Div(id=ids.BAR_CHART)


@callback(
    Output(ids.BAR_CHART, "children"),
    [
        Input(ids.EXPENSES_TABLE, "cellValueChanged"),
        Input(ids.INCOMES_TABLE, "cellValueChanged"),
        Input(ids.YEAR_DROPDOWN_EVOLUTION, "value"),
    ],
    [
        State(ids.EXPENSES_TABLE, "rowData"),
        State(ids.INCOMES_TABLE, "rowData"),
    ],
)
def update_chart(
    _, __, year: int, expenses: list[dict], incomes: list[dict]
) -> html.Div:
    for e in expenses:
        e[DataSchema.TYPE] = i18n.t("general.expenses")
    for i in incomes:
        i[DataSchema.TYPE] = i18n.t("general.incomes")

    data: list[dict] = expenses + incomes
    source = DataSource(data)
    df: DataFrame = source.evolution(year)

    fig: Figure = px.bar(
        df,
        x=DataSchema.MONTH,
        y=DataSchema.AMOUNT,
        color=DataSchema.TYPE,
        labels={
            DataSchema.MONTH: i18n.t(f"columns.{DataSchema.MONTH}"),
            DataSchema.AMOUNT: i18n.t(f"columns.{DataSchema.AMOUNT}"),
            DataSchema.RECURRENT: i18n.t(f"columns.{DataSchema.RECURRENT}"),
            DataSchema.TYPE: i18n.t(f"columns.{DataSchema.TYPE}"),
        },
        hover_data={DataSchema.RECURRENT: True, DataSchema.TYPE: True},
        category_orders={
            DataSchema.RECURRENT: [
                i18n.t(f"general.recurrent_{option}") for option in ["yes", "no"]
            ],
            DataSchema.TYPE: [
                i18n.t(f"general.{typee}") for typee in ["expenses", "incomes"]
            ],
        },
        color_discrete_sequence=px.colors.qualitative.Set1,
        barmode="group",
    )
    fig.update_layout(xaxis_type="category")
    return html.Div(
        dcc.Graph(figure=fig),
        id=ids.BAR_CHART,
    )
