from dash import html, dcc, Output, Input, State, callback
import plotly.express as px
import pandas as pd
import i18n
from plotly.graph_objs._figure import Figure

from src.components import ids
from src.data.schema import DataSchema
from src.data.source import DataSource


def render() -> html.Div:
    return html.Div(id=ids.YEARLY_EVOLUTION_LINE_CHART)


@callback(
    Output(ids.YEARLY_EVOLUTION_LINE_CHART, "children"),
    [
        Input(ids.EXPENSES_TABLE, "cellValueChanged"),
        Input(ids.INCOMES_TABLE, "cellValueChanged"),
    ],
    [
        State(ids.EXPENSES_TABLE, "rowData"),
        State(ids.INCOMES_TABLE, "rowData"),
    ],
)
def update_chart(_, __, expenses: list[dict], incomes: list[dict]) -> html.Div:
    for e in expenses:
        e[DataSchema.TYPE] = i18n.t("general.expenses")
    for i in incomes:
        i[DataSchema.TYPE] = i18n.t("general.incomes")

    data: list[dict] = expenses + incomes
    source = DataSource(data)
    df: pd.DataFrame = source.yearly_evolution()

    fig: Figure = px.line(
        df,
        x=DataSchema.YEAR,
        y=DataSchema.AMOUNT,
        color=DataSchema.TYPE,
        symbol=DataSchema.TYPE,
        color_discrete_sequence=px.colors.qualitative.Set1,
        labels={
            DataSchema.AMOUNT: i18n.t(f"columns.{DataSchema.AMOUNT}"),
            DataSchema.YEAR: i18n.t(f"columns.{DataSchema.YEAR}"),
            DataSchema.TYPE: i18n.t(f"columns.{DataSchema.TYPE}"),
        },
        # title=i18n.t("general.yearly_evolution"),
        markers=True,
    )
    fig.update_layout(
        xaxis={"tickangle": 0, "type": "category", "title": None},
        height=200,
        yaxis={"title": None},
        margin={"l": 0, "r": 0, "t": 30, "b": 0},
        paper_bgcolor="rgba(0,0,0,0)",
        legend={
            "orientation": "h",
            "yanchor": "bottom",
            "y": 1.02,
            "xanchor": "right",
            "x": 1,
        },
    )

    return html.Div(dcc.Graph(figure=fig), id=ids.YEARLY_EVOLUTION_LINE_CHART)
