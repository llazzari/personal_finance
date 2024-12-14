from dash import callback, html, dcc, Output, Input, State
import plotly.express as px
import pandas as pd
import i18n
from plotly.graph_objs._figure import Figure

from src.components import ids
from src.data.schema import DataSchema
from src.data.source import DataSource


def render() -> html.Div:
    return html.Div(id=ids.HORIZONTAL_BAR_CHART)


@callback(
    Output(ids.HORIZONTAL_BAR_CHART, "children"),
    [
        Input(ids.INCOMES_TABLE, "cellValueChanged"),
        Input(ids.MONTH_DROPDOWN, "value"),
        Input(ids.YEAR_DROPDOWN, "value"),
    ],
    State(ids.INCOMES_TABLE, "rowData"),
)
def update_bar_chart(_, month: int, year: int, data: list[dict]) -> html.Div:
    source = DataSource(data)
    df: pd.DataFrame = source.month_income_by_category(month, year)

    fig: Figure = px.bar(
        df,
        x=DataSchema.CATEGORY,
        y=DataSchema.AMOUNT,
        color=DataSchema.CATEGORY,
        color_discrete_sequence=[
            "#69ADF5",
            "#5890CC",
            "#4775A6",
            "#375B81",
        ],  # px.colors.qualitative.Vivid,
        labels={
            DataSchema.AMOUNT: i18n.t(f"columns.{DataSchema.AMOUNT}"),
            DataSchema.CATEGORY: i18n.t(f"columns.{DataSchema.CATEGORY}"),
        },
        orientation="v",
        title=i18n.t("general.incomes_source"),
        text=DataSchema.AMOUNT,
    )
    fig.update_layout(
        height=175,
        showlegend=False,
        yaxis={"visible": False, "showticklabels": False},
        xaxis={"tickangle": 45, "type": "category", "title": None},
        margin={"l": 0, "r": 0, "t": 30, "b": 0},
        paper_bgcolor="rgba(0,0,0,0)",
    )
    fig.update_traces(textangle=0, textposition="outside", cliponaxis=False)

    return html.Div(dcc.Graph(figure=fig), id=ids.HORIZONTAL_BAR_CHART)
