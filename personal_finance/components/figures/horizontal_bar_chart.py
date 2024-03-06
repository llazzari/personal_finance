from dash import callback, html, dcc, Output, Input
import plotly.express as px
import pandas as pd
import i18n

from components import ids
from components.figures import styles
from data.schema import DataSchema
from data.source import DataSource


def render() -> html.Div:
    return html.Div(id=ids.HORIZONTAL_BAR_CHART)


@callback(
    Output(ids.HORIZONTAL_BAR_CHART, 'children'),
    [
        Input(ids.INCOMES_TABLE, 'rowData'),
        Input(ids.MONTH_DROPDOWN, 'value'),
        Input(ids.YEAR_DROPDOWN, 'value'),
    ],
)
def update_bar_chart(data: list[dict], month: int, year: int) -> html.Div:
    source = DataSource(data)
    if source.is_empty:
        return html.Div(i18n.t('general.no_data'))

    df: pd.DataFrame = source.month_income_by_category(
        month, year
    )

    fig = px.bar(
        df,
        y=DataSchema.CATEGORY,
        x=DataSchema.AMOUNT,
        color=DataSchema.AMOUNT,
        color_continuous_scale=px.colors.sequential.Greens[3:],
        labels={
            DataSchema.AMOUNT: i18n.t(f'columns.{DataSchema.AMOUNT}'),
            DataSchema.CATEGORY: i18n.t(f'columns.{DataSchema.CATEGORY}'),
        },
        barmode='group',
        orientation='h',
        title=i18n.t('general.incomes'),
    )
    styles.standardize(fig)
    fig.update_polars(angularaxis=dict(tickfont=dict(size=16)))
    return html.Div(dcc.Graph(figure=fig), id=ids.HORIZONTAL_BAR_CHART)
