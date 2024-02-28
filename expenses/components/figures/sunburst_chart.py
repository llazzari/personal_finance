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
        Output(ids.SUNBURST_CHART, 'children'),
        [
            Input(ids.EXPENSES_TABLE, 'rowData'),
            Input(ids.MONTH_DROPDOWN, 'value'),
            Input(ids.YEAR_DROPDOWN, 'value'),
        ],
    )
    def update_chart(data: dict, month: int, year: int) -> html.Div:
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

        fig = px.sunburst(
            df_month_sum,
            path=[DataSchema.CATEGORY, DataSchema.SUBCATEGORY],
            values=DataSchema.AMOUNT,
            color=DataSchema.CATEGORY,
            # color_discrete_sequence=styles.COLOR_DISCRETE_SEQUENCE,
        )

        styles.standardize(fig)

        AMOUNT_LABEL: str = i18n.t(f"columns.{DataSchema.AMOUNT}")
        SUBCATEGORY_LABEL: str = i18n.t(f'columns.{DataSchema.SUBCATEGORY}')
        CATEGORY_LABEL: str = i18n.t(f'columns.{DataSchema.CATEGORY}')

        color_palette: dict[str, str] = set_color_palette()
        fig.update_traces(
            textinfo="label+percent parent",
            insidetextorientation='horizontal',
            marker_colors=[
                color_palette[cat] for cat in fig.data[-1].labels
            ],
        )
        fig.update_traces(
            hovertemplate=f'<b>{AMOUNT_LABEL}: %{{value:.2f}} </b>' +
            f'<br>{CATEGORY_LABEL}/{SUBCATEGORY_LABEL}: %{{id}}'
        )
        return html.Div(dcc.Graph(figure=fig), id=ids.SUNBURST_CHART)
    return html.Div(id=ids.SUNBURST_CHART)


def set_color_palette() -> dict[str, str]:
    color_palette: dict[str, str] = {
        i18n.t(f'category.{category}'): color
        for category, color in styles.categories_palette.items()
    }
    subcolor_palette: dict[str, str] = {
        i18n.t(f'subcategory.{subcategory}'): color
        for subcategory, color in styles.subcategories_palette.items()
    }
    color_palette.update(subcolor_palette)
    return color_palette
