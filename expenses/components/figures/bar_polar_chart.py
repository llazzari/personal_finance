from dash import Dash, html, dcc, Output, Input
import plotly.express as px
import pandas as pd
import i18n

from components import ids
from components.figures import styles
from data.schema import DataSchema
from data.categorize.finder import find_category


def render(app: Dash) -> html.Div:
    @app.callback(
        Output(ids.BAR_POLAR_CHART, 'children'),
        [
            Input(ids.EXPENSES_TABLE, 'data'),
            Input(ids.MONTH_DROPDOWN, 'value'),
            Input(ids.YEAR_DROPDOWN, 'value'),
        ],
    )
    def update_bar_chart(data: dict, month: int, year: int) -> html.Div:
        df = pd.DataFrame.from_records(data)
        if df.empty:
            return html.Div(i18n.t('general.no_data'))
        df_year = df.loc[df[DataSchema.YEAR] == year, :]
        df_month = df_year.loc[df_year[DataSchema.MONTH] == month, :]

        df_month_sum = df_month.groupby(
            by=DataSchema.SUBCATEGORY
        ).sum().reset_index().sort_values(by=DataSchema.AMOUNT)
        df_month_sum.loc[:, DataSchema.CATEGORY] = df_month_sum[
            DataSchema.SUBCATEGORY
        ].apply(find_category)
        # color_palette: dict[str, str] = {
        #     i18n.t(f'category.{category}'): color
        #     for category, color in styles.categories_palette.items()
        # }
        fig = px.bar_polar(
            df_month_sum,
            theta=DataSchema.CATEGORY,
            r=DataSchema.AMOUNT,
            color=DataSchema.AMOUNT,
            # color_discrete_map=color_palette,
            color_continuous_scale=px.colors.sequential.Cividis,
            # color_discrete_sequence=list(styles.categories_palette.values()),
            labels={
                DataSchema.AMOUNT: i18n.t(f'columns.{DataSchema.AMOUNT}'),
                DataSchema.CATEGORY: i18n.t(f'columns.{DataSchema.CATEGORY}'),
                DataSchema.SUBCATEGORY: i18n.t(
                    f'columns.{DataSchema.SUBCATEGORY}'
                ),
            },
            hover_data=[DataSchema.SUBCATEGORY],
            barmode='group',
        )
        styles.standardize(fig)
        fig.update_polars(angularaxis=dict(tickfont=dict(size=16)))
        return html.Div(dcc.Graph(figure=fig), id=ids.BAR_POLAR_CHART)
    return html.Div(id=ids.BAR_POLAR_CHART)
