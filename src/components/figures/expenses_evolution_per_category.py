from dash import html, callback, Output, Input, State, dcc
import i18n
import plotly.express as px
import pandas as pd
from plotly.graph_objs._figure import Figure

from src.components import ids
from src.data.source import DataSource
from src.data.schema import DataSchema


def render() -> html.Div:
    return html.Div(id=ids.EXPENSES_EVOLUTION_PER_CATEGORY)


@callback(
    Output(ids.EXPENSES_EVOLUTION_PER_CATEGORY, "children"),
    [
        Input(ids.EXPENSES_TABLE, "cellValueChanged"),
        Input(ids.YEAR_DROPDOWN_EVOLUTION, "value"),
    ],
    [State(ids.EXPENSES_TABLE, "rowData")],
)
def update_chart(_, year: int, expenses: list[dict]) -> html.Div:
    if not expenses:
        return html.Div(id=ids.EXPENSES_EVOLUTION_PER_CATEGORY)

    data: list[dict] = expenses
    source = DataSource(data)
    df: pd.DataFrame = source.evolution_per_category(year)

    fig: Figure = px.line(
        df,
        x=DataSchema.MONTH,
        y=DataSchema.AMOUNT,
        color=DataSchema.CATEGORY,
        symbol=DataSchema.CATEGORY,
        title=i18n.t("general.expenses_evolution_per_category"),
        color_discrete_sequence=px.colors.qualitative.Vivid,
        markers=True,
        labels={
            DataSchema.MONTH: i18n.t(f"columns.{DataSchema.MONTH}"),
            DataSchema.AMOUNT: i18n.t(f"columns.{DataSchema.AMOUNT}"),
            DataSchema.CATEGORY: i18n.t(f"columns.{DataSchema.CATEGORY}"),
        },
    )
    fig.update_traces(textposition="bottom center", marker={"size": 12})

    return html.Div(dcc.Graph(figure=fig), id=ids.EXPENSES_EVOLUTION_PER_CATEGORY)
