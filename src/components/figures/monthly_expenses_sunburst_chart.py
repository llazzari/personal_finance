from dash import callback, html, dcc, Output, Input, State
from pandas import DataFrame
import plotly.express as px
import i18n
from plotly.graph_objs._figure import Figure

from src.components import ids
from src.components.figures import styles
from src.data.schema import DataSchema
from src.data.source import DataSource


def render() -> html.Div:
    return html.Div(id=ids.SUNBURST_CHART)


def set_color_palette() -> dict[str, str]:
    color_palette: dict[str, str] = {
        i18n.t(f"category.{category}"): color
        for category, color in styles.categories_palette.items()
    }
    subcolor_palette: dict[str, str] = {
        i18n.t(f"subcategory.{subcategory}"): color
        for subcategory, color in styles.subcategories_palette.items()
    }
    color_palette.update(subcolor_palette)
    return color_palette


@callback(
    Output(ids.SUNBURST_CHART, "children"),
    [
        Input(ids.EXPENSES_TABLE, "cellValueChanged"),
        Input(ids.MONTH_DROPDOWN, "value"),
        Input(ids.YEAR_DROPDOWN, "value"),
    ],
    State(ids.EXPENSES_TABLE, "rowData"),
)
def update_chart(_, month: int, year: int, data: list[dict]) -> html.Div:
    source = DataSource(data)
    df_month_sum: DataFrame = source.month_expense_by_subcat(year, month)

    fig: Figure = px.sunburst(
        df_month_sum,
        path=[DataSchema.CATEGORY, DataSchema.SUBCATEGORY],
        values=DataSchema.AMOUNT,
        color=DataSchema.CATEGORY,
        title=i18n.t("general.expenses"),
    )

    AMOUNT_LABEL: str = i18n.t(f"columns.{DataSchema.AMOUNT}")
    SUBCATEGORY_LABEL: str = i18n.t(f"columns.{DataSchema.SUBCATEGORY}")
    CATEGORY_LABEL: str = i18n.t(f"columns.{DataSchema.CATEGORY}")

    color_palette: dict[str, str] = set_color_palette()
    fig.update_layout(
        height=200,
        showlegend=False,
        margin={"l": 0, "r": 0, "t": 30, "b": 0},
        paper_bgcolor="rgba(0,0,0,0)",
    )
    fig.update_traces(
        textinfo="label+percent parent",
        insidetextorientation="horizontal",
        marker_colors=[color_palette[cat] for cat in fig.data[-1].labels],  # type: ignore
    )
    fig.update_traces(
        hovertemplate=f"<b>{AMOUNT_LABEL}: %{{value:.2f}} </b>"
        + f"<br>{CATEGORY_LABEL}/{SUBCATEGORY_LABEL}: %{{id}}"
    )
    return html.Div(dcc.Graph(figure=fig), id=ids.SUNBURST_CHART)
