from dash import html, callback, Output, Input, State, dcc
import i18n
import plotly.express as px
import pandas as pd
from plotly.graph_objs._figure import Figure

from src.components import ids
from src.data.source import DataSource
from src.data.schema import DataSchema
from src.components.figures.monthly_expenses_sunburst_chart import set_color_palette


def render() -> html.Div:
    return html.Div(id=ids.EXPENSES_EVOLUTION_PER_CATEGORY)


@callback(
    Output(ids.EXPENSES_EVOLUTION_PER_CATEGORY, "children"),
    [
        Input(ids.EXPENSES_TABLE, "cellValueChanged"),
        Input(ids.YEAR_DROPDOWN, "value"),
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
        # color_discrete_sequence=px.colors.qualitative.Vivid,
        color_discrete_map=set_color_palette(),
        markers=True,
        category_orders={
            DataSchema.MONTH: [
                "Jan",
                "Fev",
                "Mar",
                "Abr",
                "Mai",
                "Jun",
                "Jul",
                "Ago",
                "Set",
                "Out",
                "Nov",
                "Dez",
            ]
        },
        labels={
            DataSchema.MONTH: i18n.t(f"columns.{DataSchema.MONTH}"),
            DataSchema.AMOUNT: i18n.t(f"columns.{DataSchema.AMOUNT}"),
            DataSchema.CATEGORY: i18n.t(f"columns.{DataSchema.CATEGORY}"),
        },
    )
    fig.update_layout(
        height=275,
        showlegend=True,
        yaxis={"title": None},
        xaxis={"tickangle": 0, "type": "category", "title": None},
        margin={"l": 0, "r": 0, "t": 30, "b": 30},
        paper_bgcolor="rgba(0,0,0,0)",
        legend={
            "orientation": "h",
            "yanchor": "top",
            "y": -0.25,
            "xanchor": "left",
            "x": 0,
        },
    )

    fig.update_traces(textposition="bottom center", marker={"size": 12})

    return html.Div(dcc.Graph(figure=fig), id=ids.EXPENSES_EVOLUTION_PER_CATEGORY)
